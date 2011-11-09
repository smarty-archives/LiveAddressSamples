private static void ExecuteBatchExample()
{
	// Create batch of addresses
	var address1 = new QualifiedAddress.AddressRequest
	{
		Street = "3214 N University Ave",
		Street2 = string.Empty,
		City = "Provo",
		State = "UT",
		ZipCode = "84604",
		Urbanization = string.Empty,
		LastLine = string.Empty
	};
	var address2 = new QualifiedAddress.AddressRequest
	{
		Street = "1600 ampytheatre parkways",
		Street2 = string.Empty,
		City = "mountans vieww",
		State = "calforna",
		ZipCode = "90210",
		Urbanization = string.Empty,
		LastLine = string.Empty
	};

	// Bundle the batch of addresses in the request
	var request = new QualifiedAddress.ServiceRequest
	{
		Addresses = new[] { address1, address2 },
		Key = "YOUR-KEY-HERE",
		Suggestions = 10,
		Sandbox = false
	};

	// Submit the request
	var service = new QualifiedAddress.VerifyService();
	var response = service.Execute(request);

	 // Check to see that the request was processed successfully
	if (null != response && response.Success)
	{
		// Process each array of suggestions (each array contains suggestions for the corresponding input address)
		//  (there will not be any suggestions if the address could not be verified)
		foreach (var suggestionsArray in response.Addresses)
		{
			// Process each address suggestion
			foreach (var suggestion in suggestionsArray)
			{
				Console.WriteLine(suggestion.Street);
			}
		}
	}
}
