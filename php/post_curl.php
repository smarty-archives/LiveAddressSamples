<?php


// POST example with PHP using cURL.

// In this example, we're assuming the input address(es)
// have been POSTed to this script from a local webpage
// as JSON. This is really useful when you have a web interface
// and want to batch-submit your address. LiveAddress API can
// support up to 100 addresses per request, but browser
// Same-Origin policies limit requests to external domains
// to be in JSONP format, which only supports GET, and thus
// only one address. In other words, proxying a request
// through your own server like this is a great way to
// overcome that restriction.



// Your authentication ID/token (obtained in your SmartyStreets account)
$authId = urlencode("raw ID here");
$authToken = urlencode("raw token here");

// Simulated input received from the webpage's POST request
$json_input = "[
    {
        \"street\": \"1 infinite loop\",
        \"city\": \"cupertino\",
        \"state\": \"ca\",
        \"zipCode\": \"95014\",
        \"candidates\": 10
    },
    {
        \"street\": \"1600 Pennsylvania ave\",
        \"city\": \"Washington\",
        \"state\": \"DC\",
        \"zipCode\": \"20500\",
        \"candidates\": 10
    }
]";



// Initialize cURL
$ch = curl_init();

// Configure the cURL command
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_HEADER, 0);
//curl_setopt($ch, CURLOPT_HTTPHEADER, array('x-standardize-only: true'));    // Enable this line if you want to only standardize addresses that are "good enough"
curl_setopt($ch, CURLOPT_VERBOSE, 0);
// Use the next line if you prefer to use your Javascript API token rather than your REST API token.
//curl_setopt($ch, CURLOPT_REFERER, "http://YOUR-AUTHORIZED-DOMAIN-HERE");
curl_setopt($ch, CURLOPT_URL, "https://api.smartystreets.com/street-address/?auth-id={$authId}&auth-token={$authToken}");
curl_setopt($ch, CURLOPT_POSTFIELDS, $json_input);

// Output comes back as a JSON string.
$json_output = curl_exec($ch);

// Show results
echo "<pre>";
print_r(json_decode($json_output));
echo "</pre>";


?>
