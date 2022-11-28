let WM = []

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
				suggestedMax: 5
			}
		}
	}
}
const sensors = {
	"Machine-1": "#20c997", "Machine-2": "#0d6efd", "Machine-3": "#d63384", "Machine-4": "#d63384"
}
let manual = 0
for (let sensor in sensors) {
	document.getElementById("charts").innerHTML += `
	<div class="col">
		<div class="alert alert-info" role="alert">
			<h5 class="alert-heading">${sensor}</h5>
			<div class="text-end" id="${sensor}-data"></div>
			<canvas id="${sensor}" width="400" height="200" ></canvas>
			<div id="wrapper">	
				<div id="washing${sensor}" class="wm isOpen">
					<div id="controls${sensor}" class="wm-controls">READY</div>
					<div id="door${sensor}" class="wm-door"></div>
					<div id="tub${sensor}" class="wm-tub">
						<span class="clothes"></span>
						<span class="clothes"></span>
						<span class="clothes"></span>
					</div>
				</div>
			</div>
		</div>
	</div>`
}

for (let sensor in sensors) {
	new Chart(sensor, Object.assign({}, default_chart))
	WM[sensor] = document.getElementById(`washing${sensor}`)
}


function renew() {
	document.getElementById(`connected`).hidden = 0
	document.getElementById(`not-connected`).hidden = 1
	fetch("data").then(e => e.json()).then(e => {
		for (let sensor in sensors) {
			const chart_data = Chart.getChart(sensor).data
			chart_data.datasets[0].backgroundColor = sensors[sensor]
			chart_data.datasets[0].data = e.chart[sensor][0]
			chart_data.labels = e.chart[sensor][1]
			Chart.getChart(sensor).update()
			document.getElementById(`${sensor}-data`).innerText = e.data[sensor]
			WM_set(sensor, e.data[sensor] == "On", e.data[sensor])
		}
		// document.getElementById(`Status-data`).innerText = e.data["_status_str"]
		// if (manual == 0) {
		// 	document.getElementById(`panel`).checked = !e.data["_status"]
		// }
		document.getElementById(`Error-data`).innerHTML = e.data["_error"]
		document.getElementById(`Error-box`).hidden = e.data["_error"] == ''
		console.log(e)
	}).catch(e => {
		document.getElementById(`connected`).hidden = 1
		document.getElementById(`not-connected`).hidden = 0
	})

	if (manual > 0) manual--
}
setInterval(renew, 2000)
renew()

//queue------------------------------------------------------------

function joinqueue() {
	fetch(`joinqueue`).then(e => e.json()).then(e => {
		if (e.status) alert(e.status)
	})
}

function leavequeue() {
	fetch(`leavequeue`).then(e => e.json()).then(e => {
		if (e.status) alert(e.status)
	})
}

function render_queue() {
	fetch(`queue`).then(e => e.json()).then(e => {
		let yourtoken = e.token ? `
		<h2>Your token: <span class="badge bg-success">${e.token}</span></h2>
		`: ''
		document.getElementById(`joinqbtn`).disabled = e.token
		document.getElementById(`leaveqbtn`).disabled = !e.token
		let html = ''
		for (let student in e.queue) {
			html += `
<li class="list-group-item d-flex justify-content-between align-items-center ${e.queue[student].token == e.token ? 'list-group-item-success' : ''}">
	${e.queue[student].token}
	<span class="badge bg-primary rounded-pill">${e.queue[student].time}</span>
</li>`
		}
		document.getElementById(`queue`).innerHTML = yourtoken + html
	})

}
setInterval(render_queue, 2000)
render_queue()

//washing machine------------------------------------------------------------

const WM_washspeed = 600 // If changed, need to be updated in the CSS as well

function WM_set_door(sensor, status) {
	let wm = document.getElementById(`washing${sensor}`)
	wm.classList.toggle("isOpen", status)
	wm.classList.toggle("isFilled", !status)
}

function WM_set_washing(sensor, status) {
	let wm = document.getElementById(`washing${sensor}`)
	wm.classList.toggle("isWashing", status)
	if (status && !wm.classList.contains("isWashing")) {
		wm.classList.add("isStarting")
		setTimeout(() => {
			wm.classList.remove("isStarting")
		}, WM_washspeed * 2)
	}
}

function WM_set_text(sensor, text) {
	document.getElementById(`controls${sensor}`).innerText = text
}

function WM_set(sensor, setting, text) {
	WM_set_door(sensor, !setting)
	WM_set_washing(sensor, setting)
	WM_set_text(sensor, text)
}