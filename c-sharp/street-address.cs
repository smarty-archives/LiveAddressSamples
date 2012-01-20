namespace Rest
{
	using System;
	using System.IO;
	using System.Net;
	using System.Web;
	using Newtonsoft.Json;

	public class Program
	{
		private static readonly string AuthenticationToken = HttpUtility.UrlEncode("YOUR_AUTHENTICATION_TOKEN_HERE");
		private static readonly string Street = HttpUtility.UrlEncode("3214 N University");
		private static readonly string City = HttpUtility.UrlEncode("provo");
		private static readonly string State = HttpUtility.UrlEncode("ut");
		private static readonly string ZipCode = HttpUtility.UrlEncode("84604");

		// Simple HTTP GET request:
		public static void Main()
		{
			// NOTE: all query string parameter values must be URL-encoded (as shown above)!
			var url = "https://api.qualifiedaddress.com/street-address/" +
				"?auth-token=" + AuthenticationToken +
				"&street=" + Street +
				"&city=" + City +
				"&state=" + State +
				"&zipCode=" + ZipCode;

			var request = WebRequest.Create(url);
			using (var response = request.GetResponse())
			using (var reader = new StreamReader(response.GetResponseStream() ?? new MemoryStream()))
			{
				var rawResponse = reader.ReadToEnd();
				Console.WriteLine(rawResponse);

				// Suppose you wanted to use Json.Net to pretty-print the response (delete the next two lines if not):
				// Json.Net: http://http://json.codeplex.com/
				dynamic parsedJson = JsonConvert.DeserializeObject(rawResponse);
                Console.WriteLine(JsonConvert.SerializeObject(parsedJson, Formatting.Indented));
			}

			Console.ReadLine();
		}
	}
}
