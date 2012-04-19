/**
 * LiveAddress API Example (Java implementation)
 *
 * DEPENDENCIES: json-simple		http://code.google.com/p/json-simple/
 *
 * Performs a POST request containing a JSON string of
 * two addresses; you can include up to 100 in a
 * POST request.
 *
 * http://smartystreets.com/products/liveaddress-api
 *
 * INSTRUCTIONS: Put a REST authentication token (URL-encoded!) from your
 * SmartyStreets account into the "authToken" variable below.
 * Make sure json-simple is loaded.
**/

import java.io.*;
import java.net.*;
import java.util.*;
import org.json.simple.parser.*;
import org.json.simple.*;

public class LiveAddressExample
{
	public static void main(String[] args)
	{

		// Put your authentication token here (don't forget you need the encoded form)
		String authToken = "PUT_AUTHENTICATION_TOKEN_HERE";

		// The REST endpoint
		String url = "https://api.qualifiedaddress.com/street-address/?auth-token=" + authToken;
		
		String response = ""; // Declared here for scope

		// A couple sample addresses
		JSONObject addr1 = new JSONObject();
		addr1.put("street", "3785 s las vegs av.");
		addr1.put("city", "los vegas,");
		addr1.put("state", "nevada");
		
		JSONObject addr2 = new JSONObject();
		addr2.put("street", "1600 ampitheatre parkway");
		addr2.put("city", "mtn view");
		addr2.put("state", "california");
		addr2.put("zip", "94043");

		// Build each address into the JSON array
		JSONArray list = new JSONArray();
		list.add(addr1);
		list.add(addr2);

		// The request to send to the server
		String req = list.toString();
		int len = req.length();
		
		try
		{
			URL u = new URL(url);
			
			try
			{
				// Establish connection, stream our JSON string, and close the connection.
				URLConnection urlConn = u.openConnection();
				urlConn.setDoInput(true);
				urlConn.setDoOutput(true);
				urlConn.setUseCaches(false);
				urlConn.setRequestProperty("Content-Length", Integer.toString(len));
				
				DataOutputStream outgoing = new DataOutputStream(urlConn.getOutputStream());
				String content = req;
				outgoing.writeBytes(content);
				outgoing.flush();
				outgoing.close();

				// Save the response (a JSON string)
				DataInputStream incoming = new DataInputStream(urlConn.getInputStream());
				String str;
				while ((str = incoming.readLine()) != null)
					response += str;
				incoming.close();
			}
			catch(IOException e)
			{
				System.out.println("IO Exception Error: " + e.toString());
			}
		}
		catch (MalformedURLException m)
		{
			System.out.println("Malformed URL Exception Error: " + m.toString());
		}
		
		// Parse the JSON string into a JSON array
		Object obj = JSONValue.parse(response);
		JSONArray json = (JSONArray)obj;


		
		// For each address returned in the array, parse it into an
		// object and output the verified address. This is only a
		// rudimentary sample usage of the json-simple library.
		// Remember that LiveAddress returns *many* fields with useful
		// data. This is only a demonstration of how to access it.
		
		for (int i = 0; i < json.size(); i++)
		{
			JSONObject addr = (JSONObject)json.get(i);
			
			System.out.println(addr.get("delivery_line_1"));
			System.out.println(addr.get("last_line") + "\r\n");
		}
	}
}
