namespace SmartystreetsLiveAddressTest
{
	using System.Runtime.Serialization;

	[DataContract] 
	public class Metadata
	{
		[DataMember(Name = "record_type")]
		public string RecordType { get; set; }

		[DataMember(Name = "county_fips")]
		public string CountyFips { get; set; }

		[DataMember(Name = "county_name")]
		public string CountyName { get; set; }

		[DataMember(Name = "carrier_route")]
		public string CarrierRoute { get; set; }

		[DataMember(Name = "congressional_district")]
		public string CongressionalDistrict { get; set; }

		[DataMember(Name = "latitude")]
		public string Latitude { get; set; }

		[DataMember(Name = "longitude")]
		public string Longitude { get; set; }

		[DataMember(Name = "precision")]
		public string Precision { get; set; }
	}
}