package main

import (
	"encoding/csv"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
	"strconv"

	"github.com/smartystreets/configo"
)

var (
	inputFilename string
	authID        string
	authToken     string
)

func init() {
	log.SetFlags(0)
	reader := configo.NewReader(
		configo.FromEnvironment(),
		configo.FromCommandLineFlags().
			Register("input", "The path of the input file.").
			Register("auth-id", "The auth-id to use.").
			Register("auth-token", "The auth-token to use."))

	reader.RegisterAlias("auth-id", "SMARTY_AUTH_ID")
	reader.RegisterAlias("auth-token", "SMARTY_AUTH_TOKEN")

	inputFilename = reader.StringDefault("input", "/Users/mike/Desktop/in_japan.csv")
	authID = reader.String("auth-id")
	authToken = reader.String("auth-token")
}

func main() {
	if len(inputFilename) == 0 {
		flag.Usage()
		log.Fatal()
	}

	if !exists(inputFilename) {
		log.Fatal("The input file does not exist.")
	}

	if len(authID) == 0 {
		if authID = os.Getenv("SMARTY_AUTH_ID"); len(authID) == 0 {
			log.Fatal("An auth-id is required.")
		}
	}
	if len(authToken) == 0 {
		if authToken = os.Getenv("SMARTY_AUTH_TOKEN"); len(authToken) == 0 {
			log.Fatal("An auth-token is required.")
		}
	}

	file, err := os.Open(inputFilename)
	if err != nil {
		log.Fatal(err)
	}

	reader := csv.NewReader(file)
	all, err := reader.ReadAll()
	if err != nil {
		log.Fatal(err)
	}
	err = file.Close()
	if err != nil {
		log.Fatal(err)
	}

	output, err := os.Create("output.csv")
	if err != nil {
		log.Fatal(err)
	}
	writer := csv.NewWriter(output)

	for i, record := range all {
		if i == 0 { // header
			writer.Write(append(record, resultsHeader...))
			continue
		}
		id := i + 1
		request := buildRequest(id, record)
		log.Println(i, request)
		response, err := http.Get(request)
		if err != nil {
			log.Fatal(err)
		}
		if response.StatusCode != http.StatusOK {
			dump, _ := httputil.DumpResponse(response, true)
			log.Fatal("Non-200:\n", string(dump))
		}

		results, err := deserializeResponseBody(response.Body)
		if err != nil {
			log.Fatal(err)
		}

		if len(results) > 1 {
			log.Println("LOTS:", len(results))
		}
		for j, result := range results {
			err = writer.Write(result.toCSV(i, j, record))
			if err != nil {
				log.Fatal(err)
			}
		}
	}

	writer.Flush()
	err = output.Close()
	if err != nil {
		log.Fatal(err)
	}
}

func buildRequest(lineNumber int, record []string) string {
	// return fmt.Sprintf("https://international-api.smartystreets.com/verify?auth-id=%s&auth-token=%s&geocode=true&input_id=%d&organization=%s&address1=%s&address2=%s&locality=%s&administrative_area=%s&postal_code=%s&country=%s",
	return fmt.Sprintf("http://localhost:3215/verify?auth-id=%s&auth-token=%s&geocode=true&input_id=%d&organization=%s&address1=%s&address2=%s&locality=%s&administrative_area=%s&postal_code=%s&country=%s",
		authID, authToken, lineNumber,
		url.QueryEscape(record[2]),
		url.QueryEscape(record[3]),
		url.QueryEscape(record[4]),
		url.QueryEscape(record[5]),
		url.QueryEscape(record[6]),
		url.QueryEscape(record[7]),
		url.QueryEscape(record[8]))
}

func exists(filename string) bool {
	_, err := os.Stat(filename)
	return err == nil
}

func deserializeResponseBody(reader io.Reader) ([]Result, error) {
	all, err := ioutil.ReadAll(reader)
	if err != nil {
		return nil, err
	}
	var results []Result
	err = json.Unmarshal(all, &results)
	return results, err
}

func (this Result) toCSV(inputIndex, candidateIndex int, input []string) []string {
	return append(input,
		strconv.Itoa(inputIndex),
		strconv.Itoa(candidateIndex),
		this.Organization,
		this.Address1,
		this.Address2,
		this.Address3,
		this.Address4,
		this.Address5,
		this.Address6,
		this.Address7,
		this.Address8,
		this.Address9,
		this.Address10,
		this.Address11,
		this.Address12,
		this.Country,
		this.Components.SuperAdministrativeArea,
		this.Components.AdministrativeArea,
		this.Components.SubAdministrativeArea,
		this.Components.Building,
		this.Components.DependentLocality,
		this.Components.DependentLocalityName,
		this.Components.DoubleDependentLocality,
		this.Components.CountryISO2,
		this.Components.CountryISO3,
		this.Components.CountryISON,
		this.Components.Locality,
		this.Components.PostalCode,
		this.Components.PostalCodeShort,
		this.Components.PostalCodeExtra,
		this.Components.Premise,
		this.Components.PremiseExtra,
		this.Components.PremiseNumber,
		this.Components.PremiseType,
		this.Components.Thoroughfare,
		this.Components.ThoroughfarePredirection,
		this.Components.ThoroughfarePostdirection,
		this.Components.ThoroughfareName,
		this.Components.ThoroughfareTrailingType,
		this.Components.ThoroughfareType,
		this.Components.DependentThoroughfare,
		this.Components.DependentThoroughfarePredirection,
		this.Components.DependentThoroughfarePostdirection,
		this.Components.DependentThoroughfareName,
		this.Components.DependentThoroughfareTrailingType,
		this.Components.DependentThoroughfareType,
		this.Components.BuildingLeadingType,
		this.Components.BuildingName,
		this.Components.BuildingTrailingType,
		this.Components.SubBuildingType,
		this.Components.SubBuildingNumber,
		this.Components.SubBuildingName,
		this.Components.SubBuilding,
		this.Components.PostBox,
		this.Components.PostBoxType,
		this.Components.PostBoxNumber,
		fmt.Sprintf("%v", this.Metadata.Latitude),
		fmt.Sprintf("%v", this.Metadata.Longitude),
		this.Metadata.GeocodePrecision,
		this.Metadata.MaxGeocodePrecision,
		this.Analysis.VerificationStatus,
		this.Analysis.AddressPrecision,
		this.Analysis.MaxAddressPrecision,
	)
}

/////////////////////////////////////////////////////////////////////////////////////////////

type Result struct {
	Organization string     `json:"organization,omitempty"`
	Address1     string     `json:"address1,omitempty"`
	Address2     string     `json:"address2,omitempty"`
	Address3     string     `json:"address3,omitempty"`
	Address4     string     `json:"address4,omitempty"`
	Address5     string     `json:"address5,omitempty"`
	Address6     string     `json:"address6,omitempty"`
	Address7     string     `json:"address7,omitempty"`
	Address8     string     `json:"address8,omitempty"`
	Address9     string     `json:"address9,omitempty"`
	Address10    string     `json:"address10,omitempty"`
	Address11    string     `json:"address11,omitempty"`
	Address12    string     `json:"address12,omitempty"`
	Country      string     `json:"country,omitempty"`
	Components   Components `json:"components"`
	Metadata     Metadata   `json:"metadata"`
	Analysis     Analysis   `json:"analysis"`
}
type Components struct {
	SuperAdministrativeArea            string `json:"super_administrative_area,omitempty"`
	AdministrativeArea                 string `json:"administrative_area,omitempty"`
	SubAdministrativeArea              string `json:"sub_administrative_area,omitempty"`
	Building                           string `json:"building,omitempty"`
	DependentLocality                  string `json:"dependent_locality,omitempty"`
	DependentLocalityName              string `json:"dependent_locality_name,omitempty"`
	DoubleDependentLocality            string `json:"double_dependent_locality,omitempty"`
	CountryISO2                        string `json:"-"`
	CountryISO3                        string `json:"-"`
	CountryISON                        string `json:"-"`
	Locality                           string `json:"locality,omitempty"`
	PostalCode                         string `json:"postal_code,omitempty"`
	PostalCodeShort                    string `json:"postal_code_short,omitempty"`
	PostalCodeExtra                    string `json:"postal_code_extra,omitempty"`
	Premise                            string `json:"premise,omitempty"`
	PremiseExtra                       string `json:"premise_extra,omitempty"`
	PremiseNumber                      string `json:"premise_number,omitempty"`
	PremiseType                        string `json:"premise_type,omitempty"`
	Thoroughfare                       string `json:"thoroughfare,omitempty"`
	ThoroughfarePredirection           string `json:"thoroughfare_predirection,omitempty"`
	ThoroughfarePostdirection          string `json:"thoroughfare_postdirection,omitempty"`
	ThoroughfareName                   string `json:"thoroughfare_name,omitempty"`
	ThoroughfareTrailingType           string `json:"thoroughfare_trailing_type,omitempty"`
	ThoroughfareType                   string `json:"thoroughfare_type,omitempty"`
	DependentThoroughfare              string `json:"dependent_thoroughfare,omitempty"`
	DependentThoroughfarePredirection  string `json:"dependent_thoroughfare_predirection,omitempty"`
	DependentThoroughfarePostdirection string `json:"dependent_thoroughfare_postdirection,omitempty"`
	DependentThoroughfareName          string `json:"dependent_thoroughfare_name,omitempty"`
	DependentThoroughfareTrailingType  string `json:"dependent_thoroughfare_trailing_type,omitempty"`
	DependentThoroughfareType          string `json:"dependent_thoroughfare_type,omitempty"`
	BuildingLeadingType                string `json:"building_leading_type,omitempty"`
	BuildingName                       string `json:"building_name,omitempty"`
	BuildingTrailingType               string `json:"building_trailing_type,omitempty"`
	SubBuildingType                    string `json:"sub_building_type,omitempty"`
	SubBuildingNumber                  string `json:"sub_building_number,omitempty"`
	SubBuildingName                    string `json:"sub_building_name,omitempty"`
	SubBuilding                        string `json:"sub_building,omitempty"`
	PostBox                            string `json:"post_box,omitempty"`
	PostBoxType                        string `json:"post_box_type,omitempty"`
	PostBoxNumber                      string `json:"post_box_number,omitempty"`
}
type Metadata struct {
	Latitude            float64 `json:"latitude,omitempty"`
	Longitude           float64 `json:"longitude,omitempty"`
	GeocodePrecision    string  `json:"geocode_precision,omitempty"`
	MaxGeocodePrecision string  `json:"max_geocode_precision,omitempty"`
}
type Analysis struct {
	VerificationStatus  string `json:"verification_status,omitempty"`
	AddressPrecision    string `json:"address_precision,omitempty"`
	MaxAddressPrecision string `json:"max_address_precision,omitempty"`
}

var resultsHeader = []string{
	"Record-Index",
	"Result-Candidate-Index",
	"Result-Organization",
	"Result-Address1",
	"Result-Address2",
	"Result-Address3",
	"Result-Address4",
	"Result-Address5",
	"Result-Address6",
	"Result-Address7",
	"Result-Address8",
	"Result-Address9",
	"Result-Address10",
	"Result-Address11",
	"Result-Address12",
	"Result-Country",
	"Components-SuperAdministrativeArea",
	"Components-AdministrativeArea",
	"Components-SubAdministrativeArea",
	"Components-Building",
	"Components-DependentLocality",
	"Components-DependentLocalityName",
	"Components-DoubleDependentLocality",
	"Components-CountryISO2",
	"Components-CountryISO3",
	"Components-CountryISON",
	"Components-Locality",
	"Components-PostalCode",
	"Components-PostalCodeShort",
	"Components-PostalCodeExtra",
	"Components-Premise",
	"Components-PremiseExtra",
	"Components-PremiseNumber",
	"Components-PremiseType",
	"Components-Thoroughfare",
	"Components-ThoroughfarePredirection",
	"Components-ThoroughfarePostdirection",
	"Components-ThoroughfareName",
	"Components-ThoroughfareTrailingType",
	"Components-ThoroughfareType",
	"Components-DependentThoroughfare",
	"Components-DependentThoroughfarePredirection",
	"Components-DependentThoroughfarePostdirection",
	"Components-DependentThoroughfareName",
	"Components-DependentThoroughfareTrailingType",
	"Components-DependentThoroughfareType",
	"Components-BuildingLeadingType",
	"Components-BuildingName",
	"Components-BuildingTrailingType",
	"Components-SubBuildingType",
	"Components-SubBuildingNumber",
	"Components-SubBuildingName",
	"Components-SubBuilding",
	"Components-PostBox",
	"Components-PostBoxType",
	"Components-PostBoxNumber",
	"Metadata-Latitude",
	"Metadata-Longitude",
	"Metadata-GeocodePrecision",
	"Metadata-MaxGeocodePrecision",
	"Analysis-VerificationStatus",
	"Analysis-AddressPrecision",
	"Analysis-MaxAddressPrecision",
}
