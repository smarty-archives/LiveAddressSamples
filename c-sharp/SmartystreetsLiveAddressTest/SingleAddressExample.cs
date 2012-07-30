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
		private readonly string url;

		public SingleAddressExample(string apiUrl, string authenticationToken)
		{
			this.url = apiUrl +
				"?auth-token=" + authenticationToken +
				"&street=" + Street +
				"&city=" + City +
				"&state=" + State +
				"&zipCode=" + ZipCode;
		}

		public string Execute()
		{
			if (this.url.Length >= 260)
			{
				Console.WriteLine(UrlTooLongErrorMessage, this.url.Length);
				return string.Empty;
			}

			using (var client = new WebClient())
				return client.DownloadString(this.url);
		}
	}
}