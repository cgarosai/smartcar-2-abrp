from flask import current_app, request
import time
import requests
WAIT_TIME_SECONDS = 10

abrpURL = "https://api.iternio.com/1/tlm/send"
def sendData():
    while current_app.isRunning
        try:
            if current_app.token is None:
                logger.debug("No abrp token provided")
            elif current_app.vehicle:
                batteryPercent = current_app.vehicle.battery().percentRemaining
                isCharging = current_app.vehicle.charge().isPluggedIn
                location = current_app.vehicle.location()

                tlm = {"utc": int(datetime.timestamp(energy.updated_at)),
                        "current": batteryPercent,
                        "is_charging": isCharging == "InProgress",
                        "lat": location.Latitude,
                        "lon": location.Longitude
                        }
                params = {"tlm": json.dumps(tlm), "token": current_app.abrpToken, "api_key": current_app.api_key}
                response = requests.request("POST", , params=params)
        except:
            continue
        time.sleep(WAIT_TIME_SECONDS)









