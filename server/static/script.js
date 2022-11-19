function send(data) {
	fetch("/", {
		method: "POST",
		body: new URLSearchParams(data)
	})
	renew()
}
if (window.history.replaceState)
	window.history.replaceState(null, null, window.location.href)
const default_chart = {
	type: 'line',
	data: {
		labels: ['', '', '', '', ''],
		datasets: [{
			data: [],
			backgroundColor: '#055160',
			tension: 0.4
		}]
	},
	options: {
		responsive: true,
		plugins: {
			legend: {
				display: false,
			}
		},
		scales: {
			"y": {
				suggestedMin: 0,
				suggestedMax: 100
			}
		}
	}
}
const sensors = {
	"Node1": "#20c997", "Node2": "#0d6efd", "Node3": "#d63384", "Node4": "#d63384"
}
let manual = 0
for (let sensor in sensors)
	document.getElementById("charts").innerHTML += `
	<div class="col">
		<div class="alert alert-info" role="alert">
			<h5 class="alert-heading">${sensor}</h5>
			<div class="text-end" id="${sensor}-data"></div>
			<canvas id="${sensor}" width="400" height="200"></canvas>
		</div>
	</div>
	`

for (let sensor in sensors)
	new Chart(sensor, Object.assign({}, default_chart))


function renew() {
	document.getElementById(`connected`).hidden = 0
	document.getElementById(`not-connected`).hidden = 1
	console.log("fetching")
	fetch("data").then(e => e.json()).then(e => {
		for (let sensor in sensors) {
			const chart_data = Chart.getChart(sensor).data
			chart_data.datasets[0].backgroundColor = sensors[sensor]
			chart_data.datasets[0].data = e.chart[sensor][0]
			chart_data.labels = e.chart[sensor][1]
			Chart.getChart(sensor).update()
			document.getElementById(`${sensor}-data`).innerText = e.data[sensor]
		}
		document.getElementById(`Status-data`).innerText = e.protector["status_str"]
		if (manual == 0) {
			document.getElementById(`panel`).checked = !e.protector["status"]
		}
		document.getElementById(`Error-data`).innerHTML = e.data["_error"] + e.protector["_error"]
		document.getElementById(`Error-box`).hidden = e.data["_error"] == '' && e.protector["_error"] == ''
		console.log(e)
	}).catch(e => {
		document.getElementById(`connected`).hidden = 1
		document.getElementById(`not-connected`).hidden = 0
	})
	console.log("fetched")

	if (manual > 0) manual--
}
setInterval(renew, 2000)
renew()