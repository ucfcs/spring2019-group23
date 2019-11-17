# Fetch weather data from DarkSky servers, compute cloud height and emit to server
# Usage: cronjob from 6a to 6p, every 5 minutes 
# */5 6-18 * * * /usr/bin/python3 cloud_height.py

import datetime
import requests
import socketio

# Initialize socket io
def initialize_socketio(url):
    sio = socketio.Client()

    @sio.event
    def connect():
        print("Connected to Application Server")

    @sio.event
    def disconnect():
        print("Disconnected from Application Server")

    sio.connect(url)
    return sio

# Calculate cloud-base height off of temperature & dew point
def calc_height(temp, dew):
    return (1000 * (temp - dew))/4.4


def main():
    # Initialize socket io connection to app server
    sock = initialize_socketio('http://cloudtrackingcloudserver.herokuapp.com/')
    # sock = initialize_socketio('http://localhost:3001/')

    parameters = {
        "pass": '42fa7ad5cbb661f45bdc9a23fdbe25ec',
        # TODO: Un-hardcode this location value
        "lat": 28.602437,
        "lon": -81.200071
    }

    # GET current weather data
    response = requests.get(f"https://api.darksky.net/forecast/{parameters['pass']}/{parameters['lat']},{parameters['lon']}?exclude=minutely,hourly,daily,alerts,flags")
    current = response.json()['currently']
    
    # Parse variables we're interested in
    t = current['temperature']
    dew = current['dewPoint']
    pressure = current['pressure']
    cbh = round(calc_height(t, dew), 2)

    # Prepare the payload
    data = {
        "temperature": t,
        "dew_point": dew,
        "barometric_pressure": pressure,
        "cloud_base_height": cbh
    }

    print("[", datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S"), "] Pressure:", pressure, "mb", "Temp:", t, "Dewpoint:", dew, "CBH =", cbh, "ft/F")

    # Emit to server and disconnect
    sock.emit('data', data)
    sock.disconnect()

main()