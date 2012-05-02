<?php

/**
 * LiveAddress API Example
 * "SLAP" (Single-Line Address Processing)
 *
 * by SmartyStreets
 * http://smartystreets.com/products/liveaddress-api
 *
 * This example shows how to validate an address that has
 * not been split into separate components (street, city, state, etc).
 * It generates permutations according to this algorithm: 
 * 
 * http://smartystreets.com/answers/questions/318/can-i-verify-a-freeform-address-with-your-service/319
 *
 * All the permutations are submitted as a batch to the
 * LiveAddress service, which does all the heavy lifting.
 * You may get several results back; usually the first one
 * will be the most correct. 
 *
 */

 
// Put your REST auth token here (raw format)
$authToken = urlencode("YOUR-RAW-AUTHENTICATION-TOKEN-HERE");

// The single-line address to process
$addr = "3214 north university ave. #409 provo, ut 84604";

$delim = ' ';		// Delimiter around which permutations are made
$batch = array();	// This becomes our JSON object

// Create permutations of the address for each space in it
for ($pivot = strripos($addr, $delim); $pivot !== false;
		$pivot = strripos($addr, $delim, -strlen($addr) + $pivot - 1))
{
	$permutation = array(
		"street" => substr($addr, 0, $pivot),
		"lastline" => substr($addr, $pivot + 1)
	);
	
	array_push($batch, $permutation);
}
$json = json_encode($batch);


// Initialize cURL
$ch = curl_init();

// Configure the cURL command
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_setopt($ch, CURLOPT_VERBOSE, 0);
// Use the next line if you prefer to use your Javascript API token rather than your REST API token.
//curl_setopt($ch, CURLOPT_REFERER, "http://YOUR-AUTHORIZED-DOMAIN-HERE");
curl_setopt($ch, CURLOPT_URL, "https://api.qualifiedaddress.com/street-address/?auth-token={$authToken}");
curl_setopt($ch, CURLOPT_POSTFIELDS, $json);

// Output comes back as a JSON string; convert it to PHP object
$results = json_decode(curl_exec($ch));

// Show result. The first of the permutations will likely generate
// the most correct match, so we look at index 0 for our answer.
echo "<pre>
{$results[0]->delivery_line_1}
{$results[0]->last_line}
</pre>";

?>