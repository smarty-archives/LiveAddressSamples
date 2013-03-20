<?php

// Customize this (get ID/token values in your SmartyStreets account)
$authId = urlencode("raw ID here");
$authToken = urlencode("raw token here");

// Address input
$input1 = urlencode("3785 s las vegs av.");
$input2 = urlencode("los vegas,");
$input3 = urlencode("nevada");

// Build the URL
$req = "https://api.smartystreets.com/street-address/?street={$input1}&city={$input2}&state={$input3}&auth-id={$authId}&auth-token={$authToken}";

// GET request and turn into associative array
$result = json_decode(file_get_contents($req),true);

echo "<pre>";
print_r($result);
echo "</pre>";

?>
