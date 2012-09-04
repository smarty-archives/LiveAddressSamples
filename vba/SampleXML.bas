Sub SampleXMLRequest()
    Dim strUrl As String    ' Our URL which will include the authentication info
    Dim strReq As String    ' The body of the POST request
    
    ' Make sure to reference the "Microsoft XML, v6.0" library (Tools -> References).
    ' You can use an older version, too, just be sure to change the number in the next line.
    Dim xmlHttp As New MSXML2.XMLHTTP60
    
    ' Don't forget to replace this with your auth token and ID, url-encoded, and without
    ' the < > characters. Find this in your account under "Key Management" -> "Id/Key pairs"
    strUrl = "https://api.qualifiedaddress.com/street-address/?auth-id=<YOUR ID HERE>&auth-token=<YOUR TOKEN HERE>"
    
    ' Body of the POST request
    strReq = "<?xml version=""1.0"" encoding=""utf-8""?>" & _
                "<request>" & _
                "<address>" & _
                "   <street>1 infinite loop</street>" & _
                "   <city>cupertino</city>" & _
                "   <state>ca</state>" & _
                "   <zipcode></zipcode>" & _
                "   <candidates>5</candidates>" & _
                "</address>" & _
                "</request>"
    
    With xmlHttp
        .Open "POST", strUrl, False                     ' Prepare POST request
        .setRequestHeader "Content-Type", "text/xml"    ' Sending XML ...
        .setRequestHeader "Accept", "text/xml"          ' ... expect XML in return.
        .send strReq                                    ' Send request body
        Debug.Print .responseText                       ' Print results to immediate window
    End With
End Sub