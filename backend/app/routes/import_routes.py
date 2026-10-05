from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException,
    BackgroundTasks
)

from datetime import datetime

from fastapi.responses import StreamingResponse

import csv
import io

from sqlalchemy.orm import Session

from app.config.database import get_db

from io import BytesIO

from app.config.database import SessionLocal
from app.services.import_service import process_import

from app.services.import_service import (
    validate_import,
    validate_import_file,
    process_import
)

from app.models.import_history import ImportHistory

from app.models.import_error import (
    ImportErrorRecord
)

from app.config.jwt import get_current_user


router = APIRouter(
    prefix="/api/import",
    tags=["Data Import"]
)

async def run_import_in_background(
    import_type: str,
    import_id: int,
    company_id: int,
    user_id: int,
    file_content: bytes,
    filename: str
):

    db = SessionLocal()

    try:

        file = UploadFile(
            filename=filename,
            file=BytesIO(file_content)
        )

        await process_import(
            db=db,
            company_id=company_id,
            user_id=user_id,
            import_id=import_id,
            import_type=import_type,
            file=file
        )

    finally:

        db.close()


# =========================================================
# Admin authorization
# =========================================================

def require_admin(current_user):

    if current_user.role not in [
        "Super Admin",
        "Company Admin",
        "Admin"
    ]:

        raise HTTPException(
            status_code=403,
            detail="Administrator access required."
        )

    return current_user


# =========================================================
# 1. UPLOAD
# POST /api/import/upload
# =========================================================

@router.post("/upload")
async def upload_import(

    import_type: str,

    file: UploadFile = File(...),

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    require_admin(current_user)


    if import_type not in [
        "products",
        "inventory",
        "customers",
        "sales"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Invalid import type."
        )


    MAX_FILE_SIZE = 10 * 1024 * 1024


    content = await file.read()


    if len(content) > MAX_FILE_SIZE:

        raise HTTPException(
            status_code=400,
            detail="File size cannot exceed 10 MB."
        )


    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )


    if not file.filename.lower().endswith(".csv"):

        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported."
        )


    from io import BytesIO

    file.file = BytesIO(content)


    result = await validate_import(

        db=db,

        company_id=current_user.company_id,

        user_id=current_user.id,

        import_type=import_type,

        file=file

    )


    return result


# =========================================================
# 2. VALIDATE
# POST /api/import/validate
# =========================================================

@router.post("/validate")
async def validate_import_endpoint(

    import_type: str,

    file: UploadFile = File(...),

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    require_admin(current_user)


    if import_type not in [
        "products",
        "inventory",
        "customers",
        "sales"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Invalid import type."
        )


    result = await validate_import_file(

        db=db,

        company_id=current_user.company_id,

        import_type=import_type,

        file=file

    )


    return result


# =========================================================
# 3. PROCESS
# POST /api/import/process
# =========================================================

@router.post("/process")
async def process_import_endpoint(
    background_tasks: BackgroundTasks,
    import_id: int,
    import_type: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    if import_type not in [
        "products",
        "inventory",
        "customers",
        "sales"
    ]:
        raise HTTPException(
            status_code=400,
            detail="Invalid import type."
        )

    history = (
        db.query(ImportHistory)
        .filter(
            ImportHistory.id == import_id,
            ImportHistory.company_id == current_user.company_id
        )
        .first()
    )

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Import record not found."
        )

    if history.status in [
        "Processing"
    ]:
        raise HTTPException(
            status_code=400,
            detail="Import is already being processed."
        )

    file_content = await file.read()

    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    history.status = "Processing"

    db.commit()

    background_tasks.add_task(
        run_import_in_background,
        import_type,
        import_id,
        current_user.company_id,
        current_user.id,
        file_content,
        file.filename
    )

    return {
        "import_id": import_id,
        "status": "Processing",
        "message": "Import processing started in the background."
    }

# =========================================================
# 4. IMPORT HISTORY
# GET /api/import/history
# =========================================================

@router.get("/history")
def get_import_history(

    db: Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    )

):

    require_admin(current_user)


    history = (

        db.query(ImportHistory)

        .filter(
            ImportHistory.company_id ==
            current_user.company_id
        )

        .order_by(
            ImportHistory.created_at.desc()
        )

        .all()

    )


    return history

# =========================================================
# 5. IMPORT TEMPLATES
# GET /api/import/templates
# =========================================================

@router.get("/templates/{import_type}")
def download_import_template(
    import_type: str,
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    templates = {
        "products": [
            "Product Name",
            "SKU",
            "Category",
            "Unit Price",
            "Stock Quantity"
        ],
        "inventory": [
            "SKU",
            "Current Stock",
            "Reserved Stock",
            "Reorder Level"
        ],
        "customers": [
            "Name",
            "Email",
            "Phone"
        ],
        "sales": [
            "Invoice Number",
            "Customer",
            "Product",
            "Quantity",
            "Unit Price",
            "Sale Date",
            "Sales Channel",
            "Payment Method"
        ]
    }

    if import_type not in templates:
        raise HTTPException(
            status_code=400,
            detail="Invalid import type."
        )

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow(templates[import_type])

    output.seek(0)

    filename = f"{import_type}_import_template.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )

# =========================================================
# 6. IMPORT STATUS
# GET /api/import/status
# =========================================================

@router.get("/{import_id}/status")
def get_import_status(
    import_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    history = (
        db.query(ImportHistory)
        .filter(
            ImportHistory.id == import_id,
            ImportHistory.company_id == current_user.company_id
        )
        .first()
    )

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Import not found."
        )

    processed_records = (
        history.successful_records
        + history.failed_records
        + history.duplicate_records
    )

    if history.total_records > 0:
        progress = int(
            (processed_records / history.total_records) * 100
        )
    else:
        progress = 0

    if history.status in [
        "Completed",
        "Completed with Errors"
    ]:
        progress = 100

    return {
        "import_id": history.id,
        "status": history.status,
        "total_records": history.total_records,
        "successful_records": history.successful_records,
        "failed_records": history.failed_records,
        "duplicate_records": history.duplicate_records,
        "processed_records": processed_records,
        "progress": progress,
        "created_at": history.created_at,
        "completed_at": history.completed_at
    }

# =========================================================
# 7. IMPORT CANCEL
# GET /api/import/cancel
# =========================================================

@router.post("/{import_id}/cancel")
def cancel_import(
    import_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    history = (
        db.query(ImportHistory)
        .filter(
            ImportHistory.id == import_id,
            ImportHistory.company_id == current_user.company_id
        )
        .first()
    )

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Import not found."
        )

    if history.status != "Processing":
        raise HTTPException(
            status_code=400,
            detail="Only active imports can be cancelled."
        )

    history.status = "Cancelled"

    history.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(history)

    return {
        "import_id": history.id,
        "status": history.status,
        "message": "Import cancelled successfully."
    }


# =========================================================
# 8. IMPORT DETAILS
# GET /api/import/{import_id}
# =========================================================

@router.get("/{import_id}")
def get_import_details(

    import_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    )

):

    require_admin(current_user)


    history = (

        db.query(ImportHistory)

        .filter(

            ImportHistory.id ==
            import_id,

            ImportHistory.company_id ==
            current_user.company_id

        )

        .first()

    )


    if not history:

        raise HTTPException(
            status_code=404,
            detail="Import not found."
        )


    return history


# =========================================================
# 9. IMPORT ERRORS
# GET /api/import/{import_id}/errors
# =========================================================

@router.get("/{import_id}/errors")
def get_import_errors(

    import_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    )

):

    require_admin(current_user)


    history = (

        db.query(ImportHistory)

        .filter(

            ImportHistory.id ==
            import_id,

            ImportHistory.company_id ==
            current_user.company_id

        )

        .first()

    )


    if not history:

        raise HTTPException(
            status_code=404,
            detail="Import not found."
        )


    errors = (

        db.query(
            ImportErrorRecord
        )

        .filter(

            ImportErrorRecord.import_id ==
            import_id

        )

        .all()

    )


    return errors

# =========================================================
# 9. DOWNLOAD IMPORT ERROR CSV
# GET /api/import/{import_id}/errors/download
# =========================================================

@router.get("/{import_id}/errors/download")
def download_import_errors(
    import_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    require_admin(current_user)

    history = (
        db.query(ImportHistory)
        .filter(
            ImportHistory.id == import_id,
            ImportHistory.company_id == current_user.company_id
        )
        .first()
    )

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Import not found."
        )

    errors = (
        db.query(ImportErrorRecord)
        .filter(
            ImportErrorRecord.import_id == import_id
        )
        .order_by(
            ImportErrorRecord.row_number
        )
        .all()
    )

    if not errors:
        raise HTTPException(
            status_code=404,
            detail="No error records found for this import."
        )

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Row",
        "Type",
        "Message",
        "Status",
        "Record Data"
    ])

    for error_record in errors:

        writer.writerow([
            error_record.row_number,
            error_record.error_type,
            error_record.error_message,
            "Failed",
            error_record.row_data or ""
        ])

    output.seek(0)

    filename = (
        f"import_{import_id}_error_report.csv"
    )

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition":
                f'attachment; filename="{filename}"'
        }
    )