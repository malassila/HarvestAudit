from jinja2 import Template
from win32com.client import Dispatch
import win32print
import time
import traceback
from datetime import datetime


# DYMO LABEL PRINTING ********************************************************************************

def print_dymo_label(printer_name, qty, sku, description, initials):
    dymo_printer = Dispatch("Dymo.DymoAddIn")
    dymo_printer.SelectPrinter(printer_name)
    dymo_printer.Open("C:\\HarvestAudit\\labels\\Dymo-3x1-1QR-Standard.label")
    
    printer_label = Dispatch("Dymo.DymoLabels")
    
    # print(printer_label.GetObjectNames(False))
    
    printer_label.SetField("SKU", sku)
    formatted_description = format_dymo_description(description)
    printer_label.SetField("Description", formatted_description)
    printer_label.SetField("QR", sku)
    printer_label.SetField("Initials", initials)

    dymo_printer.SetGraphicsAndBarcodePrintMode(False)
    
    dymo_printer.StartPrintJob()
    dymo_printer.Print(qty, False)

    dymo_printer.EndPrintJob()

def format_dymo_description(description):
    description = description.split()
    new_description = ""
    line_len = 0
    
    for word in description:
        word_len = len(word)
        if line_len + word_len + 1 > 30:
            new_description += "\n"
            line_len = 0
        else:
            if new_description != "":
                new_description += " "
            line_len += 1
        new_description += word
        line_len += word_len
        
    return new_description


# ZEBRA LABEL PRINTING ********************************************************************************

def print_zebra_label(printer_name, qty, sku, description, initials):
    try:

        formatted_description = format_zebra_description(description)

        date = datetime.now().strftime("%m/%d/%y")
        # zpl_path = r"C:\\HarvestAudit\\labels\\Zebra-3x1-1QR-Standard.zpl"
        print(f"Printing ZPL label: {printer_name}\n\tSKU: {sku}, Description: {description}, Initials: {initials}")
        
        zpl_template = """
        CT~~CD,~CC^~CT~
        ^XA
        ~TA000
        ~JSN
        ^LT0
        ^MNW
        ^MTD
        ^PON
        ^PMN
        ^LH0,0
        ^JMA
        ^PR6,6
        ~SD15
        ^JUS
        ^LRN
        ^CI27
        ^PA0,1,1,0
        ^XZ
        ^XA
        ^MMT
        ^PW609
        ^LL203
        ^LS0
        ^FT0,42^A0N,37,38^FB608,1,9,C^FH\^CI28^FD{sku}^FS^CI27
        ^FPH,3^FT0,149^A0N,24,23^FB494,1,6,C^FH\^CI28^FD{description3}^FS^CI27
        ^FPH,5^FT19,190^A0N,23,23^FH\^CI28^FD{initials}^FS^CI27
        ^SLS,1
        ^FT0,187^A0N,20,20^FB486,1,5,R
        ^FC%,{{,#
        ^FH\^CI28^FDPrinted on: {date}^FS^CI27
        ^FT491,171^BQN,2,4
        ^FH\^FDLA,{sku}^FS
        ^FPH,3^FT0,79^A0N,24,23^FB494,1,6,C^FH\^CI28^FD{description1}^FS^CI27
        ^FPH,3^FT0,114^A0N,24,23^FB494,1,6,C^FH\^CI28^FD{description2}^FS^CI27
        ^PQ1,0,1,Y
        ^XZ
        """
        
        zpl_data = zpl_template.format(sku=sku, description1=formatted_description[0], description2=formatted_description[1], description3=formatted_description[2], initials=initials, date=date)

        printer_handle = win32print.OpenPrinter(printer_name)

        printer_name = win32print.GetPrinter(printer_handle, 9)
        
        while qty > 0:
            win32print.StartDocPrinter(printer_handle, 1, (zpl_data, None, "raw"))
            
            win32print.WritePrinter(printer_handle, zpl_data.encode('utf-8'))

            win32print.EndDocPrinter(printer_handle)
            qty -= 1
        
        # win32print.StartDocPrinter(printer_handle, 1, (zpl_data, None, "raw"))
        
        # win32print.WritePrinter(printer_handle, zpl_data.encode('utf-8'))

        # win32print.EndDocPrinter(printer_handle)

        win32print.ClosePrinter(printer_handle)

    except Exception as e:
        print("Error printing ZPL label: " + str(e))
        print(traceback.format_exc())
    

def format_zebra_description(description):
    if len(description) <= 30:
        return ['', description, '']
    
    input_words = description.split()
    lines = ['', '', '']
    current_line = 0
    
    for word in input_words:
        if current_line >= 2:
            lines[current_line] += ' ' + word
        elif len(lines[current_line]) + len(word) + 1 <= 30:
            if lines[current_line]:
                lines[current_line] += ' ' + word
            else:
                lines[current_line] = word
        else:
            current_line += 1
            if current_line >= 2:
                lines[current_line] = word
            else:
                lines[current_line] += word
                
        if len(lines[2]) > 30:
            lines[2] = lines[2][:30]
            
    return lines