' US Street API API example with VBA using JSON
'
' REQUIRES:
' -----------------------------------------------------------------------------------------
' VB-JSON (to parse the JSON)
'   http://www.ediy.co.nz/vbjson-json-parser-library-in-vb6-xidc55680.html
'
' INSTRUCTIONS:
' -----------------------------------------------------------------------------------------
' Import:
'  JSON.bas
'  cJSONScript.cls
'  cStringBuilder.cls
'
' Then add references to:
'   Microsoft XML, v6.0
'   Microsoft Scripting Runtime
'   Microsoft ActiveX Data Object 2.8 Library
'
' Then plug in your (raw) auth-id and auth-token from your account below.
'
Public Sub Main()
    Dim HTTP As Object
    Set HTTP = CreateObject("MSXML2.ServerXMLHTTP")
    Dim request As String, id As String, token As String
    Dim jsonResult As Object
    Dim street1 As String, street2 As String, city As String, state As String, zip As String
    
    street1 = "158 S. Reed"
    street2 = ""
    city = "Lakewd"
    state = "Colorado"
    zip = ""
    
    ' Secret Key Pair from your account
    id = "AUTH-ID"
    token = "AUTH-TOKEN"
    
    ' Create and GET the address verification request
    request = "https://us-street.api.smartystreets.com/street-address?" & _
                "street=" & URLEncode(street1) & _
                "&street2=" & URLEncode(street2) & _
                "&city=" & URLEncode(city) & _
                "&state=" & URLEncode(state) & _
                "&zipcode=" & URLEncode(zip) & _
                "&auth-id=" & URLEncode(id) & _
                "&auth-token=" & URLEncode(token)
    
    ' Change false to true to do async requests
    With HTTP
        .Open "GET", request, False
        .Send ""
        Debug.Print .responseText   ' This lets you see the full result
        Set jsonResult = JSON.parse(.responseText)
    End With
    
    ' Examples of using the results:
    Debug.Print jsonResult.Item(1).Item("delivery_line_1")
    Debug.Print jsonResult.Item(1).Item("last_line")
    Debug.Print jsonResult.Item(1).Item("metadata").Item("latitude") & ", " & jsonResult.Item(1).Item("metadata").Item("longitude")
    
End Sub



' Thanks to http://stackoverflow.com/a/218199/1048862
' for this function. It URL-encodes a string, making it
' safe to include in a URL. (Does not support UTF-8/Unicode)
' See that Stack Overflow post for another one for UTF-8.
Public Function URLEncode(StringVal As String, Optional SpaceAsPlus As Boolean = False) As String
    Dim StringLen As Long: StringLen = Len(StringVal)
    
    If StringLen > 0 Then
        ReDim result(StringLen) As String
    Dim i As Long, CharCode As Integer
    Dim Char As String, Space As String
    
    If SpaceAsPlus Then Space = "+" Else Space = "%20"
    
    For i = 1 To StringLen
        Char = Mid$(StringVal, i, 1)
        CharCode = Asc(Char)
        Select Case CharCode
            Case 97 To 122, 65 To 90, 48 To 57, 45, 46, 95, 126
              result(i) = Char
            Case 32
              result(i) = Space
            Case 0 To 15
              result(i) = "%0" & Hex(CharCode)
            Case Else
              result(i) = "%" & Hex(CharCode)
        End Select
    Next i
        URLEncode = Join(result, "")
    End If
End Function