namespace SmartystreetsLiveAddressTest
{
	#region
	using System;
	using System.Configuration;
	using System.Diagnostics;
	using System.Web;
	using Newtonsoft.Json;

	#endregion

	public static partial class Program
	{
		// NOTE: all query string parameter values must be URL-encoded!
		private static string _apiUrl;
		private static string _authenticationToken;

		private static readonly Stopwatch EntireRunTime = new Stopwatch();
		private static readonly Stopwatch ComputeTime = new Stopwatch();

		public static void Main()
		{
			EntireRunTime.Start();

			var args = Environment.GetCommandLineArgs();

			for (var i = 0; i < args.Length; i++)
			{
				var argument = args[i];
				Console.WriteLine("Argument #{0} is {1}", i, argument);
			}

			if ((args.Length != 2) && !((args[1] != "single") || (args[1] != "batch")))
			{
				DisplayUsage(args);
				return;
			}

			if (ConfigurationManager.AppSettings.Count > 0)
			{
				_apiUrl = ConfigurationManager.AppSettings["ApiUrl"];
				_authenticationToken = HttpUtility.UrlEncode(ConfigurationManager.AppSettings["AuthenticationToken"]);
			}

			if (string.IsNullOrWhiteSpace(_apiUrl) || string.IsNullOrWhiteSpace(_authenticationToken))
				throw new Exception("Invalid Application Settings!");

			Console.WriteLine("AuthenticationToken is: {0}", _authenticationToken);
			Console.WriteLine("ApiUrl is: {0}", _apiUrl);

			if (args[1] == "single")
				SingleMain(args);
			if (args[1] == "batch")
				BatchMain(args);

			EntireRunTime.Stop();
			Console.WriteLine("ComputeTime was {0} millisecond(s)", ComputeTime.ElapsedMilliseconds);
			Console.WriteLine("EntireRunTime was {0} millisecond(s)", EntireRunTime.ElapsedMilliseconds);

			Console.ReadLine();
		}

		private static void DisplayUsage(string[] args)
		{
			Console.WriteLine("\nInvalid Arguments");
			Console.WriteLine("Usage: " +
			                  String.Format(@"{0} [single/batch]",
			                                (args == null || string.IsNullOrWhiteSpace(args[0]) ? "[program]" : args[0])));
		}

		private static void ParseResults(string rawResponse)
		{
			// Suppose you wanted to use Json.Net to pretty-print the response (delete the next two lines if not):
			// Json.Net: http://http://json.codeplex.com/
			dynamic parsedJson = JsonConvert.DeserializeObject(rawResponse);
			Console.WriteLine(JsonConvert.SerializeObject(parsedJson, Formatting.Indented));

			// Or suppose you wanted to deserialize the json response to a defined structure:
			var candidates = JsonConvert.DeserializeObject<CandidateAddress[]>(rawResponse);
			foreach (var address in candidates)
				Console.WriteLine(address.DeliveryLine1);
		}
	}
}