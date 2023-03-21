from jinja2 import Template
from win32com.client import Dispatch

def print_dymo_label(printer_name, qty, sku, description, initials):
    dymo_printer = Dispatch("Dymo.DymoAddIn")
    dymo_printer.SelectPrinter(printer_name)
    dymo_printer.Open("C:\\HarvestAudit\\labels\\3x1.label")
    
    printer_label = Dispatch("Dymo.DymoLabels")
    
    print(printer_label.GetObjectNames(False))
    
    printer_label.SetField("SKU", sku)
    formatted_description = format_description(description)
    printer_label.SetField("Description", formatted_description)
    printer_label.SetField("QR", sku)
    printer_label.SetField("Initials", initials)

    dymo_printer.SetGraphicsAndBarcodePrintMode(False)
    
    dymo_printer.StartPrintJob()
    dymo_printer.Print(qty, False)

    dymo_printer.EndPrintJob()
    
def format_description(description):
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