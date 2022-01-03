var Urll = JSON.parse(document.getElementById('name').textContent);

function formatUptime(uptime) {
	var seconds = uptime % 60;
	uptime /= 60;
	var minutes = uptime % 60;
	uptime /= 60;
	var hours = uptime % 24;
	uptime /= 24;
	var days = uptime;
	return (Math.floor(days) + "d "
				+ ("0" + Math.floor(hours)).substr(-2) + ":"
				+ ("0" + Math.floor(minutes)).substr(-2) + ":"
				+ ("0" + Math.floor(seconds)).substr(-2));
}

function formatValue(value, defaultPrecision, valueUnit) {
	if (value >= 1000000000)
		return ((value / 1000000000).toFixed(2) + " G" + valueUnit);
	else if (value >= 1000000)
		return ((value / 1000000).toFixed(2) + " M" + valueUnit);
	else if (value >= 1000)
		return ((value / 1000).toFixed(2) + " K" + valueUnit);
	else
		return (value.toFixed(defaultPrecision) + " " + valueUnit);
}

function createDeviceStatTable(deviceCount) {
	var deviceStatTable = document.getElementById("device_stat");
	var rows = deviceStatTable.rows;
	for (var i = deviceStatTable.rows.length - 2; i > 1; --i)
		deviceStatTable.removeChild(rows[i]);
	for (var i = 0; i < deviceCount; ++i) {
		var row = deviceStatTable.insertRow(i + 2);
		for (var j = 0; j < 10; ++j)		
			row.insertCell(-1);
		row.id = "GPU" + i;	
		row.cells[0].className = "column_title";
		var temperatureCell = row.cells[3];
		temperatureCell.appendChild(document.createElement("span"));
		temperatureCell.appendChild(document.createElement("span"));
		temperatureCell.appendChild(document.createElement("span"));
	}
}

function temperatureColor(temperature, temperatureLimit) {
	var temperatureLimit1 = Math.floor(temperatureLimit * 0.9);
	var temperatureLimit2 = Math.floor(temperatureLimit * 0.8);
	if (temperature < temperatureLimit2)
		return "text_green";
	if (temperature < temperatureLimit1)
		return "text_yellow";
	return "text_red";
}

function updateStatistics(data) {
	var statusCell = document.getElementById("status");
	var extendedShareInfo = data.extended_share_info;
	statusCell.innerText = "Online";
	statusCell.className = "text_green";
	document.getElementById("miner_name").innerText = data.miner;
	document.getElementById("uptime").innerText = formatUptime(data.uptime);
	document.getElementById("pool_hashrate").innerText = formatValue(data.pool_speed, data.speed_rate_precision, data.speed_unit);
	document.getElementById("shares_per_minute").innerText = data.shares_per_minute.toFixed(2);
	document.getElementById("algorithm").innerText = data.algorithm;
	var electricityStr;
	if (data.electricity != 0) {
		electricityStr = data.electricity.toFixed(3) + " kWh";
		if (data.electricity_cost != null)
			electricityStr += " $" + data.electricity_cost.toFixed(2);
	} else
		electricityStr = "N/A";
	document.getElementById("electricity").innerText = electricityStr;
	document.getElementById("server").innerText = (data.server == null ? "N/A" : data.server);
	document.getElementById("user").innerText = (data.user == null ? "N/A" : data.user);

	var totalSpeed = 0;
	var totalSpeed2 = 0;
	var totalSpeedPower = 0;
	var totalPowerUsage = 0;
	var totalAcceptedShares = 0;
	var totalAcceptedShares2 = 0;
	var totalStaleShares = 0;
	var totalStaleShares2 = 0;
	var totalInvalidShares = 0;
	var totalInvalidShares2 = 0;
	var dualMode = (data.total_accepted_shares2 != null);
	
	var deviceStatTable = document.getElementById("device_stat");
	deviceStatTable.style.display = "table";
	
	for (var deviceIndex = 0; deviceIndex < data.devices.length; ++deviceIndex) {
		var device = data.devices[deviceIndex];
		var row = document.getElementById("GPU" + deviceIndex);
		var cells = row.cells;
		cells[0].innerText = device.gpu_id;
		cells[1].innerText = device.name;
		cells[2].innerText = device.fan + " %";
		if (device.temperature == 0) {
			cells[3].innerText = "N/A";
			cells[3].className = null;		
		} else {
			var temperatureChilds = cells[3].childNodes;
			temperatureChilds[0].innerText = device.temperature + " C";
			temperatureChilds[0].className = temperatureColor(device.temperature, device.temperature_limit);
			if (device.memory_temperature != 0) {
				temperatureChilds[1].innerText = " / ";
				temperatureChilds[2].innerText = device.memory_temperature + " C";
				temperatureChilds[2].className = temperatureColor(device.memory_temperature, device.memory_temperature_limit);
			} else {
				temperatureChilds[1].innerText = null;
				temperatureChilds[2].innerText = null;
			}
		}
		cells[4].innerText = formatValue(device.speed, data.speed_rate_precision, data.speed_unit);
		totalSpeed += device.speed;
		if (dualMode) {
			cells[4].innerText += " + " + formatValue(device.speed2, data.speed_rate_precision2, data.speed_unit2);
			totalSpeed2 += device.speed2;
		}
		if (device.accepted_shares != null) {
			if (extendedShareInfo)
				cells[5].innerText = device.accepted_shares + " / " + device.stale_shares + " / " + device.invalid_shares;
			else
				cells[5].innerText = device.accepted_shares + " / " + device.rejected_shares;
			totalAcceptedShares += device.accepted_shares;
			totalStaleShares += device.stale_shares;
			totalInvalidShares += device.invalid_shares;
			if (dualMode) {
				if (extendedShareInfo)
					cells[5].innerText += " + " + device.accepted_shares2 + " / " + device.stale_shares2 + " / " + device.invalid_shares2;
				else
					cells[5].innerText += " + " + device.accepted_shares2 + " / " + device.rejected_shares2;
				totalAcceptedShares2 += device.accepted_shares2;
				totalStaleShares2 += device.stale_shares2;
				totalInvalidShares2 += device.invalid_shares2;
			}
		} else
			cells[5].innerText = "-";
		cells[6].innerText = device.core_clock;
		cells[7].innerText = device.memory_clock;
		if (device.power_usage != 0) {
			cells[8].innerText = device.power_usage + " W";
			cells[9].innerText = formatValue((device.speed / device.power_usage), 2, data.power_unit);
			totalSpeedPower += device.speed;
			totalPowerUsage += device.power_usage;
		} else {
			cells[8].innerText = "N/A";
			cells[9].innerText = "N/A";
		}
	}
	var row = document.getElementById("total");
	var cells = row.cells;
	cells[4].innerText = formatValue(totalSpeed, data.speed_rate_precision, data.speed_unit);
	if (dualMode)
		cells[4].innerText += " + " + formatValue(totalSpeed2, data.speed_rate_precision2, data.speed_unit2);
	if (totalPowerUsage != 0) {
		cells[8].innerText = totalPowerUsage + " W";
		cells[9].innerText = formatValue((totalSpeedPower / totalPowerUsage), 2, data.power_unit);
	} else {
		cells[8].innerText = "N/A";
		cells[9].innerText = "N/A";
	}
	if (extendedShareInfo) {
		cells[5].innerText = totalAcceptedShares + " / " + totalStaleShares + " / " + totalInvalidShares;
		if (dualMode)
			cells[5].innerText += totalAcceptedShares2 + " / " + totalStaleShares2 + " / " + totalInvalidShares2;
	} else {
		cells[5].innerText = totalAcceptedShares + " / " + (totalStaleShares + totalInvalidShares);
		if (dualMode)
			cells[5].innerText += totalAcceptedShares2 + " / " + (totalStaleShares2 + totalInvalidShares2);
	}
}

function minerDisconnected() {
	var statusCell = document.getElementById("status");
	statusCell.innerText = "Offline";
	statusCell.className = "text_red";
	document.getElementById("miner_name").innerText = "Miner";
	document.getElementById("uptime").innerText = "N/A";
	document.getElementById("pool_hashrate").innerText = "N/A";
	document.getElementById("shares_per_minute").innerText = "N/A";
	document.getElementById("algorithm").innerText = "N/A";
	document.getElementById("electricity").innerText = "N/A";
	document.getElementById("server").innerText = "N/A";
	document.getElementById("user").innerText = "N/A";
	var deviceStatTable = document.getElementById("device_stat");
	deviceStatTable.style.display = "none";
}

function showError(message) {
	error = document.getElementById("error");
	error.innerText = message;
	error.style.display = "block";
	var minerStatTable = document.getElementById("miner_stat");
	minerStatTable.style.display = "none";
	var deviceStatTable = document.getElementById("device_stat");
	deviceStatTable.style.display = "none";
}

var httpRequest = null;
var requestTime = null;
// var Urll = '/stat';
// const DCT = JSON.parse(document.getElementById('hello-data').textContent);
// var input2 = document.getElementById("searchTxt").valueOf();
console.log(Urll);
function update() {
	requestTime = (new Date).getTime();
	httpRequest.open('GET', Urll, true);
    httpRequest.send(null);
}

function onLoad() {
	var deviceStatTable = document.getElementById("device_stat");
	if (!window.XMLHttpRequest) {
		showError("Your browser does not support XMLHttpRequest");
		return;
	}
	httpRequest = new XMLHttpRequest();
	if (!httpRequest) {
		showError("Your browser does not support XMLHttpRequest");
		return;
	}
	httpRequest.timeout = 5000;
	httpRequest.ontimeout = function() {
		minerDisconnected();
		setTimeout(update, 1000);
 	};
	var deviceCount = 0;
	httpRequest.onreadystatechange = function() {
		if (httpRequest.readyState !== XMLHttpRequest.DONE)
			return;
		if (httpRequest.status !== 200 || httpRequest.responseText.length === 0) {
			minerDisconnected();
			setTimeout(update, 1000);
			return;
		}
		var data = window.JSON.parse(httpRequest.responseText);
		if (deviceCount !== data.devices.length) {
			deviceCount = data.devices.length;
			createDeviceStatTable(data.devices.length);		
		}
		updateStatistics(data);
		var currentTime = (new Date).getTime();
		var delay = 100000 - (currentTime - requestTime);
		setTimeout(update, delay > 0 ? delay : 1);
	};
	update();
}

window.onload = onLoad;
