namespace SmartystreetsLiveAddressTest
{
	using System.Runtime.Serialization;

	[DataContract] 
	public class Components
	{
		[DataMember(Name = "primary_number")]
		public string PrimaryNumber { get; set; }

		[DataMember(Name = "street_name")]
		public string StreetName { get; set; }

		[DataMember(Name = "street_suffix")]
		public string StreetSuffix { get; set; }

		[DataMember(Name = "city_name")]
		public string CityName { get; set; }

		[DataMember(Name = "state_abbreviation")]
		public string StateAbbreviation { get; set; }

		[DataMember(Name = "zipcode")]
		public string Zipcode { get; set; }

		[DataMember(Name = "plus4_code")]
		public string Plus4Code { get; set; }

		[DataMember(Name = "delivery_point")]
		public string DeliveryPoint { get; set; }

		[DataMember(Name = "delivery_point_check_digit")]
		public string DeliveryPointCheckDigit { get; set; }
	}
}