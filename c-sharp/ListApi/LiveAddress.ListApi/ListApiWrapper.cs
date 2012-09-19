namespace LiveAddress.ListApi
{
	using System;
	using System.IO;
	using System.Net;

	public class ListApiWrapper
	{
		private const string FinishedListStatus = "\"current_step\":\"Succeeded\"";
		private readonly string authentication;

		public ListApiWrapper(string authId, string authToken)
		{
			this.authentication = string.Format("auth-id={0}&auth-token={1}", authId, authToken);
		}

		public void ShowAllLists()
		{
			var url = string.Format("https://api.smartystreets.com/lists?{0}", this.authentication);
			Console.WriteLine(url);
			
			var request = WebRequest.Create(url);
			
			using (var response = request.GetResponse())
			using (var stream = response.GetResponseStream() ?? new MemoryStream())
			using (var reader = new StreamReader(stream))
				JsonHelper.PrintJson(reader.ReadToEnd());
		}

		public Guid UploadList(string pathToFile)
		{
			var file = new FileInfo(pathToFile);

			var url = string.Format(				
				"https://api.smartystreets.com/lists?{0}&filename={1}", this.authentication, file.Name);

			Console.WriteLine(url);

			var request = WebRequest.Create(url);
			request.Method = "POST";

			using (var fileStream = File.Open(pathToFile, FileMode.Open))
			using (var requestStream = request.GetRequestStream())
				fileStream.CopyTo(requestStream);

			using (var response = request.GetResponse())
			using (var responseStream = response.GetResponseStream() ?? new MemoryStream())
			using (var reader = new StreamReader(responseStream))
			{
				var output = reader.ReadToEnd();
				JsonHelper.PrintJson(output);
				
				// Parse the id from the json result: (you could use json.net to do this!)
				const string Search = "list_id\":\"";
				var index = output.IndexOf(Search, StringComparison.Ordinal);
				var id = Guid.Empty;
				if (index > 0)
				{
					var rawId = output.Substring(index + Search.Length, Guid.Empty.ToString().Length);
					Guid.TryParse(rawId, out id);
				}
				return id;
			}

			/* Sample JSON Response:
			 *
			 *	{
			 *		"list_id": "4ba8807e-139b-45e1-a5c7-1e30b5dd5c9a",
			 *		"polling_frequency_in_seconds": 30
			 *	}
			 *
			 */
		}

		public bool CheckStatusOfList(Guid listId)
		{
			var url = string.Format("https://api.smartystreets.com/lists/{0}?{1}", listId, this.authentication);
			Console.WriteLine(url);
			
			var request = WebRequest.Create(url);
			
			using (var response = request.GetResponse())
			using (var responseStream = response.GetResponseStream() ?? new MemoryStream())
			using (var reader = new StreamReader(responseStream))
			{
				var output = reader.ReadToEnd();
				JsonHelper.PrintJson(output);
				return output.Contains(FinishedListStatus);
			}

			/*
			 * Sample JSON Response (list in process):
			 * 
			 *  {
			 *		"current_step": "Processing",
			 *		"step_progress": .54
			 *  }
			 *  
			 * 
			 * Sample JSON Response (finished list): 
			 * 
			 *  {
			 *		"current_step": "Succeeded"
			 *	}
			 * 
			 */
		}

		public void DownloadCompleteList(Guid listId, string destinationPath)
		{
			File.Delete(destinationPath);

			var url = string.Format("https://api.smartystreets.com/lists/{0}/download?{1}", listId, this.authentication);
			Console.WriteLine(url);

			var request = WebRequest.Create(url);

			using (var response = request.GetResponse())
			using (var stream = response.GetResponseStream() ?? new MemoryStream())
			using (var file = File.Open(destinationPath, FileMode.Create))
				stream.CopyTo(file);

			var info = new FileInfo(destinationPath);
			Console.WriteLine("Finished Downloading the complete list to: {0}", Path.Combine(info.Directory.FullName, info.FullName));
		}

		public void DeleteList(Guid listId)
		{
			var url = string.Format("https://api.smartystreets.com/lists/{0}?{1}", listId, this.authentication);
			Console.WriteLine(url);

			var request = WebRequest.Create(url);
			request.Method = "DELETE";

			using (request.GetResponse())
				Console.WriteLine("List ({0}) deleted", listId);
		}
	}
}