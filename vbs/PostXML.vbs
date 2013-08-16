xml = "<?xml version=""1.0"" encoding=""utf-8""?><request><address><street>1 infinite loop</street><street2></street2><secondary></secondary><city>cupertino</city><state>california</state><zipcode></zipcode><candidates>10</candidates></address></request>"

strUrl = "https://api.smartystreets.com/street-address?auth-id=URL_ENCODED_AUTH_ID&auth-token=URL_ENCODED_AUTH_TOKEN"

Set xmlHttp = CreateObject("MSXML2.XMLHTTP")

With xmlHttp
 .Open "POST", strUrl, False
 .setRequestHeader "Content-Type", "text/xml"
 .setRequestHeader "Accept", "text/xml"
 .setRequestHeader "Content-Length", Len(xml)
 .send xml
 AddressResponse = .responseText
 
 WScript.StdOut.Write(AddressResponse)
End With