namespace ZipCodeApi
{
	using System;
	using System.Collections.Generic;
	using System.Linq;
	using System.Text;
	
	// This class from the accepted answer to this question: 
	// http://stackoverflow.com/questions/4580397/json-formatter-in-c

	public class JsonHelper
	{
		private const string IndentString = "    ";

		public static void PrintJson(string str)
		{
			Console.WriteLine("\n" + FormatJson(str) + "\n");
		}

		static string FormatJson(string str)
		{
			var indent = 0;
			var quoted = false;
			var sb = new StringBuilder();
			for (var i = 0; i < str.Length; i++)
			{
				var ch = str[i];
				switch (ch)
				{
					case '{':
					case '[':
						sb.Append(ch);
						if (!quoted)
						{
							sb.AppendLine();
							Enumerable.Range(0, ++indent).ForEach(item => sb.Append(IndentString));
						}
						break;
					case '}':
					case ']':
						if (!quoted)
						{
							sb.AppendLine();
							Enumerable.Range(0, --indent).ForEach(item => sb.Append(IndentString));
						}
						sb.Append(ch);
						break;
					case '"':
						sb.Append(ch);
						var escaped = false;
						var index = i;
						while (index > 0 && str[--index] == '\\')
							escaped = !escaped;
						if (!escaped)
							quoted = !quoted;
						break;
					case ',':
						sb.Append(ch);
						if (!quoted)
						{
							sb.AppendLine();
							Enumerable.Range(0, indent).ForEach(item => sb.Append(IndentString));
						}
						break;
					case ':':
						sb.Append(ch);
						if (!quoted)
							sb.Append(" ");
						break;
					default:
						sb.Append(ch);
						break;
				}
			}
			return sb.ToString();
		}
	}

	static class Extensions
	{
		public static void ForEach<T>(this IEnumerable<T> ie, Action<T> action)
		{
			foreach (var i in ie)
				action(i);
		}
	}
}