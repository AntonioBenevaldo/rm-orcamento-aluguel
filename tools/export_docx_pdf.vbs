Option Explicit

If WScript.Arguments.Count <> 2 Then
  WScript.Echo "Usage: cscript export_docx_pdf.vbs input.docx output.pdf"
  WScript.Quit 2
End If

Dim inputPath, outputPath, wordApp, document
inputPath = WScript.Arguments(0)
outputPath = WScript.Arguments(1)

On Error Resume Next
Set wordApp = CreateObject("Word.Application")
If Err.Number <> 0 Then
  WScript.Echo "Could not start Word: " & Err.Description
  WScript.Quit 3
End If

wordApp.Visible = False
wordApp.DisplayAlerts = 0
Set document = wordApp.Documents.Open(inputPath, False, True)
If Err.Number <> 0 Then
  WScript.Echo "Could not open document: " & Err.Description
  wordApp.Quit
  WScript.Quit 4
End If

' 17 = wdExportFormatPDF
document.ExportAsFixedFormat outputPath, 17
If Err.Number <> 0 Then
  WScript.Echo "Could not export PDF: " & Err.Description
  document.Close False
  wordApp.Quit
  WScript.Quit 5
End If

WScript.Echo document.ComputeStatistics(2)
document.Close False
wordApp.Quit
WScript.Quit 0
