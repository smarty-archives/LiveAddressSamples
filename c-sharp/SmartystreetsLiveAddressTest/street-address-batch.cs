namespace SmartystreetsLiveAddressTest
{
	#region
	using System;
	using System.IO;
	using System.Net;

	#endregion

	public static partial class Program
	{
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

		private static void BatchMain(string[] args)
		{
			var url = new Uri(_apiUrl + "?auth-token=" + _authenticationToken);
			var request = (HttpWebRequest) WebRequest.Create(url);
			request.Method = "POST";

			ComputeTime.Start();
			using (var stream = request.GetRequestStream())
			{
				using (var writer = new StreamWriter(stream))
					writer.Write(RequestPayload);
			}
			ComputeTime.Stop();

			using (var response = request.GetResponse())
			{
				using (var stream = response.GetResponseStream())
				{
					if (stream != null)
					{
						using (var reader = new StreamReader(stream))
						{
							var rawResponse = reader.ReadToEnd();
							Console.WriteLine(rawResponse);

							ParseResults(rawResponse);
						}
					}
				}
			}
		}
	}
}