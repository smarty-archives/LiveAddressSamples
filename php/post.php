<?php

// HTTP POST example (multiple input addresses) using curl:

$json_input = "[
    {
        street: '1 infinite loop',
        city: 'cupertino',
        state: 'ca',
        zipCode: '95014',
        candidates: '10',
    },
    {
        street: '1600 Pennsylvania ave',
        city: 'Washington',
        state: 'DC',
        zipCode: '20500',
        candidates: '10',
    }
]";

$ch = curl_init();

curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_setopt($ch, CURLOPT_VERBOSE, 0);
curl_setopt ($ch, CURLOPT_REFERER, "http://www.YOUR_AUTHORIZED_DOMAIN.com");
curl_setopt($ch, CURLOPT_URL, 'https://api.qualifiedaddress.com/street-address/?auth-token=YOUR_TOKEN_HERE');
curl_setopt($ch, CURLOPT_POSTFIELDS, $json_output);

$json_output = curl_exec($ch);

?>