namespace SmartystreetsLiveAddressTest
{
	#region
	using System.Runtime.Serialization;

	#endregion

	#region Nested type: CandidateAddress
	[DataContract] public class CandidateAddress
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
	#endregion
}