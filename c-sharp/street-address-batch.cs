namespace RestBatch
{
	// First, ensure that you are using the .NET Framework 4 (NOT .NET Framework 4 "Client Profile").
	// Second, add references to:
	// - Microsoft.CSharp
	// - System
	// - System.Web
	// - Newtonsoft.Json

	using System;
	using System.IO;
	using System.Net;
	using System.Web;
	using Newtonsoft.Json;

	public class Program
	{
		// NOTE: All query string parameter values must be URL-encoded!
		// TIP: Get an auth ID/token pair from your SmartyStreets account and put them below.
		private const string ApiUrl = "https://api.qualifiedaddress.com/street-address/";
		private static readonly string AuthenticationID = HttpUtility.UrlEncode("YOUR_AUTH_ID_HERE");
		private static readonly string AuthenticationToken = HttpUtility.UrlEncode("YOUR_RAW_AUTH_TOKEN_HERE");
		private const string RequestPayload = @"[
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

		public static void Main()
		{
			var url = new Uri(ApiUrl + "?auth-id=" + AuthenticationID + "&auth-token=" + AuthenticationToken);
			var request = (HttpWebRequest)WebRequest.Create(url);
			request.Method = "POST";

			using (var stream = request.GetRequestStream())
			using (var writer = new StreamWriter(stream))
				writer.Write(RequestPayload);

			using (var response = request.GetResponse())
			using (var stream = response.GetResponseStream())
			using (var reader = new StreamReader(stream))
			{
				var rawResponse = reader.ReadToEnd();
				Console.WriteLine(rawResponse);

				// Suppose you wanted to use Json.Net to pretty-print the response (delete the next two lines if not):
				// Json.Net: http://http://json.codeplex.com/
				dynamic parsedJson = JsonConvert.DeserializeObject(rawResponse);
				Console.WriteLine(JsonConvert.SerializeObject(parsedJson, Formatting.Indented));

				// Or suppose you wanted to deserialize the json response to a defined structure (defined below):
				var candidates = JsonConvert.DeserializeObject<CandidateAddress[]>(rawResponse);
				foreach (var address in candidates)
					Console.WriteLine(address.DeliveryLine1);
			}

			Console.ReadLine();
		}

		// Optional strongly-typed data structures: (Generated using: http://json2csharp.com/)
		public class CandidateAddress
		{
			public int InputIndex { get; set; }
			public int CandidateIndex { get; set; }
			public string DeliveryLine1 { get; set; }
			public string LastLine { get; set; }
			public string DeliveryPointBarcode { get; set; }
			public Components Components { get; set; }
			public Metadata Metadata { get; set; }
			public Analysis Analysis { get; set; }
		}

		public class Components
		{
			public string PrimaryNumber { get; set; }
			public string StreetName { get; set; }
			public string StreetSuffix { get; set; }
			public string CityName { get; set; }
			public string StateAbbreviation { get; set; }
			public string Zipcode { get; set; }
			public string Plus4Code { get; set; }
			public string DeliveryPoint { get; set; }
			public string DeliveryPointCheckDigit { get; set; }
		}

		public class Metadata
		{
			public string RecordType { get; set; }
			public string CountyFips { get; set; }
			public string CountyName { get; set; }
			public string CarrierRoute { get; set; }
			public string CongressionalDistrict { get; set; }
			public string Latitude { get; set; }
			public string Longitude { get; set; }
			public string Precision { get; set; }
		}

		public class Analysis
		{
			public string DpvMatchCode { get; set; }
			public string DpvFootnotes { get; set; }
			public string DpvCmra { get; set; }
			public string DpvVacant { get; set; }
			public bool EwsMatch { get; set; }
			public string Footnotes { get; set; }
		}
	}
}