<?php

// Zip Code API example (provided as-is, for instruction only)
// by SmartyStreets: smartystreets.com
// POST example with PHP that doesn't use cURL.


// Your authentication ID/token (obtained in your SmartyStreets account)
$authId = urlencode("raw id here");
$authToken = urlencode("raw token here");

// Your input... remember that this endpoint can accept practically any combination
// of zip code, city, and/or state -- give what you can, we'll give back what we can.
// You can send up to 100 lookups per request.
$addresses = array(
    array(
        "city" => "Cupertino",
        "state" => "CA",
        "zipcode" => "95014"
    ),
    array(
        "zipcode" => "20500"
    ),
    array(
        "state" => "WY"
    ),
    array(
        "city" => "lebanon",
        "state" => "kansas"
    )
);


// This endpoint expects JSON
$post = json_encode($addresses);


// Create the stream context (a context is like metadata)
$context = stream_context_create(
    array(
        "http" => array(
        "method" => "POST",
        "header" => "Content-Type: application/json\r\n"
                    ."Content-Length: ".strlen($post)."\r\n",  
        "content" => $post
        )
    )
);


// Do the request
$page = file_get_contents("https://us-zipcode.api.smartystreets.com/lookup?auth-id={$authId}&auth-token={$authToken}", false, $context);


// Show results
echo "<pre>";
print_r(json_decode($page));
echo "</pre>";


?>
