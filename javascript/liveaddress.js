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
	var _batches = {};
	var _counter = 0;

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
		// We expect addr to be at least one object, mapping fields to values
		if (!addr)
			return null;

		var reqids = [], batch = {};
		var batch_id = "batch_" + (_counter++);

		addr = addr instanceof Array ? addr : [addr];

		_batches[batch_id] = {
			size: addr.length,
			returned: 0,
			json: [],
			userCallback: callback,
			wrap: wrapper || function(data) { return data; },
		};

		for (var idx in addr)
			reqids.push(_buildRequest(addr[idx], batch_id, idx));

		return reqids;
	}

	function _buildRequest(addr, batch_id, index)
	{
		var address = { fields: addr };

		address.id = "addr_" + (_counter++);
		address.inputIndex = parseInt(index);
		address.json = [];
		address.batch = batch_id;
		address.callback = function(response) { LiveAddress.callback(address.id, response); }
		_requests[address.id] = address;

		return address.id;
	}

	function _queryString(reqid)
	{
		var request = _requests[reqid];
		var qs = "?auth-token=" + encodeURIComponent(_id);
		for (prop in request.fields)
			qs += "&" + prop + "=" + encodeURIComponent(request.fields[prop]);
		qs += "&callback=" + encodeURIComponent("LiveAddress.request(\"" + reqid + "\").callback");
		return qs;
	}

	function _request(reqids)
	{
		for (i in reqids)
		{
			var dom = document.createElement("script");
			dom.src = "https://api.qualifiedaddress.com/street-address/"
				+ _queryString(reqids[i]);
			document.body.appendChild(dom);
			_requests[reqids[i]].DOM = dom;
		}
	}






	return {
		init: function(identifier)
		{
			_id = encodeURIComponent(identifier);
		},

		verify: function(addr, callback, wrapper)
		{
			var reqids;

			if (typeof addr === "string")
				reqids = _buildFreeformRequest(addr, callback, wrapper);

			else if (typeof addr === "object" && !(addr instanceof Array))
				reqids = _buildComponentizedRequest(addr, callback, wrapper);

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
				reqids = _buildComponentizedRequest(addresses, callback, wrapper);
			}

			_request(reqids);
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

		request: function(reqid)
		{
			return _requests[reqid];
		},

		geocode: function(addr, callback)
		{
			this.verify(addr, callback, function(data) {

				if (data.length == 1)
					return LiveAddress.coordinates(data[0]);
				else
				{
					var coords = [];
					for (var i in data)
						coords.push(LiveAddress.coordinates(data[i]));
					return coords;
				}

			});
		},

		components: function(addr, callback)
		{
			this.verify(addr, callback, function(data) {
				var comp = [];
				for (idx in data)
				{
					data[idx].components.first_line = data[idx].delivery_line_1;
					if (typeof data[idx].delivery_line_2 !== "undefined")
						data[idx].components.first_line += " " + data[idx].delivery_line_2;
					data[idx].components.last_line = data[idx].last_line;
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
			var batch = _batches[request.batch];

			for (var i in data)
				data[i].input_index = request.inputIndex;
			batch.json = batch.json.concat(data);

			document.body.removeChild(request.DOM);
			delete _requests[reqid];

			if (++batch.returned == batch.size)
			{
				var result = batch.userCallback(batch.wrap(batch.json));
				delete _batches[request.batch];
				return result;
			}
		}
	};

})();