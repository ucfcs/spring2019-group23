const request = require('request');
let baseAddy  = "https://api.darksky.net/forecast/";
let pass = "42fa7ad5cbb661f45bdc9a23fdbe25ec";
let long = "28.602437";
let lati = "-81.200071";
let apiCall = baseAddy + pass + "/" + long + "," + lati;

export function getCloudHeight() {
	return new Promise(function(resolve, reject) {
		request(apiCall, function (error, response, body) {
			if (!error && response.statusCode == 200) {
				let json = JSON.parse(body);
				let height = Number(1000 * (json.currently.temperature - json.currently.dewPoint) / 4.4, 2).toFixed(2);
				resolve(height);
			} else {
				reject()
			}
		});
	});
}