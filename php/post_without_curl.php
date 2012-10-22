<?php

// LiveAddress API example (provided as-is, for instruction only)
// by SmartyStreets: smartystreets.com


// POST example with PHP without using cURL.
// Instead of cURL, we open a connection the API as a stream.


// Your authentication ID/token (obtained in your SmartyStreets account)
$authId = urlencode("raw id here");
$authToken = urlencode("raw token here");

// Your input to the API...
$addresses = array(
    array(
        "street" => "1 infinite loop",
        "city" => "cupertino",
        "state" => "ca",
        "zipcode" => "95014",
        "candidates" => 10
    ),
    array(
        "street" => "1600 pennsylvania Ave.",
        "zipcode" => "20500",
        "candidates" => 3
    )
);


// LiveAddress API expects JSON input by default, but you could send XML
// if you set the Content-Type header to "text/xml".
$post = json_encode($addresses);


// Create the stream context (like metadata)
$context = stream_context_create(
    array(
        "http" => array(
            "method" => "POST",
            "header" => "Content-Type: application/x-www-form-urlencoded\r\n"
                        ."Content-Length: ".strlen($post)."\r\n",  
            "content" => $post
        )
    )
);


// Do the request, and we'll time it just for kicks
$start = microtime(true);
$page = file_get_contents("https://api.qualifiedaddress.com/street-address/?auth-id={$authId}&auth-token={$authToken}", false, $context);
$end = microtime(true);


// Show results
echo "<pre>";
echo "<b>Round-trip time (including external latency):</b> ";
echo (($end - $start) * 1000)." ms<br><br><br>";    // Show result in milliseconds, not microseconds
print_r(json_decode($page));
echo "</pre>";


?>
