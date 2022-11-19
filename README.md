# Washing Machine Dashboard
This is a dashboard that the users can use to check which washing machines are free.

# Sensors used
- Current sensor (WCS1800)

# Functions
- Fetches data from the OM2M server and displays the following data for each washing machine:
	- Current state: `Spin` or `Rinse` or `Wash` or `Standby` or `Off`

# How it works
- Backend (`flask`) ' 
	- Sends `GET` and `POST` requests to OM2M server
	- `json` data format is used for interoperability
- Frontend (`html+css+js`)
	<!-- - `Chart.js` is used for drawing beautiful charts -->
	- Updates data every 2 seconds using `js`

# Setup
- install `flask`
```
$ pip install flask
```
- run `app.py`
```
$ python3 app.py
```