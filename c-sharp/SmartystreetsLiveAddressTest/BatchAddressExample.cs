namespace SmartystreetsLiveAddressTest
{
	using System;
	using System.IO;
	using System.Net;

	public class BatchAddressExample
	{
		private readonly string apiUrl;
		private readonly string authenticationToken;
		private const string RequestPayload =
			@"[
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

		public BatchAddressExample(string apiUrl, string authenticationToken)
		{
			this.apiUrl = apiUrl;
			this.authenticationToken = authenticationToken;
		}

		public string Execute()
		{
			var url = new Uri(this.apiUrl + "?auth-token=" + this.authenticationToken);
			var request = (HttpWebRequest)WebRequest.Create(url);
			request.Method = "POST";

			using (var stream = request.GetRequestStream())
			using (var writer = new StreamWriter(stream))
				writer.Write(RequestPayload);

			using (var response = request.GetResponse())
			using (var stream = response.GetResponseStream())
				if (stream != null)
					using (var reader = new StreamReader(stream))
						return reader.ReadToEnd();
			
			return string.Empty;
		}
	}
}