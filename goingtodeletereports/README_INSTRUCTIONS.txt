================================================================================
WORD DOCUMENT AUTOMATION - QUICK INSTRUCTIONS
================================================================================

This folder contains an automated script to fill Word document templates with
your RTS Fan Control project data.

GENERATED DOCUMENTS:
--------------------
1. FILLED_Project_Synopsis.docx     - Project overview and specifications (8-10 pages)
2. FILLED_Project_Report.docx       - Complete technical report (25-30 pages)

HOW TO USE:
-----------
1. Run the script:
   > python fill_word_documents.py

2. Open the generated FILLED_*.docx files

3. Search for red text "[INSERT IMAGE: ...]" - These are placeholders for screenshots

4. Insert your screenshots at each placeholder:
   - Delete the red placeholder text
   - Insert → Pictures → Select your screenshot
   - Add caption if needed

RECOMMENDED SCREENSHOTS TO PREPARE:
-----------------------------------
□ System Block Diagram              (draw in PowerPoint or similar)
□ Circuit Schematic                 (export from KiCad: File → Plot → PDF/PNG)
□ Control Algorithm Flowchart       (draw in PowerPoint or similar)
□ Temperature vs Fan Speed Graph    (plot from reports/simulation_data.csv in Excel)
□ Linearity Analysis (R² plot)      (Excel trendline with R² value)
□ UART Output Sample                (screenshot from reports/uart_output.txt)
□ Renode Simulation Running         (screenshot of Renode terminal)
□ Compiled Firmware Info            (PlatformIO build output)

TABLES INCLUDED (AUTO-GENERATED):
----------------------------------
✓ System Specifications
✓ Pin Configuration
✓ Bill of Materials (BOM)
✓ Test Results Data
✓ Power Supply Specifications

AFTER COMPLETION:
-----------------
- Review both documents for completeness
- Check all tables for accuracy
- Verify all images are inserted
- Generate Table of Contents in Word (References → Table of Contents)
- Print or export to PDF for submission
- DELETE THIS ENTIRE FOLDER if no longer needed

CUSTOMIZATION:
--------------
Edit these values in fill_word_documents.py if needed:
- PROJECT_DATA["student_name"]     (Line 34)
- PROJECT_DATA["guide"]            (Line 38)
- PROJECT_DATA["department"]       (Line 39)
- PROJECT_DATA["college"]          (Line 40)

NOTE: The script will auto-install python-docx library if not present.

================================================================================
Questions? Check the main project README.md in the root folder.
================================================================================
