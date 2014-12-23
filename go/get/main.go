package main

import (
	"fmt"
	"net/http"
	"net/url"
	"log"
	"encoding/json"
	"io/ioutil"
)

// The struct you use doesn't have to contain all the fields
// in order to decode properly. You can choose just the ones
// you need, like we've done here for an example.
type Address struct {
	Delivery_Line_1 string
	Last_Line string
	Metadata struct {
		Latitude float64
		Longitude float64
		RDI string
		County_Name string
	}
	Analysis struct {
		Active string
		DPV_Vacant string
	}
}

func main() {
	qs := url.Values{}
	
	// Fill in a secret key pair from your account; use raw, non-encoded values
	qs.Set("auth-id", 		"AUTH_ID")
	qs.Add("auth-token",	"RAW_AUTH_TOKEN")
	
	// Fill in the address data here
	qs.Add("street",	"1 infinite loop")
	qs.Add("city",		"cupertino")
	qs.Add("state",		"CA")
	qs.Add("zipcode",	"95014")

	// Build the GET request
	reqUrl := fmt.Sprintf("https://api.smartystreets.com/street-address?%s", qs.Encode())

	// Make the request
	resp, err := http.Get(reqUrl)

	if err != nil {
		log.Fatal(err)
	}

	// Read the response
	str, err := ioutil.ReadAll(resp.Body)
	resp.Body.Close()

	if err != nil {
		log.Fatal(err)
	}

	// Decode the JSON output
	var results []Address
	err = json.Unmarshal(str, &results)

	if err != nil {
		log.Fatal(err)
	}

	// Print/use the results
	fmt.Println(results[0].Delivery_Line_1)
	fmt.Println(results[0].Last_Line + "\n")
	fmt.Println("County: " + results[0].Metadata.County_Name)
	fmt.Println("RDI: " + results[0].Metadata.RDI)
	fmt.Printf("Coordinates: %f, %f\n", results[0].Metadata.Latitude, results[0].Metadata.Longitude)
	fmt.Println("Active: " + results[0].Analysis.Active)
	fmt.Println("Vacant: " + results[0].Analysis.DPV_Vacant)
}