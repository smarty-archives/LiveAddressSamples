# cURL examples

## HTTP GET Method

    curl 'https://us-street.api.smartystreets.com/street-address?auth-id=<auth-id>&auth-token=<auth-token>&street=3214+n+university+ave&city=provo&state=ut&zipcode=84604&candidates=10'

## HTTP POST (JSON payload)

    curl 'https://us-street.api.smartystreets.com/street-address?auth-id=<auth-id>&auth-token=<auth-token>' -H --data-binary '[{"street":"3214 n university Ave","city":"provo","state":"ut","zipcode":"84604","candidates":10}]'

## Output to file

    curl -o results.json "https://us-street.api.smartystreets.com/street-address?street=579+N+600+W&ssecondary=Apt+3city=Provo&state=UT&zipcode=84601&auth-id=<your-auth-id-here>&auth-token=<your-urlencoded-auth-token-here>"
