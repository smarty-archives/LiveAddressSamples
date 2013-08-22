/*

LiveAddress API Interface for Javascript (unofficial)
by SmartyStreets
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

A helpful library for using LiveAddress while abstracting
away the JSONP requests and other lower-level operations.
We advise against using this code in production without
thorough testing in your own system. This library does not
handle the raw JSON output except return it to your calling
functions. No other dependencies required (not even jQuery).

Always call "LiveAddress.init('1234567...')" first, replacing
"1234567..." with your HTML key. Then for each call
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


LiveAddress.geocode("address-textbox", function(geo) {
	// 'geo' is an object: lat, lon, coords, precision
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


You can also pass in a timeout callback as the last parameter,
which is executed in case the query times out (a timeout is 3
failed attempts, where we wait 3.5 seconds for each one). The
input values are passed back to the timeout function as they were
received (except if a string was passed in the value comes
back as an object with the string in the "street" field.)

*/


var LiveAddress = (function()
{
	var _id, _token;
	var _requests = {};
	var _batches = {};
	var _timers = {};
	var _counter = 0;
	var _candidates = 5;	// You can customize this: maximum results per address
	var _timeout = 3500;	// Milliseconds until a timeout is counted ("1 attempt")
	var _maxAttempts = 3;	// Maximum number of attempts for a single request before finally timing out

	function _buildFreeformRequest(addr, callback, timeout, wrapper)
	{
		// Here we expect addr to be a string (ID or actual address)
		var elem = document.getElementById(addr);
		return _buildComponentizedRequest({ street: (elem ? elem.value : addr) }, callback, timeout, wrapper);
	}

	function _buildComponentizedRequest(addr, callback, timeout, wrapper)
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
			wrap: wrapper || function(data) { return data; }
		};

		for (var idx in addr)
			reqids.push(_buildRequest(addr[idx], batch_id, idx, timeout));

		return reqids;
	}

	function _buildRequest(addr, batch_id, index, timeout)
	{
		var address = { fields: addr };

		address.id = "addr_" + (_counter++);
		address.inputIndex = parseInt(index, 10);
		address.json = [];
		address.batch = batch_id;
		address.userTimeout = timeout;
		address.callback = function(response) { _callback(address.id, response); };
		_requests[address.id] = address;
		return address.id;
	}

	function _queryString(reqid)
	{
		var request = _requests[reqid], qs;
		if (_id && _token)
			qs = "?auth-id=" + _id + "&auth-token=" + _token + "&candidates=" + _candidates;
		else
			qs = "?auth-token=" + _id + "&candidates=" + _candidates;
		for (var prop in request.fields)
			qs += "&" + prop + "=" + encodeURIComponent(request.fields[prop]);
		qs += "&callback=" + encodeURIComponent("LiveAddress.request(\"" + reqid + "\").callback");
		return qs;
	}

	function _request(reqids)
	{
		for (var i in reqids)
		{
			var dom = document.createElement("script");
			dom.src = "https://api.smartystreets.com/street-address"
				+ _queryString(reqids[i]);
			document.getElementsByTagName('head')[0].appendChild(dom);
			_requests[reqids[i]].DOM = dom;
			_timers[reqids[i]] = {
				attempts: _timers[reqids[i]] ? _timers[reqids[i]].attempts || 0 : 0,
				timeoutID: setTimeout(_timeoutHandler(reqids[i]), _timeout)
			};
		}
	}

	function _callback(reqid, data)
	{
		var request = _requests[reqid];
		var batch = _batches[request.batch];

		for (var i in data)
			data[i].input_index = request.inputIndex;
		batch.json = batch.json.concat(data);

		document.getElementsByTagName('head')[0].removeChild(request.DOM);
		delete _requests[reqid];

		clearTimeout(_timers[reqid].timeoutID);
		delete _timers[reqid];

		if (++batch.returned == batch.size)
		{
			var result = batch.userCallback(batch.wrap(batch.json));
			delete _batches[request.batch];
			return result;
		}
	}

	function _timeoutHandler(reqid)
	{
		return function()
		{
			if (++_timers[reqid].attempts < _maxAttempts)
				_request([reqid]);
			else if (typeof _requests[reqid].userTimeout === 'function')
				_requests[reqid].userTimeout(_requests[reqid].fields);
		};
	}

	function _coordinates(responseAddress)
	{
		if (!responseAddress || typeof responseAddress !== 'object')
			return undefined;

		return {
			lat: responseAddress.metadata.latitude,
			lon: responseAddress.metadata.longitude,
			precision: responseAddress.metadata.precision,
			coords: responseAddress.metadata.latitude + ", " + responseAddress.metadata.longitude
		};
	}






	return {
		init: function(authId, authToken)
		{
			_id = encodeURIComponent(authId || "");
			_token = encodeURIComponent(authToken || "");
		},

		verify: function(addr, callback, timeout, wrapper)
		{
			var reqids;

			if (typeof addr === "string")
				reqids = _buildFreeformRequest(addr, callback, timeout, wrapper);

			else if (typeof addr === "object" && !(addr instanceof Array))
				reqids = _buildComponentizedRequest(addr, callback, timeout, wrapper);

			else if (addr instanceof Array)
			{
				var addresses = [];		// Batch request
				for (var idx in addr)
				{
					if (typeof addr[idx] == "string")
					{
						var elem = document.getElementById(addr);
						addresses.push({ street: (elem ? elem.value : addr[idx]) });
					}
					else
						addresses.push(addr[idx]);
				}
				reqids = _buildComponentizedRequest(addresses, callback, timeout, wrapper);
			}

			_request(reqids);
		},

		request: function(reqid)	// For internal use only; must be accessible from the outside (when a JSONP request succeeds)
		{
			return _requests[reqid];
		},

		geocode: function(addr, callback, timeout)
		{
			this.verify(addr, callback, timeout, function(data)
			{
				if (data.length == 1)
					return _coordinates(data[0]);
				else
				{
					var coords = [];
					for (var i in data)
						coords.push(_coordinates(data[i]));
					return coords;
				}
			});
		},

		components: function(addr, callback, timeout)
		{
			this.verify(addr, callback, timeout, function(data)
			{
				var comp = [];
				for (var idx in data)
				{
					data[idx].components.first_line = data[idx].delivery_line_1;
					if (typeof data[idx].delivery_line_2 !== "undefined")
						data[idx].components.first_line += " " + data[idx].delivery_line_2;
					data[idx].components.last_line = data[idx].last_line;
					if (typeof data[idx].addressee !== "undefined")
						data[idx].components.addressee = data[idx].addressee;
					comp.push(data[idx].components);
				}
				return comp;
			});
		},

		county: function(addr, callback, timeout)
		{
			this.verify(addr, callback, timeout, function(data) {
				return data[0].metadata.county_name;
			});
		}
	};

})();