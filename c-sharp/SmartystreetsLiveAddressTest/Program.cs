namespace SmartystreetsLiveAddressTest
{
	using System;
	using System.Collections.Generic;
	using System.Configuration;
	using Newtonsoft.Json;

	public static class Program
	{
		private const string SingleAddressParameter = "single";
		private const string BatchAddressParameter = "batch";
		private static readonly string ApiUrl = ConfigurationManager.AppSettings["ApiUrl"];
		private static readonly string AuthId = ConfigurationManager.AppSettings["AUTH-ID"];
		private static readonly string AuthToken = ConfigurationManager.AppSettings["AUTH-TOKEN"];
		private static readonly SingleAddressExample SingleAddress = new SingleAddressExample(ApiUrl, AuthId, AuthToken);
		private static readonly BatchAddressExample BatchOfAddresses = new BatchAddressExample(ApiUrl, AuthId, AuthToken);

		public static void Main()
		{
			var args = Environment.GetCommandLineArgs();

			if (CommandLineUsageWasCorrect(args))
				ParseResults(ExecuteExample(args[1]));
			else
			{
				DisplayProperUsage();
				ParseResults(ExecuteExample("single"));
			}
			
			EndProgram();
		}

		private static bool CommandLineUsageWasCorrect(IList<string> args)
		{
			return args.Count == 2 && (args[1] == SingleAddressParameter || args[1] == BatchAddressParameter);
		}

		private static string ExecuteExample(string choice)
		{
			return choice == SingleAddressParameter ? SingleAddress.Execute() : BatchOfAddresses.Execute();
		}

		private static void ParseResults(string rawResponse)
		{
			Console.WriteLine("\nRaw Response:");
			Console.WriteLine(rawResponse);
			
			// Suppose you wanted to use Json.Net to pretty-print the response (delete the next two lines if not):
			// Json.Net: http://http://json.codeplex.com/
			dynamic parsedJson = JsonConvert.DeserializeObject(rawResponse);
			Console.WriteLine(JsonConvert.SerializeObject(parsedJson, Formatting.Indented));

			// Or suppose you wanted to deserialize the json response to a defined structure:
			var candidates = JsonConvert.DeserializeObject<CandidateAddress[]>(rawResponse);
			foreach (var address in candidates)
				Console.WriteLine(address.DeliveryLine1);
		}

		private static void DisplayProperUsage()
		{
			Console.WriteLine("\nInvalid Arguments\n" +
				"Usage: \n\nSmartyStreetsLiveAddressTests.exe [single/batch]");
		}

		private static void EndProgram()
		{
			Console.WriteLine("\n\n<ENTER> to continue...");
			Console.ReadLine();
		}
	}
}