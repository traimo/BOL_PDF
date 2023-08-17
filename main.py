from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Frame, FrameBreak, PageTemplate, Paragraph, BaseDocTemplate, NextPageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from functools import partial
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT


class vics_bol(BaseDocTemplate):
    def __init__(self, filename, bol_json, **kwargs):
        super().__init__(filename, page_size=letter, _pageBreakQuick=0, **kwargs)
        self.bol_json = bol_json
        self.flow = []
        self.page_templates = []

        self.page_width = (self.width + self.leftMargin * 2)
        self.page_height = (self.height + self.bottomMargin * 2)

        self.header_content = self.build_header()
        self.footer_content = self.build_footer()

        # Setting up the frames, frames are use for dynamic content not fixed page elements
        p1_order_frame = Frame(65, 475, 450, 150, id='OrderInfo1')
        px_order_frame = Frame(2, 350, 600, 450, id='OrderInfo2')

        #p1_carrier_frame = Frame(65, 275, 450, 150, id='CarrierInfo1')
        #px_carrier_frame = Frame(2, 150, 600, 450, id='CarrierInfo2')

        # Creating the page templates
        first_page = PageTemplate(id='FirstPage', frames=[p1_order_frame], onPage=self.on_first_page)
        later_pages = PageTemplate(id='LaterPages', frames=[px_order_frame], onPage=self.on_later_page)
        self.addPageTemplates([first_page, later_pages])

        # Tell Reportlab to use the other template on the later pages,
        # by the default the first template that was added is used for the first page.
        self.flow = [NextPageTemplate(['*', 'LaterPages'])]

        order_table = self.build_customer_info_table_from_json()
        self.flow.append(order_table)

        #carrier_table = self.build_carrier_info_table_from_json()
        #self.flow.append(carrier_table)

        self.build(self.flow)

    def build_customer_info_table_from_json(self):
        table_data = []
        i = 0
        for itm in self.bol_json["OrderInfo"]["Items"]:
            indx = 0
            i = i + 1
            row_data = []
            if i == 1:
                table_data.append(["OrderNo", "Pkgs", "Weight", "AddInfo"])
            for field_name in itm:
                row_data.append(itm[field_name])
                indx = indx + 1
            table_data.append(row_data)
        table = Table(table_data, colWidths=[150, 100, 100, 225], repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        return table

    def build_carrier_info_table_from_json(self):
        table_data = []
        i = 0
        for itm in self.bol_json["CarrierInfo"]["Items"]:
            indx = 0
            i = i + 1
            row_data = []
            if i == 1:
                table_data.append(["HUQty", "HUType", "PkgQty", "PkgType", "Weight", "HM", "Desc", "NMFC", "Class"])
            for field_name in itm:
                row_data.append(itm[field_name])
                indx = indx + 1
            table_data.append(row_data)
        table = Table(table_data, colWidths=[50, 50, 50, 50, 60, 25, 165, 75, 50], repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        return table

    # def create_vics_bill_of_lading(self, pdf_filename, bill_of_lading_data):
    #     # Create a canvas object and specify the PDF file
    #     #c = canvas.Canvas(pdf_filename, pagesize=landscape(letter))
    #     doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    #
    #     header_content = self.build_header()
    #     footer_content = self.build_footer()
    #
    #     shipfrom_frame = self.draw_ship_from(doc, bill_of_lading_data)
    #     shipto_frame = self.draw_ship_to(doc, bill_of_lading_data)
    #     #bol_frame = self.draw_bol_number(doc, bill_of_lading_data)
    #     order_frame = self.draw_customer_order_info(doc, bill_of_lading_data)
    #
    #     page_template = PageTemplate(id='page1', frames=[shipfrom_frame, shipto_frame, order_frame],
    #                                  onPage=partial(self.header_and_footer, header_content=header_content, footer_content=self.footer_content))
    #     doc.addPageTemplates([page_template])
    #
    #     doc.build(self.flow, onFirstPage=self.on_first_page, onLaterPages=self.on_later_page)

    def build_header(self):
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Heading1_CENTER',
                                  parent=styles['Heading1'],
                                  fontName='Helvetica',
                                  wordWrap='LTR',
                                  alignment=TA_CENTER,
                                  fontSize=18,
                                  leading=13,
                                  textColor=colors.black,
                                  borderPadding=0,
                                  leftIndent=0,
                                  rightIndent=0,
                                  spaceAfter=0,
                                  spaceBefore=0,
                                  splitLongWords=True,
                                  spaceShrinkage=0.05,
                                  ))
        header_content = Paragraph("Bill of Lading", styles['Heading1_CENTER'])
        return header_content

    def build_footer(self):
        styles = getSampleStyleSheet()
        footer_content = Paragraph("This is a footer. It goes on every page.  ", styles['Normal'])
        return footer_content

    def header(self, canvas, doc, content):
        canvas.saveState()
        w, h = content.wrap(doc.width, doc.topMargin)
        content.drawOn(canvas, doc.leftMargin, doc.height + doc.bottomMargin + doc.topMargin - h)
        canvas.restoreState()

    def footer(self, canvas, doc, content):
        canvas.saveState()
        w, h = content.wrap(doc.width, doc.bottomMargin)
        content.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    def header_and_footer(self, canvas, doc, header_content, footer_content):
        self.header(canvas, doc, header_content)
        self.footer(canvas, doc, footer_content)

    def on_first_page(self, canvas, doc):
        canvas.saveState()

        canvas.drawString(250, 825, "Bill of Lading")

        #Draw ShipFrom
        table = self.draw_ship_from(self.bol_json)
        table.wrapOn(canvas, 0, 0)
        table.drawOn(canvas, 2, 710)

        # Draw ShipTo
        table = self.draw_ship_to(self.bol_json)
        table.wrapOn(canvas, 0, 0)
        table.drawOn(canvas, 2, 625)

        #Draw BOL Data
        table = self.draw_bol_number(self.bol_json)
        table.wrapOn(canvas, 0, 0)
        table.drawOn(canvas, 355, 764)


        canvas.restoreState()

    def on_later_page(self, canvas, doc):
        canvas.saveState()

        canvas.drawString(225, 825, "Bill of Lading (Supplemental)")

        canvas.restoreState()

    # def convert_dict_to_list(self, data_dict):
    #     table_data = [['Key', 'Value']]
    #     for key, value in data_dict.items():
    #         table_data.append([key, value])
    #     return table_data

    def draw_ship_from(self, bol_data):
        # Create a table for the bill of lading data
        table_data = [
            ["", bol_data["ShipFrom"]["HeaderTitle"]],
            ["Name:", bol_data["ShipFrom"]["Name"]],
            ["Address:", bol_data["ShipFrom"]["Address"]],
            ["City/State/Zip:", bol_data["ShipFrom"]["City/State/Zip"]],
            ["SID#:", bol_data["ShipFrom"]["SID#"]],
            # ... add more rows as needed
        ]
        table = Table(table_data, colWidths=[100, 250])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        return table


    def draw_ship_to(self, bol_data):
        # Create a table for the bill of lading data
        table_data = [
            ["", bol_data["ShipTo"]["HeaderTitle"]],
            ["Name:", bol_data["ShipTo"]["Name"]],
            ["Address:", bol_data["ShipTo"]["Address"]],
            ["City/State/Zip:", bol_data["ShipTo"]["City/State/Zip"]],
            # ... add more rows as needed
        ]
        table = Table(table_data, colWidths=[100, 250])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        return table

    def draw_bol_number(self, bol_data):
        # Create a table for the bill of lading data
        table_data = [
            ["", bol_data["BOL"]["HeaderTitle"]],
            ["Bill of Lading Number:", bol_data["BOL"]["BOLNumber"]],
        ]
        table = Table(table_data, colWidths=[110, 125])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        return table

    # def draw_customer_order_info(self, doc, bol_data):
    #     # Create a table for the bill of lading data
    #     table_data = []
    #     row_data = []
    #     i = 0
    #
    #     for itm in bol_data["OrderInfo"]["Items"]:
    #         indx = 0
    #         i = i + 1
    #         row_data = []
    #         if i == 1:
    #             table_data.append(["OrderNo", "Pkgs", "Weight", "AddInfo"])
    #         for field_name in itm:
    #             row_data.append(itm[field_name])
    #             indx = indx + 1
    #         table_data.append(row_data)
    #             #table_data.append(itm["OrderNo"], itm["Pkgs"], itm["Weight"], itm["AddInfo"])
    #     #table_data = convert_dict_to_list(bol_data["OrderInfo"]["Items"])
    #
    #     # table_data = [
    #     #     ["", bol_data["OrderInfo"]["HeaderTitle"]],
    #     #     ["Name:", bol_data["ShipTo"]["OrderNo"]],
    #     #     ["Address:", bol_data["ShipTo"]["Pkgs"]],
    #     #     ["City/State/Zip:", bol_data["ShipTo"]["City/State/Zip"]],
    #     #     # ... add more rows as needed
    #     # ]
    #
    #     table = Table(table_data, colWidths=[150, 100, 100, 250], repeatRows=1)
    #     table.setStyle(TableStyle([
    #         ('BACKGROUND', (0, 0), (-1, 0), colors.black),
    #         ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    #         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    #         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    #         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    #         ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    #         ('GRID', (0, 0), (-1, -1), 1, colors.black)
    #     ]))
    #
    #     self.flow.append(table)
    #     frame = Frame(2, 410, 600, 150, showBoundary=0, bottomPadding=0, topPadding=0, leftPadding=0, rightPadding=0)
    #
    #     return frame
    #
    # def draw_carrier_info(self, doc, bol_data):
    #     # Create a table for the bill of lading data
    #     table_data = []
    #     row_data = []
    #     i = 0
    #
    #     for itm in bol_data["CarrierInfo"]["Items"]:
    #         indx = 0
    #         i = i + 1
    #         row_data = []
    #         if i == 1:
    #             table_data.append(["HUQty", "HUType", "PkgQty", "PkgType", "Weight", "HM", "Desc", "NMFC", "Class"])
    #         for field_name in itm:
    #             row_data.append(itm[field_name])
    #             indx = indx + 1
    #         table_data.append(row_data)
    #
    #     table = Table(table_data, colWidths=[25, 25, 25, 25, 25, 10, 100, 25, 25], repeatRows=1)
    #     table.setStyle(TableStyle([
    #         ('BACKGROUND', (0, 0), (-1, 0), colors.black),
    #         ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    #         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    #         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    #         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    #         ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    #         ('GRID', (0, 0), (-1, -1), 1, colors.black)
    #     ]))
    #
    #     self.flow.append(table)
    #     frame = Frame(2, 410, 600, 150, showBoundary=0, bottomPadding=0, topPadding=0, leftPadding=0, rightPadding=0)
    #
    #     return frame



if __name__ == "__main__":
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
                    "Weight": "8.1",
                    "AddInfo": "some text 2"
                },
                {
                    "OrderNo": "9987",
                    "Pkgs": "1",
                    "Weight": "11.4",
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
                    "Weight": "5.0",
                    "AddInfo": "some text 2"
                },
            ]
        },
        "CarrierInfo":{
            "HeaderTitle": "",
            "Items": [
                {
                    "HUQty": "1",
                    "HUType": "PLTS",
                    "PkgQty": "48",
                    "PkgType": "CTNS",
                    "Weight": "364 LBS",
                    "HM": "",
                    "Desc": "Sport Accessories",
                    "NMFC": "13431433",
                    "Class": "70"
                },
                {
                    "HUQty": "2",
                    "HUType": "PLTS",
                    "PkgQty": "48",
                    "PkgType": "CTNS",
                    "Weight": "425 LBS",
                    "HM": "",
                    "Desc": "Other stuff",
                    "NMFC": "234523454",
                    "Class": "85"
                }
            ]
        }
    }
    #flow = []
    #page_templates = []
    pdf_filename = "c:\\temp\\vics_bill_of_lading.pdf"
    vics_bol(pdf_filename, bill_of_lading_data)
    #create_vics_bill_of_lading(pdf_filename, bill_of_lading_data)
    # print(f"VICS Bill of Lading PDF created: {pdf_filename}")
