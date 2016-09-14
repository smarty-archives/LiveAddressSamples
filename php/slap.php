<?php

/**
 * US Street API: freeform address example
 *
 * http://smartystreets.com/docs/us-street-api
 *
 * This example shows how to validate an address that has
 * not yet been split into separate components (street, city, etc).
 * Simply put the whole address into the "street" field.
 *
 */

// Put your own auth ID/token values here (obtained from your account)
$authId = urlencode("raw ID here");
$authToken = urlencode("raw token here");

$address = urlencode("3785 s las vegs av. los vegas, nevada"); // Address input (one line, not split into components)
$req = "https://us-street.api.smartystreets.com/street-address/?street={$address}&auth-id={$authId}&auth-token={$authToken}";
$result = json_decode(file_get_contents($req));

echo "<pre>";
print_r($result);
echo "</pre>";

?>