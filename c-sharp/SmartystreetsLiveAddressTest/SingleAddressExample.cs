namespace SmartystreetsLiveAddressTest
{
	using System;
	using System.Net;
	using System.Web;

	public class SingleAddressExample
	{
		private const string UrlTooLongErrorMessage = 
			"Sorry, the url must be shorter than 260 characters (yours was {0} characters long)." +
			"As a work-around, See the BatchAddressExample for an alternate method using a WebRequest.";
		
		// NOTE: all query string parameter values must be URL-encoded!
		private static readonly string Street = HttpUtility.UrlEncode("3214 N University");
		private static readonly string City = HttpUtility.UrlEncode("provo");
		private static readonly string State = HttpUtility.UrlEncode("ut");
		private static readonly string ZipCode = HttpUtility.UrlEncode("84604");
		private readonly string apiUrl;
		private readonly string authenticationToken;

		public SingleAddressExample(string apiUrl, string authenticationToken)
		{
			this.apiUrl = apiUrl;
			this.authenticationToken = authenticationToken;
		}

		public string Execute()
		{
			var url = this.apiUrl + 
				"?auth-token=" + this.authenticationToken + 
				"&street=" + Street + 
				"&city=" + City + 
				"&state=" + State +
				"&zipCode=" + ZipCode;

			using (var client = new WebClient())
			{
				if (url.Length >= 260)
				{
					Console.WriteLine(UrlTooLongErrorMessage, url.Length);
					return string.Empty;
				}

				return client.DownloadString(url);
			}
		}
	}
}