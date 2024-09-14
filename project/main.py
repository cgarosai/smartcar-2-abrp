import smartcar
from flask import Flask, redirect, render_template, request, jsonify, Blueprint, url_for, current_app
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    else:
        return render_template('index.html', running=current_app.isRunning, year=current_app.year)

@main.route("/run")
@login_required
def run():
    if current_app.isRunning:
        # Stop our thread giving ABRP live data
        current_app.isRunning = False

    else:
        # Start by getting access code
        if current_app.access == None:
            scope = ["read_vehicle_info", "read_location", "read_battery", "read_charge"]
            auth_url = current_app.client.get_auth_url(scope)
            return redirect(auth_url)

    return redirect(url_for('main.index'))

@main.route("/get_access")
@login_required
def get_access():
    if request.args.get("code"):
        current_app.access = current_app.client.exchange_code(request.args.get("code"))
        idVehicle = smartcar.get_vehicles(current_app.access.access_token).vehicles[0]
        current_app.vehicle = smartcar.Vehicle(idVehicle, current_app.access.access_token)
        current_app.isRunning = True
        return redirect(url_for('main.index'))
    else:
        return redirect(url_for('main.error'))

@main.route('/error')
def error():
    return render_template('error.html')
