// freeform-list is a command line tool for processing lists of addresses
// in text files. It assumes that each line in the file is an address and
// submits the line in it's entirety to the SmartyStreets street API.
// It requires that you provide an auth-id/auth-token key pair and an
// active subscription. Head over to smartystreets.com to get started.
//
// This script is provided as-is and is not guaranteed to accomplish your
// purposes. You may use it as-is or modify it for said purposes, but
// that's not something we can do for you. Enjoy!
package main

///////////////////////////////////////////////////////////////////////////////

import (
	"bufio"
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"os"
	"runtime"
	"strings"
	"sync"
)

///////////////////////////////////////////////////////////////////////////////

var ( // config: TODO: would a config file be easier to use?
	authID     string
	authToken  string
	inputPath  string
	outputPath string
	uri        string

	maxConcurrentBatches int
)

func init() {
	runtime.GOMAXPROCS(runtime.NumCPU())

	log.SetFlags(log.Ltime | log.Lshortfile)

	flag.StringVar(&authID, "auth-id", "", "The auth-id for use in HTTP requests.")
	flag.StringVar(&authToken, "auth-token", "", "The auth-token for use in HTTP requests.")
	flag.StringVar(&inputPath, "input", "input.txt", "The path to the input text file.")
	flag.StringVar(&outputPath, "output", "output.txt", "The path to place the output text file.")
	flag.StringVar(&uri, "url", "https://api.smartystreets.com/street-address", "The full URL to target.")
	flag.IntVar(&maxConcurrentBatches, "batches", 10, "The maximum number of concurrent batches to submit at a time.")
	flag.Parse()

	uri += fmt.Sprintf("?auth-id=%s&auth-token=%s", authID, url.QueryEscape(authToken))
}

///////////////////////////////////////////////////////////////////////////////

var lines int

func main() {
	input, err := os.Open(inputPath)
	if err != nil {
		log.Panic(err)
	}
	defer input.Close()

	output, err := os.Create(outputPath)
	if err != nil {
		log.Panic(err)
	}
	defer output.Close()

	scanner := bufio.NewScanner(input)
	writer := bufio.NewWriter(output)
	defer writer.Flush()

	writer.WriteString(strings.Join(headerFields, "\t") + "\n")

	batcher := NewBatcher(writer)

	for scanner.Scan() {
		lines++
		batcher.Receive(scanner.Text())

		if lines%1000 == 0 {
			fmt.Println("Processed:", lines)
		}
	}

	batcher.Finish()
	fmt.Println("Processed:", lines)
}

///////////////////////////////////////////////////////////////////////////////

func post(payload *bytes.Reader) ([]Candidate, error) {
	var (
		err      error
		response *http.Response
	)

	for x := 0; x < MaxAttemptsPreRequest; x++ {
		response, err = http.Post(uri, "application/json", payload)
		if err != nil || response.StatusCode != http.StatusOK {
			continue
		}

		jsonResponse, err := ioutil.ReadAll(response.Body)
		if err != nil {
			continue
		}

		var candidates []Candidate

		err = json.Unmarshal(jsonResponse, &candidates)
		if err != nil {
			continue
		}

		if len(candidates) == 0 {
			continue
		}

		return candidates, nil
	}

	if err == nil {
		err = fmt.Errorf("Failed batch with HTTP Status: %s", response.Status)
	}

	return nil, err
}

///////////////////////////////////////////////////////////////////////////////

type Batcher struct {
	currentBatch int
	batches      [][]Input
	output       *bufio.Writer
	waiter       *sync.WaitGroup
}

func NewBatcher(output *bufio.Writer) *Batcher {
	return &Batcher{
		waiter:  &sync.WaitGroup{},
		output:  output,
		batches: make([][]Input, maxConcurrentBatches),
	}
}

func (self *Batcher) Receive(line string) {
	input := Input{Street: line, InputID: line}
	added := false

	for i, batch := range self.batches {
		if len(batch) < MaxAddressesPerBatch {
			self.batches[i] = append(self.batches[i], input)
			added = true
			break
		}
	}

	if !added {
		self.sendBatches()
		self.batches = make([][]Input, maxConcurrentBatches)
		self.batches[0] = append(self.batches[0], input)
	}
}

func (self *Batcher) Finish() {
	self.sendBatches()
}

func (self *Batcher) sendBatches() {
	all := make([][]Candidate, maxConcurrentBatches)

	for batchIndex, input := range self.batches {
		if len(input) == 0 {
			continue
		}

		self.waiter.Add(1)

		go func(batchIndex int, input []Input) {
			payload, err := json.Marshal(input)
			if err != nil {
				log.Println("Can't marshal input, filling in with empty values. Error:", err)
			}

			var candidates []Candidate
			if err == nil {
				candidates, err = post(bytes.NewReader(payload))
			} else {
				candidates = []Candidate{}
			}

			if err != nil {
				log.Println("API call failed, filling in with empty values. Error:", err)
			}

			all[batchIndex] = candidates
			self.waiter.Done()
		}(batchIndex, input)

	}
	self.waiter.Wait()

	for b, batch := range all {
		if len(batch) == 0 {
			continue
		}

		c := 0
		for ; c < len(batch); c++ {
			candidate := batch[c]
			for c < candidate.InputIndex { // We've got non-contiguous candidates, fill in with blanks.
				self.output.WriteString(Blank(self.batches[b][c].InputID, c))
				c++
			}

			self.output.WriteString(candidate.String()) // Record the actual valid response.
		}

		for c < len(self.batches[b]) { // The batch is missing a few blanks at the end, fill it in.
			self.output.WriteString(Blank(self.batches[b][c].InputID, c))
			c++
		}
	}
}

///////////////////////////////////////////////////////////////////////////////

type Input struct {
	Street  string `json:"street"`
	InputID string `json:"input_id"`
}

type (
	Candidate struct {
		InputID              string     `json:"input_id,omitempty"`
		InputIndex           int        `json:"input_index"`
		CandidateIndex       int        `json:"candidate_index"`
		Addressee            string     `json:"addressee,omitempty"`
		DeliveryLine1        string     `json:"delivery_line_1,omitempty"`
		DeliveryLine2        string     `json:"delivery_line_2,omitempty`
		LastLine             string     `json:"last_line,omitempty"`
		DeliveryPointBarcode string     `json:"delivery_point_barcode,omitempty"`
		Components           Components `json:"components,omitempty"`
		Metadata             Metadata   `json:"metadata,omitempty"`
		Analysis             Analysis   `json:"analysis,omitempty"`
	}

	Components struct {
		PrimaryNumber            string `json:"primary_number,omitempty"`
		StreetPredirection       string `json:"street_predirection,omitempty"`
		StreetName               string `json:"street_name,omitempty"`
		StreetPostdirection      string `json:"street_postdirection,omitempty"`
		StreetSuffix             string `json:"street_suffix,omitempty"`
		SecondaryNumber          string `json:"secondary_number,omitempty"`
		SecondaryDesignator      string `json:"secondary_designator,omitempty"`
		ExtraSecondaryNumber     string `json:"extra_secondary_number,omitempty"`
		ExtraSecondaryDesignator string `json:"extra_secondary_designator,omitempty"`
		PMBNumber                string `json:"pmb_number,omitempty"`
		PMBDesignator            string `json:"pmb_designator,omitempty"`
		CityName                 string `json:"city_name,omitempty"`
		DefaultCityName          string `json:"default_city_name,omitempty"`
		StateAbbreviation        string `json:"state_abbreviation,omitempty"`
		ZIPCode                  string `json:"zipcode,omitempty"`
		Plus4Code                string `json:"plus4_code,omitempty"`
		DeliveryPoint            string `json:"delivery_point,omitempty"`
		DeliveryPointCheckDigit  string `json:"delivery_point_check_digit,omitempty"`
		Urbanization             string `json:"urbanization,omitempty"`
	}

	Metadata struct {
		RecordType               string  `json:"record_type,omitempty"`
		ZIPType                  string  `json:"zip_type,omitempty"`
		CountyFIPS               string  `json:"county_fips,omitempty"`
		CountyName               string  `json:"county_name,omitempty"`
		CarrierRoute             string  `json:"carrier_route,omitempty"`
		CongressionalDistrict    string  `json:"congressional_district,omitempty"`
		BuildingDefaultIndicator string  `json:"building_default_indicator,omitempty"`
		RDI                      string  `json:"rdi,omitempty"`
		ELOTSequence             string  `json:"elot_sequence,omitempty"`
		ELOTSort                 string  `json:"elot_sort,omitempty"`
		EWSMatch                 bool    `json:"ews_match,omitempty"`
		Latitude                 float64 `json:"latitude,omitempty"`
		Longitude                float64 `json:"longitude,omitempty"`
		Precision                string  `json:"precision,omitempty"`
		TimeZone                 string  `json:"time_zone,omitempty"`
		UTCOffset                float32 `json:"utc_offset,omitempty"`
		DST                      bool    `json:"dst,omitempty"`
	}

	Analysis struct {
		DPVMatchCode      string `json:"dpv_match_code,omitempty"`
		DPVFootnotes      string `json:"dpv_footnotes,omitempty"`
		DPVCMRACode       string `json:"dpv_cmra,omitempty"`
		DPVVacantCode     string `json:"dpv_vacant,omitempty"`
		Active            string `json:"active,omitempty"`
		Footnotes         string `json:"footnotes,omitempty"`
		LACSLinkCode      string `json:"lacslink_code,omitempty"`
		LACSLinkIndicator string `json:"lacslink_indicator,omitempty"`
		SuiteLinkMatch    bool   `json:"suitelink_match,omitempty"`
	}
)

func Blank(inputID string, inputIndex int) string {
	c := Candidate{InputID: inputID, InputIndex: inputIndex}
	return c.String()
}

func (self *Candidate) String() string {
	buffer := []string{
		self.InputID,
		self.Addressee,
		self.DeliveryLine1,
		self.DeliveryLine2,
		self.LastLine,
		self.DeliveryPointBarcode,
		self.Components.Urbanization,
		self.Components.PrimaryNumber,
		self.Components.StreetName,
		self.Components.StreetPredirection,
		self.Components.StreetPostdirection,
		self.Components.StreetSuffix,
		self.Components.SecondaryNumber,
		self.Components.SecondaryDesignator,
		self.Components.ExtraSecondaryNumber,
		self.Components.ExtraSecondaryDesignator,
		self.Components.PMBNumber,
		self.Components.PMBDesignator,
		self.Components.CityName,
		self.Components.DefaultCityName,
		self.Components.StateAbbreviation,
		self.Components.ZIPCode,
		self.Components.Plus4Code,
		self.Components.DeliveryPoint,
		self.Components.DeliveryPointCheckDigit,
		self.Metadata.RecordType,
		self.Metadata.ZIPType,
		self.Metadata.CountyFIPS,
		self.Metadata.CountyName,
		self.Metadata.CarrierRoute,
		self.Metadata.CongressionalDistrict,
		self.Metadata.BuildingDefaultIndicator,
		self.Metadata.RDI,
		self.Metadata.ELOTSequence,
		self.Metadata.ELOTSort,
		fmt.Sprintf("%f", self.Metadata.Latitude),
		fmt.Sprintf("%f", self.Metadata.Longitude),
		self.Metadata.Precision,
		self.Metadata.TimeZone,
		fmt.Sprintf("%v", self.Metadata.UTCOffset),
		fmt.Sprintf("%t", self.Metadata.DST),
		self.Analysis.DPVMatchCode,
		self.Analysis.DPVFootnotes,
		self.Analysis.DPVCMRACode,
		self.Analysis.DPVVacantCode,
		self.Analysis.Active,
		fmt.Sprintf("%t", self.Metadata.EWSMatch),
		self.Analysis.Footnotes,
		self.Analysis.LACSLinkCode,
		self.Analysis.LACSLinkIndicator,
		fmt.Sprintf("%t", self.Analysis.SuiteLinkMatch),
	}

	return strings.Join(buffer, "\t") + "\n"
}

///////////////////////////////////////////////////////////////////////////////

const (
	MaxAddressesPerBatch  = 100
	MaxAttemptsPreRequest = 5
)

var headerFields = []string{
	"Input",
	"Addressee",
	"DeliveryLine1",
	"DeliveryLine2",
	"LastLine",
	"DeliveryPointBarcode",
	"Urbanization",
	"PrimaryNumber",
	"StreetName",
	"StreetPredirection",
	"StreetPostdirection",
	"StreetSuffix",
	"SecondaryNumber",
	"SecondaryDesignator",
	"ExtraSecondaryNumber",
	"ExtraSecondaryDesignator",
	"PMBNumber",
	"PMBDesignator",
	"CityName",
	"DefaultCityName",
	"StateAbbreviation",
	"ZIPCode",
	"Plus4Code",
	"DeliveryPoint",
	"DeliveryPointCheckDigit",
	"RecordType",
	"ZIPType",
	"CountyFIPS",
	"CountyName",
	"CarrierRoute",
	"CongressionalDistrict",
	"BuildingDefaultIndicator",
	"RDI",
	"ELOTSequence",
	"ELOTSort",
	"Latitude",
	"Longitude",
	"Precision",
	"TimeZone",
	"UTCOffset",
	"DST",
	"DPVMatchCode",
	"DPVFootnotes",
	"DPVCMRACode",
	"DPVVacantCode",
	"Active",
	"EWSMatch",
	"Footnotes",
	"LACSLinkCode",
	"LACKLinkIndicator",
	"SuiteLinkMatch",
}

///////////////////////////////////////////////////////////////////////////////
