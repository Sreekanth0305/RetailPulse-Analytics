import csv
import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from reportlab.lib.units import mm


# ---------------------------------------------------------
# Convert values to readable text
# ---------------------------------------------------------

def format_value(value):
    if value is None:
        return ""

    if hasattr(value, "strftime"):
        return value.strftime("%Y-%m-%d %H:%M:%S")

    return str(value)


# ---------------------------------------------------------
# CSV Export
# ---------------------------------------------------------

def export_report_csv(
    report_type,
    filters,
    items,
):
    """
    Creates a CSV file in memory.
    """

    output = io.StringIO()

    # If there is no data
    if not items:

        writer = csv.writer(output)

        writer.writerow([
            "Report Type",
            report_type
        ])

        writer.writerow([
            "Applied Filters",
            str(filters)
        ])

        writer.writerow([])

        writer.writerow([
            "No data found"
        ])

        return output.getvalue()

    # -----------------------------------------------------
    # Applied filter information
    # -----------------------------------------------------

    writer = csv.writer(output)

    writer.writerow([
        "Report Type",
        report_type
    ])

    writer.writerow([
        "Applied Filters",
        str(filters)
    ])

    writer.writerow([])

    # -----------------------------------------------------
    # Table headers
    # -----------------------------------------------------

    headers = list(items[0].keys())

    writer.writerow(headers)

    # -----------------------------------------------------
    # Data rows
    # -----------------------------------------------------

    for item in items:

        writer.writerow([
            format_value(item.get(header))
            for header in headers
        ])

    return output.getvalue()


# ---------------------------------------------------------
# PDF Export
# ---------------------------------------------------------

def export_report_pdf(
    report_type,
    filters,
    items,
):
    """
    Creates a PDF report in memory.
    """

    output = io.BytesIO()

    document = SimpleDocTemplate(
        output,
        pagesize=landscape(A4),
        rightMargin=10 * mm,
        leftMargin=10 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
    )

    styles = getSampleStyleSheet()

    elements = []

    # -----------------------------------------------------
    # Report title
    # -----------------------------------------------------

    title = Paragraph(
        f"<b>{report_type}</b>",
        styles["Title"],
    )

    elements.append(title)

    elements.append(
        Spacer(1, 8)
    )

    # -----------------------------------------------------
    # Applied filters
    # -----------------------------------------------------

    filter_text = "Applied Filters: "

    if filters:
        filter_text += ", ".join(
            f"{key}={value}"
            for key, value in filters.items()
        )
    else:
        filter_text += "None"

    elements.append(
        Paragraph(
            filter_text,
            styles["Normal"]
        )
    )

    elements.append(
        Spacer(1, 12)
    )

    # -----------------------------------------------------
    # Empty report
    # -----------------------------------------------------

    if not items:

        elements.append(
            Paragraph(
                "No data found for the selected filters.",
                styles["Normal"]
            )
        )

        document.build(elements)

        output.seek(0)

        return output.getvalue()

    # -----------------------------------------------------
    # Create table
    # -----------------------------------------------------

    headers = list(items[0].keys())

    table_data = [
        headers
    ]

    for item in items:

        row = [
            format_value(item.get(header))
            for header in headers
        ]

        table_data.append(row)

    table = Table(
        table_data,
        repeatRows=1,
    )

    # -----------------------------------------------------
    # Table styling
    # -----------------------------------------------------

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.grey,
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white,
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold",
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                7,
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey,
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP",
            ),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [
                    colors.white,
                    colors.lightgrey,
                ],
            ),
        ])
    )

    elements.append(table)

    # -----------------------------------------------------
    # Build PDF
    # -----------------------------------------------------

    document.build(elements)

    output.seek(0)

    return output.getvalue()