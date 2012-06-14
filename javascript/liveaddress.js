/*

LiveAddress API Interface for Javascript (unofficial)
by SmartyStreets
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

A helpful library for using LiveAddress while abstracting
away the JSONP requests and other lower-level operations.
We advise against using this code in production without
thorough testing in your own system. This library does not
handle the raw JSON output except return it to your calling
functions. No jQuery dependencies required.

Always call "LiveAddress.init(12345678)" first, replacing
"12345678" with your HTML identifier. Then for each call
to LiveAddress, supply a callback function to handle
the output.


EXAMPLES
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(When you pass in an address, you can pass in an object
which maps fields to their values, a string being a freeform
address, a string being the ID of an HTML input/textarea
element which contains a value, or an array of any of the
above to do asyncrhonous batch requests.)

LiveAddress.verify({
	street: "123 main",
	street2: "apt 105",
	city: "denver",
	state: "colorado",
	zipcode: "12345"
}, function(json) { ... });


LiveAddress.verify("123 main st, 12345", function(json) {
	// 'json' contains the complete raw JSON response
	...
});


LiveAddress.geocode("address-textbox", function(coord) {
	// 'coord' is a string like: "35.05613, -115.10234"
	...
});


LiveAddress.county("500 fir, denver co", function(cty) {
	// 'cty' contains the county name
	...
});


LiveAddress.components("123 main 12345", function(comp) {
	// 'comp' is the components of a freeform address
	...
});


*/


var LiveAddress = (function()
{
	var _id;
	var _requests = [];
	var _requestID = 0;

	function _buildFreeformRequest(addr, callback, wrapper)
	{
		// Here we expect addr to be a string (ID or actual address)
		var elem = document.getElementById(addr);
		return _buildComponentizedRequest({
			street: (elem ? elem.value : addr)
		}, callback, wrapper);
	}

	function _buildComponentizedRequest(addr, callback, wrapper)
	{
		// We expect addr to be an object, mapping fields to values
		if (!addr)
			return null;

		var request = {};
		request.addresses = addr instanceof Array ? addr : [addr];
		request.id = "req_" + (_requestID++) + "_" + new Date().getTime();
		request.callback = function(response) { LiveAddress.callback(request.id, response); };
		request.wrap = wrapper || function(data) { return data; };
		request.userCallback = callback;
		request.returnCount = 0;
		request.json = [];
		request.DOM = [];

		_requests[request.id] = request;
		return request.id;
	}

	function _queryString(address, id)
	{
		var qs = "?auth-token=" + encodeURIComponent(_id);
		for (prop in address)
			qs += "&" + prop + "=" + encodeURIComponent(address[prop]);
		qs += "&callback=LiveAddress.requests()." + id + ".callback";
		return qs;
	}

	function _request(reqid)
	{
		for (idx in _requests[reqid].addresses)
		{
			var dom = document.createElement("script");
			dom.src = "https://api.qualifiedaddress.com/street-address/"
				+ _queryString(_requests[reqid].addresses[idx], reqid);
			document.body.appendChild(dom);
			_requests[reqid].DOM[idx] = dom;
		}
	}




	return {
		init: function(identifier)
		{
			_id = encodeURIComponent(identifier);
		},

		verify: function(addr, callback, wrapper)
		{
			var reqid;

			if (typeof addr === "string")
				reqid = _buildFreeformRequest(addr, callback, wrapper);

			else if (typeof addr === "object" && !(addr instanceof Array))
				reqid = _buildComponentizedRequest(addr, callback, wrapper);

			else if (addr instanceof Array)
			{
				// Batch request
				var addresses = [];
				for (idx in addr)
				{
					if (typeof addr[idx] == "string")
					{
						var elem = document.getElementById(addr);
						addresses.push({ street: (elem ? elem.value : addr[idx]) });
					}
					else
						addresses.push(addr[idx]);
				}
				reqid = _buildComponentizedRequest(addresses, callback, wrapper);
			}

			_request(reqid);
		},

		coords: function(address)
		{
			if (!address)
				return {};

			return {
				lat: address.metadata.latitude,
				lon: address.metadata.longitude
			};
		},

		coordinates: function(address)
		{
			if (!address)
				return undefined;

			return address.metadata.latitude + ", " + address.metadata.longitude;
		},

		requests: function()
		{
			return _requests;
		},

		geocode: function(addr, callback)
		{
			this.verify(addr, callback, function(data) {
				return LiveAddress.coordinates(data[0]);
			});
		},

		components: function(addr, callback)
		{
			this.verify(addr, callback, function(data) {
				var comp = [];
				for (idx in data)
				{
					data[idx].components.street_line1 = data[idx].delivery_line_1;
					comp.push(data[idx].components);
				}
				return comp;
			});
		},

		county: function(addr, callback)
		{
			this.verify(addr, callback, function(data) {
				return data[0].metadata.county_name;
			});
		},

		callback: function(reqid, data)
		{
			var request = _requests[reqid];

			request.json = request.json.concat(data);

			if (++request.returnCount == request.addresses.length)
			{
				var result = request.userCallback(request.wrap(request.json));
				for (idx in request.DOM)
					document.body.removeChild(request.DOM[idx]);
				delete request;
				return result;
			}
		}
	};

})();