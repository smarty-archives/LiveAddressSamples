# Output goes to results.json file:
curl -o -v results.json "https://api.smartystreets.com/street-address?street=579+N+600+W&ssecondary=Apt+3city=Provo&state=UT&zipcode=84601&auth-id=<your-auth-id-here>&auth-token=<your-urlencoded-auth-token-here>"

# Output to stdout:
curl -v "https://api.smartystreets.com/street-address?street=579+N+600+W&ssecondary=Apt+3city=Provo&state=UT&zipcode=84601&auth-id=auth-id=<your-auth-id-here>&auth-token=<your-urlencoded-auth-token-here>"