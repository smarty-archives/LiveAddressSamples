<?php

/**
 * LiveAddress API; freeform address example
 * "SLAP" (Single-Line Address Parsing)
 *
 * By SmartyStreets
 * http://smartystreets.com/products/liveaddress-api
 *
 * This example shows how to validate an address that has
 * not yet been split into separate components (street, city, etc).
 * Simply put the whole address into the "street" field
 * and LiveAddress will do the rest for you.
 *
 */


// Put your own auth ID/token values here (obtained from your account)
$authId = urlencode("raw ID here");
$authToken = urlencode("raw token here");

// Address input (one line, not split into components)
$address = urlencode("3785 s las vegs av. los vegas, nevada");

// Build the URL
$req = "https://api.smartystreets.com/street-address/?street={$address}&auth-id={$authId}&auth-token={$authToken}";

// GET request and turn into associative array
$result = json_decode(file_get_contents($req));

echo "<pre>";
print_r($result);
echo "</pre>";

?>