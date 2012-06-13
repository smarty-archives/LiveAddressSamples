/*
 *
 * A sample Javascript interface for using the LiveAddress API.
 * This example doesn't require jQuery.
 *
 * This sample is not officially supported by us but is a convenient
 * way to begin implementing the API on your site and experimenting.
 *
 * -- Basic Instructions --
 * Always call LiveAddress.init(123456789) first, replacing "123456789"
 * with your own access identifier from your SmartyStreets settings.
 *
 * You can call LiveAddress.verify() and pass in an object:
 * LiveAddress.verify({ street: "123 main", zip: "12345" });
 *
 * Or you can pass in the ID of a textbox/area of a single-line address:
 * LiveAddress.verify('address');
 *
 * Or you can call geocode to get the coordinates as a string:
 * LiveAddress.geocode('address');
 *
 * Note that both of these functions require a callback function as
 * the second argument if you want to do anything with the JSON response.
 */

var LiveAddress = (function()
{
	var _id;
	var _requests = [];
	var _requestID = 0;

	function _buildRequest(addr, callback, wrapper)
	{
		var request = {};

		if (!addr)
			return null;

		request.id = "req_" + (_requestID++) + "_" + new Date().getTime();
		request.street = addr.street || "";
		request.street2 = addr.street2 || "";
		request.city = addr.city || "";
		request.state = addr.state || "";
		request.zip = addr.zip || "";
		request.callback = function(response) { LiveAddress.callback(request.id, response); };
		request.wrap = wrapper || function(data) { return data; };
		request.userCallback = callback;
		request.queryString = "?auth-token=" + encodeURIComponent(_id)
			+ "&street=" + encodeURIComponent(request.street)
			+ "&street2=" + encodeURIComponent(request.street2)
			+ "&city=" + encodeURIComponent(request.city)
			+ "&state=" + encodeURIComponent(request.state)
			+ "&zip=" + encodeURIComponent(request.zip)
			+ "&callback=LiveAddress.requests()." + request.id + ".callback";

		_requests[request.id] = request;

		return request.id;
	}

	function _request(reqid)
	{
		_requests[reqid].DOM = document.createElement("script");
	    _requests[reqid].DOM.src = "https://api.qualifiedaddress.com/street-address/"
	    	+ _requests[reqid].queryString;
	    document.body.appendChild(_requests[reqid].DOM);
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
			{
				var elem = document.getElementById(addr);
				reqid = _buildRequest({
					street: (elem ? elem.value : addr)
				}, callback, wrapper);
			}
			else if (typeof addr === "object")
				reqid = _buildRequest(addr, callback, wrapper);

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
			var result = _requests[reqid].userCallback(_requests[reqid].wrap(data));
			document.body.removeChild(_requests[reqid].DOM);
			delete _requests[reqid];
			return result;
		}
	};

})();