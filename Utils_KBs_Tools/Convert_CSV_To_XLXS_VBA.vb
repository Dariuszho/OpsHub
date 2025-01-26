' Open a blank workbook in Excel.
' Press Alt + F11 to open the VBA editor
' Go to Insert > Module
' Replace C:\path\to\csv\files\ and C:\path\to\xlsx\files\ with your actual folder paths.
' Press F5 to run the macro

Sub ConvertCSVtoXLSX()
    Dim csvFolder As String
    Dim xlsxFolder As String
    Dim csvFile As String
    Dim wb As Workbook

    ' Set the folder paths
    csvFolder = "C:\path\to\csv\files\" ' Replace with your CSV folder path
    xlsxFolder = "C:\path\to\xlsx\files\" ' Replace with your XLSX folder path

    ' Create output directory if it doesn't exist
    If Dir(xlsxFolder, vbDirectory) = "" Then
        MkDir xlsxFolder
    End If

    ' Loop through all CSV files in the folder
    csvFile = Dir(csvFolder & "*.csv")
    Do While csvFile <> ""
        ' Open the CSV file
        Set wb = Workbooks.Open(csvFolder & csvFile)
        
        ' Save as XLSX
        wb.SaveAs xlsxFolder & Replace(csvFile, ".csv", ".xlsx"), FileFormat:=xlOpenXMLWorkbook
        wb.Close False
        
        ' Get the next CSV file
        csvFile = Dir
    Loop

    MsgBox "All files have been converted!", vbInformation
End Sub
