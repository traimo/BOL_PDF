from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Frame
from reportlab.lib import colors

def create_pdf(output_filename):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)

    # Create a list to hold flowables (content elements)
    story = []

    # Create a table data
    data = [
        ["Name", "Age", "Occupation"],
        ["John Doe", "30", "Engineer"],
        ["Jane Smith", "25", "Designer"],
        ["Michael Johnson", "40", "Manager"],
    ]

    # Create a table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])

    # Create a table and apply the style
    table = Table(data)
    table.setStyle(table_style)

    # Create a frame to hold the table
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        showBoundary=1  # Display frame boundary for demonstration purposes
    )

    # Add the table to the frame
    frame.addFromList([table], doc)

    # Add the frame to the story
    story.append(frame)

    # Build the PDF
    doc.build(story)

if __name__ == "__main__":
    output_filename = "c:\\temp\\vics_bill_of_lading.pdf"
    create_pdf(output_filename)
    print(f"PDF created: {output_filename}")
