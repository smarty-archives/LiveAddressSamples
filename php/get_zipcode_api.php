<?php

// Customize this (get ID/token values in your SmartyStreets account)
$authId = urlencode("raw ID here");
$authToken = urlencode("raw token here");

// Input. You can fill out any combination of the 3 values (except city only) and leave any blank
$city = urlencode("");
$state = urlencode("");
$zipcode = urlencode("90023");

// Build the URL
$req = "https://api.smartystreets.com/zipcode/?city={$city}&state={$state}&zipcode={$zipcode}&auth-id={$authId}&auth-token={$authToken}";

// GET request and turn into associative array
$result = json_decode(file_get_contents($req));

echo "<pre>";
print_r($result);
echo "</pre>";

?>