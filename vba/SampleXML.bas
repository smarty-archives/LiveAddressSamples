Sub SampleXMLRequest()
    Dim strUrl As String    ' Our URL which will include the authentication info
    Dim strReq As String    ' The body of the POST request
    
    ' Make sure to reference the "Microsoft XML, v6.0" library (Tools -> References).
    ' You can use an older version, too, just be sure to change the number in this next line.
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
    
    ' Perform the request
    With xmlHttp
        .Open "POST", strUrl, False                     ' Prepare POST request
        .setRequestHeader "Content-Type", "text/xml"    ' Sending XML ...
        .setRequestHeader "Accept", "text/xml"          ' ... expect XML in return.
        .send strReq                                    ' Send request body
        Debug.Print .responseText & vbCrLf              ' Print results to immediate window - for demo purposes
    End With
    
    
    ' The request has been saved into xmlHttp.responseText and is
    ' now ready to be parsed. Remember that fields in our XML response may
    ' change or be added to later, so make sure your method of parsing accepts that.
    ' Google and Stack Overflow are replete with helpful examples.
    
    Dim xmlDoc As MSXML2.DOMDocument
    Set xmlDoc = New MSXML2.DOMDocument
    If Not xmlDoc.LoadXML(xmlHttp.responseText) Then
        Err.Raise xmlDoc.parseError.ErrorCode, , xmlDoc.parseError.reason
    End If
    
    
    ' According to the schema (http://smartystreets.com/kb/liveaddress-api/parsing-the-response#xml),
    ' <candidates> is a top-level node with each <candidate> below it. Let's obtain each one.
    Dim candidates, candidate, components, metadata, analysis As MSXML2.IXMLDOMNode
    Set candidates = xmlDoc.DocumentElement
    
    ' Loop through each candidate...
    
    For Each candidate In candidates.ChildNodes
        ' Example of how to obtain the value of child nodes of this <candidate> node:
        Debug.Print candidate.SelectSingleNode("delivery_line_1").nodeTypedValue
        Debug.Print candidate.SelectSingleNode("last_line").nodeTypedValue
        
        ' Example of how to obtain the grandchildren nodes:
        Set components = candidate.SelectSingleNode("components")
        Set metadata = candidate.SelectSingleNode("metadata")
        Set analysis = candidate.SelectSingleNode("analysis")
        
        ' Then access the actual grandchildren node values like this:
        Debug.Print metadata.SelectSingleNode("latitude").nodeTypedValue & ", " & _
                        metadata.SelectSingleNode("longitude").nodeTypedValue & vbCrLf
    Next

End Sub