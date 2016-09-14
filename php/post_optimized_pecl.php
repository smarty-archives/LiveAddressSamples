<?php

// US Street API API sample using PHP's pecl_http libraries.
// Requires that the PECL extension(s) are installed.
// This sample is optimized for performing large requests in a loop
// very quickly.

// In a real scenario, you would load 100 addresses into a single request,
// and call the setBody() function inside your loop so each request has
// 100 new addresses in it. In this example, we repeat the same 2 addresses
// over and over to demonstrate the performance benefit of keeping your
// TCP connection alive between requests. By minimizing the HTTP overhead
// in this manner, you nearly double your speed.


// Your authentication ID/token (obtained in your SmartyStreets account)
$authId = urlencode("raw id here");
$authToken = urlencode("raw token here");

// The REST endpoint
$url = "https://us-street.api.smartystreets.com/street-address/?auth-id={$authId}&auth-token={$authToken}";

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

// The US Street API expects JSON input.
$post = json_encode($addresses);

// Prepare the POST request, and set the body of it.
$request = new HTTPRequest($url, HTTP_METH_POST);
$request->setBody($post);

// Simple statistic variables
$max = 0;
$min = 99999999;
$sum = 0;
$requests = 100;

echo "<pre>";

// Do the requests, and time it
for ($i = 0; $i < $requests; $i ++)
{
    $start = microtime(true);
    $request->send();       // In a real case, you'd call setBody() before this, to do the next 100 addresses
    $end = microtime(true);
    $ms = ($end - $start) * 1000;

    // For the record, you can get the response with:
    // $response = $request->getResponseBody();
    // Then json_decode() to use the values in PHP.

    $max = $ms > $max ? $ms : $max;
    $min = $ms < $min ? $ms : $min;
    $sum += $ms;
    echo $ms."<br>";
}

// Show the cumulative results
echo "<br><b>MAX:</b> {$max}ms<br>";
echo "<b>MIN:</b> {$min}ms<br>";
echo "<b>AVG:</b> ".($sum / $requests)."ms<br>";
echo "<b>TOTAL TIME:</b> ".($sum/1000)." seconds";
echo "</pre>";
?>