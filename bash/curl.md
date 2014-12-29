curl -v 

# cURL examples

## HTTP GET Method

    curl 'https://api.smartystreets.com/street-address?auth-id=<auth-id>&auth-token=<auth-token>&street=3214+n+university+ave&city=provo&state=ut&zipcode=84604&candidates=10'

## HTTP POST (JSON payload)

    curl 'https://api.smartystreets.com/street-address?auth-id=<auth-id>&auth-token=<auth-token>' -H --data-binary '[{"street":"3214 n university Ave","city":"provo","state":"ut","zipcode":"84604","candidates":10}]'

## HTTP POST (XML payload)

    curl 'https://api.smartystreets.com/street-address?auth-id=<auth-id>&auth-token=<auth-token>' -H 'Content-Type: application/xml' --data-binary '<?xml version="1.0" encoding="utf-8"?><request><address><street>3214 n university ave</street><city>provo</city><state>ut</state><zipcode>84604</zipcode><candidates>10</candidates></address></request>'

## HTTP 'Accept' Header (can be used for any GET or POST)

    curl 'https://api.smartystreets.com/street-address?auth-id=<auth-id>&auth-token=<auth-token>&street=3214+n+university+ave&city=provo&state=ut&zipcode=84604&candidates=10' -H 'Accept: application/xml'

## HTTP Custom Headers (can be used for any GET or POST)

    curl 'https://api.smartystreets.com/street-address?auth-id=<auth-id>&auth-token=<auth-token>&street=3214+n+university+ave&city=provo&state=ut&zipcode=84604&candidates=10' -H 'X-Standardize-Only: true'

    curl 'https://api.smartystreets.com/street-address?auth-id=<auth-id>&auth-token=<auth-token>&street=3214+n+university+ave&city=provo&state=ut&zipcode=84604&candidates=10' -H 'X-Include-Invalid: true'
