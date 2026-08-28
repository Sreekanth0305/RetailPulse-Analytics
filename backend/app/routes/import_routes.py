from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException
)

from sqlalchemy.orm import Session

from app.config.database import get_db

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

    import_id: int,

    import_type: str,

    file: UploadFile = File(...),

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    require_admin(current_user)


    if import_type not in [
        "products",
        "customers",
        "sales"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Invalid import type."
        )


    result = await process_import(

        db=db,

        company_id=current_user.company_id,

        user_id=current_user.id,

        import_id=import_id,

        import_type=import_type,

        file=file

    )


    return result


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
# 5. IMPORT DETAILS
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
# 6. IMPORT ERRORS
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