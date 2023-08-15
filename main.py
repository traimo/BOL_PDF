from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet

# Sample data for the bill of lading
bill_of_lading_data = {
    "ShipFrom": {
        "HeaderTitle": "Ship From",
        "Name": "ShipERP, LLC",
        "Address": "5000 Airport Plaza Dr. STE 230",
        "City/State/Zip": "Long Beach, CA 90810",
        "SID#": ""
    },
    "ShipTo": {
        "HeaderTitle": "Ship To",
        "Name": "ABC Company",
        "Address": "123 Main St.",
        "City/State/Zip": "Lynn, MA 01904"
    },
    "BOL": {
        "HeaderTitle": "",
        "BOLNumber": "99278793",
        "BarCode": "99278793"
    },
    "OrderInfo": {
        "HeaderTitle": "Customer Order Info",
        "Items": [
            {
                "OrderNo": "9987",
                "Pkgs": "2",
                "Weight": "5.6",
                "AddInfo": "some text"
            },
            {
                "OrderNo": "9987",
                "Pkgs": "1",
                "Weight": "15.4",
                "AddInfo": "some text 2"
            },
            {
                "OrderNo": "9987",
                "Pkgs": "1",
                "Weight": "15.4",
                "AddInfo": "some text 2"
            },
            {
                "OrderNo": "9987",
                "Pkgs": "1",
                "Weight": "15.4",
                "AddInfo": "some text 2"
            },
            {
                "OrderNo": "9987",
                "Pkgs": "1",
                "Weight": "15.4",
                "AddInfo": "some text 2"
            },
            {
                "OrderNo": "9987",
                "Pkgs": "1",
                "Weight": "15.4",
                "AddInfo": "some text 2"
            },
            {
                "OrderNo": "9987",
                "Pkgs": "1",
                "Weight": "15.4",
                "AddInfo": "some text 2"
            },
            {
                "OrderNo": "9987",
                "Pkgs": "1",
                "Weight": "15.4",
                "AddInfo": "some text 2"
            },
            {
                "OrderNo": "9987",
                "Pkgs": "1",
                "Weight": "15.4",
                "AddInfo": "some text 2"
            },
            {
                "OrderNo": "9987",
                "Pkgs": "1",
                "Weight": "15.4",
                "AddInfo": "some text 2"
            },
            {
                "OrderNo": "9987",
                "Pkgs": "1",
                "Weight": "15.4",
                "AddInfo": "some text 2"
            },
            {
                "OrderNo": "9987",
                "Pkgs": "1",
                "Weight": "15.4",
                "AddInfo": "some text 2"
            },
            {
                "OrderNo": "9987",
                "Pkgs": "1",
                "Weight": "15.4",
                "AddInfo": "some text 2"
            },
            {
                "OrderNo": "9987",
                "Pkgs": "1",
                "Weight": "15.4",
                "AddInfo": "some text 2"
            },
            {
                "OrderNo": "9987",
                "Pkgs": "1",
                "Weight": "15.4",
                "AddInfo": "some text 2"
            },
            {
                "OrderNo": "9987",
                "Pkgs": "1",
                "Weight": "15.4",
                "AddInfo": "some text 2"
            },
            {
                "OrderNo": "9987",
                "Pkgs": "1",
                "Weight": "15.4",
                "AddInfo": "some text 2"
            },
            {
                "OrderNo": "9987",
                "Pkgs": "1",
                "Weight": "15.4",
                "AddInfo": "some text 2"
            },
            {
                "OrderNo": "9987",
                "Pkgs": "1",
                "Weight": "15.4",
                "AddInfo": "some text 2"
            },
        ]
    }
}
flow = []
page_templates = []


def create_vics_bill_of_lading(pdf_filename, bill_of_lading_data):
    # Create a canvas object and specify the PDF file
    #c = canvas.Canvas(pdf_filename, pagesize=landscape(letter))
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)


    shipfrom_frame = draw_ship_from(doc, bill_of_lading_data)
    shipto_frame = draw_ship_to(doc, bill_of_lading_data)
    #bol_frame = draw_bol_number(doc, bill_of_lading_data)
    order_frame = draw_customer_order_info(doc, bill_of_lading_data)


    page_template = PageTemplate(id='page1', frames=[shipfrom_frame, shipto_frame, order_frame])

    # Save the canvas to the PDF file
    #c.save()
    doc.addPageTemplates([page_template])
    doc.build(flow)

def convert_dict_to_list(data_dict):
    table_data = [['Key', 'Value']]
    for key, value in data_dict.items():
        table_data.append([key, value])
    return table_data

def draw_ship_from(doc, bol_data):
    # Create a table for the bill of lading data
    table_data = [
        ["", bol_data["ShipFrom"]["HeaderTitle"]],
        ["Name:", bol_data["ShipFrom"]["Name"]],
        ["Address:", bol_data["ShipFrom"]["Address"]],
        ["City/State/Zip:", bol_data["ShipFrom"]["City/State/Zip"]],
        ["SID#:", bol_data["ShipFrom"]["SID#"]],
        # ... add more rows as needed
    ]
    table = Table(table_data, colWidths=[100, 328])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    flow.append(table)
    frame = Frame(2, 650, 435, 100, showBoundary=0, bottomPadding=0, topPadding=0, leftPadding=0, rightPadding=0)
    #frame.addFromList(flow, c)

    #page_template = PageTemplate(id="page1", frames=[frame])
    #page_templates.append(page_template)
    return frame

    #doc.addPageTemplates([page_template])

def draw_ship_to(doc, bol_data):
    # Create a table for the bill of lading data
    table_data = [
        ["", bol_data["ShipTo"]["HeaderTitle"]],
        ["Name:", bol_data["ShipTo"]["Name"]],
        ["Address:", bol_data["ShipTo"]["Address"]],
        ["City/State/Zip:", bol_data["ShipTo"]["City/State/Zip"]],
        # ... add more rows as needed
    ]
    table = Table(table_data, colWidths=[100, 328])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    flow.append(table)
    frame = Frame(2, 549, 435, 100, showBoundary=0, bottomPadding=0, topPadding=0, leftPadding=0, rightPadding=0)
    #page_template = PageTemplate(id="page1", frames=[frame])
    #page_templates.append(page_template)
    return frame

def draw_bol_number(doc, bol_data):
    # Create a table for the bill of lading data
    table_data = [
        ["", bol_data["BOL"]["HeaderTitle"]],
        ["Bill of Lading Number:", bol_data["BOL"]["BOLNumber"]],
    ]
    table = Table(table_data, colWidths=[110, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    flow.append(table)
    frame = Frame(500, 600, 350, 100, showBoundary=1, bottomPadding=0, topPadding=0, leftPadding=0, rightPadding=0)
    return frame

def draw_customer_order_info(doc, bol_data):
    # Create a table for the bill of lading data
    table_data = []
    row_data = []
    i = 0

    for itm in bol_data["OrderInfo"]["Items"]:
        indx = 0
        i = i + 1
        row_data = []
        if i == 1:
            table_data.append(["OrderNo", "Pkgs", "Weight", "AddInfo"])
        for field_name in itm:
            row_data.append(itm[field_name])
            indx = indx + 1
        table_data.append(row_data)
            #table_data.append(itm["OrderNo"], itm["Pkgs"], itm["Weight"], itm["AddInfo"])
    #table_data = convert_dict_to_list(bol_data["OrderInfo"]["Items"])

    # table_data = [
    #     ["", bol_data["OrderInfo"]["HeaderTitle"]],
    #     ["Name:", bol_data["ShipTo"]["OrderNo"]],
    #     ["Address:", bol_data["ShipTo"]["Pkgs"]],
    #     ["City/State/Zip:", bol_data["ShipTo"]["City/State/Zip"]],
    #     # ... add more rows as needed
    # ]

    table = Table(table_data, colWidths=[150, 100, 100, 250])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    #flow.append(table)

    frame = Frame(2, 410, 600, 150, showBoundary=0, bottomPadding=0, topPadding=0, leftPadding=0, rightPadding=0)
    # Define a page template with the frame
    #page_template = PageTemplate(id="page1", frames=[frame])

    #frame.addFromList([table], doc)
    flow.append(table)

    # Build the document using the flowables and page template
    #doc.addPageTemplates([page_template])
    #page_templates.append(page_template)

    return frame



if __name__ == "__main__":
    pdf_filename = "c:\\temp\\vics_bill_of_lading.pdf"
    create_vics_bill_of_lading(pdf_filename, bill_of_lading_data)
    # print(f"VICS Bill of Lading PDF created: {pdf_filename}")
