using System;
using System.Collections.Generic;
using System.Drawing.Printing;
using System.IO;

namespace ZPLPrinter {
    class Program {
        static void Main(string[] args) {
            string zplPath = args[0];
            string printerName = args[1];
            string sku = args[2];
            string description = args[3];
            string initials = args[4];

            // Read the ZPL file
            string zplContent = File.ReadAllText(zplPath);

            // Replace the placeholders in the ZPL file with the specified values
            Dictionary<string, string> replacements = new Dictionary<string, string> {
                { "sku1", sku },
                { "sku2", sku },
                { "description", description },
                { "initials", initials }
            };
            foreach (var pair in replacements) {
                zplContent = zplContent.Replace("^^" + pair.Key + "^^", pair.Value);
            }

            // Send the ZPL file to the printer
            PrintDocument pd = new PrintDocument();
            pd.PrinterSettings.PrinterName = printerName;
            pd.PrinterSettings.PrintFileName = null;
            pd.PrintPage += (sender, e) => {
                e.Graphics.DrawString(zplContent, new System.Drawing.Font("Courier New", 8), System.Drawing.Brushes.Black, 0, 0);
                e.HasMorePages = false;
            };
            pd.Print();
        }
    }
}