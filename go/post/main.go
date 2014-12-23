package main

import (
	"fmt"
	"net/http"
	"net/url"
	"log"
	"encoding/json"
	"io/ioutil"
	"strings"
)

type InputAddress struct {
	Street string
	City string
	State string
	Zipcode string
	Candidates int
}

// The struct you use for output doesn't have to contain all the fields
// in order to decode properly. You can choose just the ones you need,
// like we've done here for an example.
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
	body := make([]InputAddress, 2)
	
	// Fill in a secret key pair from your account; use raw, non-encoded values
	qs.Set("auth-id", 		"AUTH_ID")
	qs.Add("auth-token",	"RAW_AUTH_TOKEN")

	// Fill in the address data here
	body[0] = InputAddress { "1 infinite loop", "", "", "95014", 5 }
	body[1] = InputAddress { "1 Rosedale St", "Baltimore", "MD", "", 10 }


	// Build the request URL
	reqUrl := fmt.Sprintf("https://api.smartystreets.com/street-address/?%s", qs.Encode())

	// Convert the input to a []byte of JSON, then fill a stream with it to POST it
	jsonBytes, _ := json.Marshal(body)
	buf := strings.NewReader(string(jsonBytes))
	resp, err := http.Post(reqUrl, "application/json", buf)

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
	for i := range results {
		fmt.Println(results[i].Delivery_Line_1)
		fmt.Println(results[i].Last_Line + "\n")
		fmt.Println("County:\t" + results[i].Metadata.County_Name)
		fmt.Println("RDI:\t" + results[i].Metadata.RDI)
		fmt.Printf("Coordinates: %f, %f\n", results[i].Metadata.Latitude, results[i].Metadata.Longitude)
		fmt.Println("Active: " + results[i].Analysis.Active)
		fmt.Println("Vacant: " + results[i].Analysis.DPV_Vacant + "\n\n")
	}
}