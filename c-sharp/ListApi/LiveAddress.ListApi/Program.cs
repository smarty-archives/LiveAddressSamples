namespace LiveAddress.ListApi
{
	using System;
	using System.Configuration;
	using System.Threading;
	using System.Web;

	public static class Program
	{
		private static readonly TimeSpan PollingFrequency = TimeSpan.FromSeconds(30);
		private static readonly TimeSpan GiveShortListsAChanceToCompleteBeforeCheckingStatusForTheFirstTime = TimeSpan.FromSeconds(5);
		private static readonly string AuthId = ConfigurationManager.AppSettings["AuthId"];
		private static readonly string AuthToken = HttpUtility.UrlEncode(ConfigurationManager.AppSettings["AuthToken"]);
		private static readonly string InputList = ConfigurationManager.AppSettings["InputList"];
		private static readonly string OutputDestination = ConfigurationManager.AppSettings["OutputDestination"];
		private static readonly ListApiWrapper ListApi = new ListApiWrapper(AuthId, AuthToken);

		public static void Main()
		{
			ListApi.ShowAllLists();

			var newListId = ListApi.UploadList(InputList);

			WaitForListToComplete(newListId);

			ListApi.ShowAllLists(); // should include the list you uploaded just now

			ListApi.DownloadCompleteList(newListId, OutputDestination); // Deducts necessary credits from your account (will fail with HTTP 402 "Payment Required" if you don't have enough)

			ListApi.DeleteList(newListId);

			ListApi.ShowAllLists(); // should match the initial output

			Console.WriteLine("<ENTER> to quit...");
			Console.ReadLine();
		}

		private static void WaitForListToComplete(Guid newListId)
		{
			while (true)
			{
				Thread.Sleep(GiveShortListsAChanceToCompleteBeforeCheckingStatusForTheFirstTime);

				var finished = ListApi.CheckStatusOfList(newListId);
				if (finished)
					break;

				Console.WriteLine("List is still in process--will check status again in {0}", PollingFrequency);
				Thread.Sleep(PollingFrequency);
			}
		}
	}
}