namespace SmartystreetsLiveAddressTest
{
	using System.Net;
	using System.Web;

	public class SingleAddressExample
	{
		// NOTE: all query string parameter values must be URL-encoded!
		private static readonly string Street = HttpUtility.UrlEncode("3214 N University");
		private static readonly string City = HttpUtility.UrlEncode("provo");
		private static readonly string State = HttpUtility.UrlEncode("ut");
		private static readonly string ZipCode = HttpUtility.UrlEncode("84604");
		private readonly string url;

		public SingleAddressExample(string apiUrl, string authenticationId, string authenticationToken)
		{
			this.url = apiUrl +
				"?auth-id=" + authenticationId +
				"&auth-token=" + authenticationToken +
				"&street=" + Street +
				"&city=" + City +
				"&state=" + State +
				"&zipcode=" + ZipCode;
		}

		public string Execute()
		{
			using (var client = new WebClient())
				return client.DownloadString(this.url);
		}
	}
}