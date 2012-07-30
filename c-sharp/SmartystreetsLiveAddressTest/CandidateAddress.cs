namespace SmartystreetsLiveAddressTest
{
	using System.Runtime.Serialization;

	[DataContract]
	public class CandidateAddress
	{
		[DataMember(Name = "input_index")]
		public int InputIndex { get; set; }

		[DataMember(Name = "candidate_index")]
		public int CandidateIndex { get; set; }

		[DataMember(Name = "delivery_line_1")]
		public string DeliveryLine1 { get; set; }

		[DataMember(Name = "last_line")]
		public string LastLine { get; set; }

		[DataMember(Name = "delivery_point_barcode")]
		public string DeliveryPointBarcode { get; set; }

		[DataMember(Name = "components")]
		public Components Components { get; set; }

		[DataMember(Name = "metadata")]
		public Metadata Metadata { get; set; }

		[DataMember(Name = "analysis")]
		public Analysis Analysis { get; set; }
	}

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

	[DataContract]
	public class Analysis
	{
		[DataMember(Name = "dpv_match_code")]
		public string DpvMatchCode { get; set; }

		[DataMember(Name = "dpv_footnotes")]
		public string DpvFootnotes { get; set; }

		[DataMember(Name = "dpv_cmra_code")]
		public string DpvCmraCode { get; set; }

		[DataMember(Name = "dpv_vacant_code")]
		public string DpvVacantCode { get; set; }

		[DataMember(Name = "ews_match")]
		public bool EwsMatch { get; set; }

		[DataMember(Name = "footnotes")]
		public string Footnotes { get; set; }

		[DataMember(Name = "lacslink_code")]
		public string LacsLinkCode { get; set; }

		[DataMember(Name = "lacslink_indicator")]
		public string LacsLinkIndicator { get; set; }
	}
}