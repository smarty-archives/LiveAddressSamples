namespace SmartystreetsLiveAddressTest
{
	#region
	using System;
	using System.Net;
	using System.Web;

	#endregion

	public static partial class Program
	{
		private static readonly string Street = HttpUtility.UrlEncode("3214 N University");
		private static readonly string City = HttpUtility.UrlEncode("provo");
		private static readonly string State = HttpUtility.UrlEncode("ut");
		private static readonly string ZipCode = HttpUtility.UrlEncode("84604");

		///<summary>
		///	TODO: Need to handle situations where url is greater than 260. Long addresses can cause this. Windows will throw PathTooLongException.
		///</summary>
		///<param name="args"> </param>
		private static void SingleMain(string[] args)
		{
			var url = _apiUrl + "?auth-token=" + _authenticationToken + "&street=" + Street + "&city=" + City + "&state=" + State +
			          "&zipCode=" + ZipCode;

			using (var client = new WebClient())
			{
				if (url.Length >= 260) {
					Console.WriteLine("Generated url is too long. Max is 260 or PathTooLongException will be thrown. Query can not be ran!");
					return;
				}

				ComputeTime.Start();
				var rawResponse = client.DownloadString(url);
				ComputeTime.Stop();
				Console.WriteLine(rawResponse);

				ParseResults(rawResponse);
			}
		}
	}
}