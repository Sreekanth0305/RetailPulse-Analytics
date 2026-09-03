from sqlalchemy.orm import Session
from sqlalchemy import or_

import csv
import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)

from app.models.audit_log import AuditLog
from app.models.user import User
import json
from datetime import datetime, timedelta

def create_audit_log(
    db: Session,
    company_id: int,
    user_id: int,
    action: str,
    resource_type: str = "",
    resource_id: int | None = None,
    description: str = "",
    ip_address: str = "",
    user_agent: str = "",
    status: str = "SUCCESS",
    before_values: dict | None = None,
    after_values: dict | None = None
):
    """
    Create an audit log entry.

    company_id and user_id come from the authenticated
    backend context. They should not be trusted from
    frontend input.
    """

    log = AuditLog(
        company_id=company_id,
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent,
        status=status,
        before_values=(
            json.dumps(before_values, default=str)
            if before_values is not None
            else None
        ),
        after_values=(
            json.dumps(after_values, default=str)
            if after_values is not None
            else None
        )
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log


def get_audit_logs(
    db: Session,
    company_id: int,
    user_id: int | None = None,
    action: str | None = None,
    resource_type: str | None = None,
    status: str | None = None,
    search: str | None = None,
    date_from=None,
    date_to=None,
    sort_order: str = "desc",
    page: int = 1,
    limit: int = 25
):
    """
    Get audit logs belonging only to the authenticated
    user's company.

    Supports:
    - User filtering
    - Action filtering
    - Resource filtering
    - Status filtering
    - Search
    - Date range
    - Sorting
    - Pagination
    """

    # -----------------------------------------------------
    # Base query
    # -----------------------------------------------------

    query = (
        db.query(AuditLog, User.name)
        .join(
            User,
            AuditLog.user_id == User.id
        )
        .filter(
            AuditLog.company_id == company_id
        )
    )

    # -----------------------------------------------------
    # User filter
    # -----------------------------------------------------

    if user_id is not None:
        query = query.filter(
            AuditLog.user_id == user_id
        )

    # -----------------------------------------------------
    # Action filter
    # -----------------------------------------------------

    if action:
        query = query.filter(
            AuditLog.action == action
        )

    # -----------------------------------------------------
    # Resource type filter
    # -----------------------------------------------------

    if resource_type:
        query = query.filter(
            AuditLog.resource_type == resource_type
        )

    # -----------------------------------------------------
    # Status filter
    # -----------------------------------------------------

    if status:
        query = query.filter(
            AuditLog.status == status
        )

    # -----------------------------------------------------
    # Search
    # -----------------------------------------------------

    if search:

        search_value = f"%{search}%"
    
        search_conditions = [
            User.name.ilike(search_value),
            AuditLog.action.ilike(search_value),
            AuditLog.resource_type.ilike(search_value),
            AuditLog.description.ilike(search_value)
        ]
    
        try:
    
            resource_id_value = int(search)
    
            search_conditions.append(
                AuditLog.resource_id == resource_id_value
            )
    
        except ValueError:
            pass
    
        query = query.filter(
            or_(*search_conditions)
        )

    # -----------------------------------------------------
    # Date range
    # -----------------------------------------------------
    
    if date_from:
        start_date = datetime.strptime(
            date_from,
            "%Y-%m-%d"
        )
    
        query = query.filter(
            AuditLog.created_at >= start_date
        )
    
    if date_to:
        end_date = datetime.strptime(
            date_to,
            "%Y-%m-%d"
        ) + timedelta(days=1)
    
        query = query.filter(
            AuditLog.created_at < end_date
        )

    # -----------------------------------------------------
    # Sorting
    # -----------------------------------------------------

    if sort_order.lower() == "asc":

        query = query.order_by(
            AuditLog.created_at.asc()
        )

    else:

        query = query.order_by(
            AuditLog.created_at.desc()
        )

    # -----------------------------------------------------
    # Pagination validation
    # -----------------------------------------------------

    if page < 1:
        page = 1

    if limit < 1:
        limit = 25

    if limit > 100:
        limit = 100

    # -----------------------------------------------------
    # Total records
    # -----------------------------------------------------

    total = query.count()

    # -----------------------------------------------------
    # Calculate offset
    # -----------------------------------------------------

    offset = (page - 1) * limit

    # -----------------------------------------------------
    # Fetch requested page
    # -----------------------------------------------------

    logs = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    # -----------------------------------------------------
    # Convert database result
    # -----------------------------------------------------

    result = []

    for log, user_name in logs:

        result.append({

            "id": log.id,

            "user_id": log.user_id,

            "user_name": user_name,

            "action": log.action,

            "resource_type": log.resource_type,

            "resource_id": log.resource_id,

            "description": log.description,

            "ip_address": log.ip_address,

            "user_agent": log.user_agent,

            "status": log.status,

            "before_values": log.before_values,

            "after_values": log.after_values,

            "created_at": log.created_at

        })

    # -----------------------------------------------------
    # Total pages
    # -----------------------------------------------------

    total_pages = (
        (total + limit - 1) // limit
        if total > 0
        else 0
    )

    return {

        "items": result,

        "total": total,

        "page": page,

        "limit": limit,

        "total_pages": total_pages

    }


def get_audit_log_by_id(
    db: Session,
    company_id: int,
    audit_log_id: int
):
    """
    Get one audit log.

    The company_id filter prevents an Admin from
    accessing another company's audit record.
    """

    result = (
        db.query(AuditLog, User.name)
        .join(
            User,
            AuditLog.user_id == User.id
        )
        .filter(
            AuditLog.id == audit_log_id,
            AuditLog.company_id == company_id
        )
        .first()
    )

    if not result:
        return None

    log, user_name = result

    before_values = None
    after_values = None
    
    if log.before_values:
        try:
            before_values = json.loads(log.before_values)
        except (json.JSONDecodeError, TypeError):
            before_values = None
    
    if log.after_values:
        try:
            after_values = json.loads(log.after_values)
        except (json.JSONDecodeError, TypeError):
            after_values = None
    
    return {
        "id": log.id,
        "company_id": log.company_id,
        "user_id": log.user_id,
        "user_name": user_name,
        "action": log.action,
        "resource_type": log.resource_type,
        "resource_id": log.resource_id,
        "description": log.description,
        "ip_address": log.ip_address,
        "user_agent": log.user_agent,
        "status": log.status,
        "before_values": before_values,
        "after_values": after_values,
        "created_at": log.created_at
    }

def get_audit_logs_for_export(
    db: Session,
    company_id: int,
    user_id: int | None = None,
    action: str | None = None,
    resource_type: str | None = None,
    status: str | None = None,
    search: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    sort_order: str = "desc"
):
    query = (
        db.query(AuditLog, User.name)
        .join(User, AuditLog.user_id == User.id)
        .filter(AuditLog.company_id == company_id)
    )

    if user_id:
        query = query.filter(AuditLog.user_id == user_id)

    if action:
        query = query.filter(AuditLog.action == action)

    if resource_type:
        query = query.filter(
            AuditLog.resource_type == resource_type
        )

    if status:
        query = query.filter(AuditLog.status == status)

    if search:

        search_value = f"%{search}%"

        search_conditions = [
            User.name.ilike(search_value),
            AuditLog.action.ilike(search_value),
            AuditLog.resource_type.ilike(search_value),
            AuditLog.description.ilike(search_value)
        ]

        if search.isdigit():

            search_conditions.append(
                AuditLog.resource_id == int(search)
            )

        from sqlalchemy import or_

        query = query.filter(or_(*search_conditions))

    if date_from:

        start_date = datetime.strptime(
            date_from,
            "%Y-%m-%d"
        )

        query = query.filter(
            AuditLog.created_at >= start_date
        )

    if date_to:

        end_date = datetime.strptime(
            date_to,
            "%Y-%m-%d"
        ) + timedelta(days=1)

        query = query.filter(
            AuditLog.created_at < end_date
        )

    if sort_order.lower() == "asc":

        query = query.order_by(
            AuditLog.created_at.asc()
        )

    else:

        query = query.order_by(
            AuditLog.created_at.desc()
        )

    return query.all()


def export_audit_logs_csv(
    db: Session,
    company_id: int,
    user_id: int | None = None,
    action: str | None = None,
    resource_type: str | None = None,
    status: str | None = None,
    search: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    sort_order: str = "desc"
):

    logs = get_audit_logs_for_export(
        db=db,
        company_id=company_id,
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        status=status,
        search=search,
        date_from=date_from,
        date_to=date_to,
        sort_order=sort_order
    )

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Timestamp",
        "User",
        "Action",
        "Resource",
        "Resource ID",
        "Description",
        "IP Address",
        "Browser",
        "Status"
    ])

    for log, user_name in logs:

        writer.writerow([
            log.created_at.strftime("%Y-%m-%d %H:%M:%S")
            if log.created_at
            else "",

            user_name or "",

            log.action or "",

            log.resource_type or "",

            log.resource_id
            if log.resource_id is not None
            else "",

            log.description or "",

            log.ip_address or "",

            log.user_agent or "",

            log.status or ""
        ])

    return output.getvalue()


def export_audit_logs_pdf(
    db: Session,
    company_id: int,
    user_id: int | None = None,
    action: str | None = None,
    resource_type: str | None = None,
    status: str | None = None,
    search: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    sort_order: str = "desc"
):

    logs = get_audit_logs_for_export(
        db=db,
        company_id=company_id,
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        status=status,
        search=search,
        date_from=date_from,
        date_to=date_to,
        sort_order=sort_order
    )

    output = io.BytesIO()

    document = SimpleDocTemplate(
        output,
        pagesize=landscape(A4),
        rightMargin=20,
        leftMargin=20,
        topMargin=25,
        bottomMargin=25
    )

    styles = getSampleStyleSheet()

    title = Paragraph(
        "RetailPulse Analytics - Audit Logs",
        styles["Title"]
    )

    table_data = [[
        "Timestamp",
        "User",
        "Action",
        "Resource",
        "Resource ID",
        "Description",
        "IP Address",
        "Browser",
        "Status"
    ]]

    for log, user_name in logs:

        timestamp = (
            log.created_at.strftime("%Y-%m-%d %H:%M:%S")
            if log.created_at
            else "-"
        )

        table_data.append([
            timestamp,
            user_name or "-",
            log.action or "-",
            log.resource_type or "-",
            str(log.resource_id)
            if log.resource_id is not None
            else "-",
            log.description or "-",
            log.ip_address or "-",
            log.user_agent or "-",
            log.status or "-"
        ])

    table = Table(
        table_data,
        repeatRows=1
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#1976d2")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [
                    colors.white,
                    colors.HexColor("#f5f5f5")
                ]
            )
        ])
    )

    document.build([
        title,
        table
    ])

    output.seek(0)

    return output

def clear_audit_logs(
    db: Session,
    company_id: int,
    user_id: int
):
    deleted_count = (
        db.query(AuditLog)
        .filter(
            AuditLog.company_id == company_id
        )
        .delete(
            synchronize_session=False
        )
    )

    db.commit()

    clear_log = AuditLog(
        company_id=company_id,
        user_id=user_id,
        action="CLEAR_LOGS",
        resource_type="AuditLog",
        resource_id=None,
        description=f"Cleared {deleted_count} audit log(s)",
        before_values=None,
        after_values=None,
        ip_address=None,
        user_agent=None,
        status="Success"
    )

    db.add(clear_log)

    db.commit()
    db.refresh(clear_log)

    return {
        "message": "Audit logs cleared successfully",
        "deleted_count": deleted_count
    }