namespace Rest
{
	// First, ensure that you are using the .NET Framework 4 (NOT .NET Framework 4 "Client Profile").
	// Second, add references to:
	// - Microsoft.CSharp
	// - System
	// - System.Web
	// - System.Runtime.Serialization
	// - Newtonsoft.Json

	using System;
	using System.Net;
	using System.Runtime.Serialization;
	using System.Web;
	using Newtonsoft.Json;

	public class Program
	{
		// NOTE: All query string parameter values must be URL-encoded!
		// TIP: Get an auth ID/token pair from your SmartyStreets account and put them below.
		private const string ApiUrl = "https://api.smartystreets.com/street-address/";
		private static readonly string AuthenticationID = HttpUtility.UrlEncode("YOUR_AUTH_ID_HERE");
		private static readonly string AuthenticationToken = HttpUtility.UrlEncode("YOUR_AUTH_TOKEN_HERE");
		private static readonly string Street = HttpUtility.UrlEncode("3214 N University");
		private static readonly string City = HttpUtility.UrlEncode("provo");
		private static readonly string State = HttpUtility.UrlEncode("ut");
		private static readonly string ZipCode = HttpUtility.UrlEncode("84604");

		public static void Main()
		{
			var url = ApiUrl +
					  "?auth-id=" + AuthenticationID +
					  "&auth-token=" + AuthenticationToken +
					  "&street=" + Street +
					  "&city=" + City +
					  "&state=" + State +
					  "&zipcode=" + ZipCode;

			using (var client = new WebClient())
			{
				var rawResponse = client.DownloadString(url);
				Console.WriteLine(rawResponse);

				// Suppose you wanted to use Json.Net to pretty-print the response (delete the next two lines if not):
				// Json.Net: http://http://json.codeplex.com/
				dynamic parsedJson = JsonConvert.DeserializeObject(rawResponse);
				Console.WriteLine(JsonConvert.SerializeObject(parsedJson, Formatting.Indented));

				// Or suppose you wanted to deserialize the json response to a defined structure:
				var candidates = JsonConvert.DeserializeObject<CandidateAddress[]>(rawResponse);
				foreach (var address in candidates)
					Console.WriteLine(address.DeliveryLine1);
			}

			Console.ReadLine();
		}

		[DataContract]
		public class CandidateAddress
		{
			[DataMember(Name = "input_index")]
			public int InputIndex { get; set; }

			[DataMember(Name = "candidate_index")]
			public int CandidateIndex { get; set; }

			[DataMember(Name = "delivery_line_1")]
			public string DeliveryLine1 { get; set; }

			[DataMember(Name = "last_line")]
			public string LastLine { get; set; }

			[DataMember(Name = "delivery_point_barcode")]
			public string DeliveryPointBarcode { get; set; }

			[DataMember(Name = "components")]
			public Components Components { get; set; }

			[DataMember(Name = "metadata")]
			public Metadata Metadata { get; set; }

			[DataMember(Name = "analysis")]
			public Analysis Analysis { get; set; }
		}

		[DataContract]
		public class Components
		{
			[DataMember(Name = "primary_number")]
			public string PrimaryNumber { get; set; }

			[DataMember(Name = "street_name")]
			public string StreetName { get; set; }

			[DataMember(Name = "street_suffix")]
			public string StreetSuffix { get; set; }

			[DataMember(Name = "city_name")]
			public string CityName { get; set; }

			[DataMember(Name = "state_abbreviation")]
			public string StateAbbreviation { get; set; }

			[DataMember(Name = "zipcode")]
			public string Zipcode { get; set; }

			[DataMember(Name = "plus4_code")]
			public string Plus4Code { get; set; }

			[DataMember(Name = "delivery_point")]
			public string DeliveryPoint { get; set; }

			[DataMember(Name = "delivery_point_check_digit")]
			public string DeliveryPointCheckDigit { get; set; }
		}

		[DataContract]
		public class Metadata
		{
			[DataMember(Name = "record_type")]
			public string RecordType { get; set; }

			[DataMember(Name = "county_fips")]
			public string CountyFips { get; set; }

			[DataMember(Name = "county_name")]
			public string CountyName { get; set; }

			[DataMember(Name = "carrier_route")]
			public string CarrierRoute { get; set; }

			[DataMember(Name = "congressional_district")]
			public string CongressionalDistrict { get; set; }

			[DataMember(Name = "latitude")]
			public string Latitude { get; set; }

			[DataMember(Name = "longitude")]
			public string Longitude { get; set; }

			[DataMember(Name = "precision")]
			public string Precision { get; set; }
		}

		[DataContract]
		public class Analysis
		{
			[DataMember(Name = "dpv_match_code")]
			public string DpvMatchCode { get; set; }

			[DataMember(Name = "dpv_footnotes")]
			public string DpvFootnotes { get; set; }

			[DataMember(Name = "dpv_cmra_code")]
			public string DpvCmraCode { get; set; }

			[DataMember(Name = "dpv_vacant_code")]
			public string DpvVacantCode { get; set; }

			[DataMember(Name = "ews_match")]
			public bool EwsMatch { get; set; }

			[DataMember(Name = "footnotes")]
			public string Footnotes { get; set; }

			[DataMember(Name = "lacslink_code")]
			public string LacsLinkCode { get; set; }

			[DataMember(Name = "lacslink_indicator")]
			public string LacsLinkIndicator { get; set; }
		}
	}
}