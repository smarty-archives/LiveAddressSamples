namespace SmartystreetsLiveAddressTest
{
	#region
	using System.Runtime.Serialization;

	#endregion

	#region Nested type: Analysis
	[DataContract] public class Analysis
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
	#endregion
}