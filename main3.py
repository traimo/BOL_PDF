from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Frame, PageTemplate
from reportlab.lib.units import inch

# Create a list of data for the table
data = [
    ["Name", "Age", "Occupation"],
    ["John Doe", "30", "Engineer"],
    ["Jane Smith", "25", "Designer"],
    ["Michael Johnson", "40", "Manager"],
]

# Create a document and set its attributes
doc = SimpleDocTemplate("c:\\temp\\vics_bill_of_lading.pdf", pagesize=landscape(letter))

# Define a frame for the table
frame = Frame(inch, inch, doc.width - 2 * inch, doc.height - 2 * inch, id="normal")

# Define a page template with the frame
page_template = PageTemplate(id="table_template", frames=[frame])

# Build the flowables list
flowables = []

# Create a table and apply styles
table = Table(data)
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
    ("GRID", (0, 0), (-1, -1), 1, colors.black),
]))

# Add the table to the flowables list
flowables.append(table)

# Build the document using the flowables and page template
doc.addPageTemplates([page_template])
doc.build(flowables)
