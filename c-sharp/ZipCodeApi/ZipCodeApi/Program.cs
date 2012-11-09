namespace ZipCodeApi
{
	using System;
	using System.Configuration;
	using System.Net;
	using System.Web;

	public static class Program
	{
		public static void Main()
		{
			HttpGet(zipCode: "20500");            // shows City/State options for that ZIP Code
			HttpGet("Cupertino", "CA");           // shows ZIP Code options for that City/State combination
			HttpGet("Cupertino", "CA", "95014");  // confirms that the City/State and ZIP Code match.
			HttpGet();                            // blank query string - HTTP 400 - bad input
			HttpGet(zipCode: "eibn3ei2nb");       // Invalid ZIP Code
			HttpGet("Does not exist", "CA");      // Invalid City
			HttpGet("Cupertino", "ca", "90210");  // Conflicting City/State and ZIP Code

			HttpPost(string.Empty);               // empty payload - HTTP 400 - bad input
			HttpPost(PostPayload);                // all previous examples in a single POST request

			Console.WriteLine("Done. <ENTER> to quit.");
			Console.ReadLine();
		}

		private static void HttpGet(string city = "", string state = "", string zipCode = "")
		{
			TryExecute(() =>
			{
				using (var client = new WebClient())
				{
					city = HttpUtility.UrlEncode(city ?? string.Empty);
					state = HttpUtility.UrlEncode(state ?? string.Empty);
					zipCode = HttpUtility.UrlEncode(zipCode ?? string.Empty);
					var url = string.Format(Url, AuthId, AuthToken) + string.Format(QueryString, city, state, zipCode);

					Console.WriteLine("City: {0}\nState: {1}\nZIP Code: {2}", city, state, zipCode);
					Console.WriteLine(url);
					JsonHelper.PrintJson(client.DownloadString(url));
				}
			});
			
		}

		private static void HttpPost(string payload)
		{
			TryExecute(() =>
			{
				using (var client = new WebClient())
				{
					var url = string.Format(Url, AuthId, AuthToken);
					Console.WriteLine("{0} (with POST payload)", url);
					JsonHelper.PrintJson(client.UploadString(url, payload));
				}
			});
		}

		private static void TryExecute(Action action)
		{
			try
			{
				action();
			}
			catch (Exception e)
			{
				Console.WriteLine(e.Message);
			}
		}

		private const string PostPayload = @"
[
	{
		zipcode: '20500'
	},
	{
		city: 'Cupertino',
		state: 'CA'
	},
	{
		city: 'Cupertino',
		state: 'CA',
		zipcode: '95014'
	},
	{
	},
	{
		zipcode: 'eibn3ei2nb'
	},
	{
		city: 'Does not exist',
		state: 'CA'
	},
	{
		city: 'Cupertino',
		state: 'ca',
		zipcode: '90210'
	}
]
";
		private static readonly string Url = ConfigurationManager.AppSettings["Url"];
		private static readonly string QueryString = ConfigurationManager.AppSettings["QueryString"];
		private static readonly string AuthId = ConfigurationManager.AppSettings["AuthId"];
		private static readonly string AuthToken = HttpUtility.UrlEncode(ConfigurationManager.AppSettings["RawAuthToken"]);
	}
}