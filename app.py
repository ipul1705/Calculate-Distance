from flask import Flask, redirect, url_for, render_template, request
import requests
import json
import pprint as pp
import smtplib


app=Flask(__name__)

@app.route("/", methods = ["POST","GET"])
def index():
    if request.method == "POST" :
        origin = request.form["origin"]
        destination = request.form["destination"]
        return redirect(url_for("calculate", orig=origin, dest=destination))
    else:
        return render_template("index.html")

@app.route("/origin=<orig>&destination=<dest>")
def calculate(orig,dest):
    
    API_FILE = open("api-key.txt","r") 
    API_KEY = API_FILE.read()
    API_FILE.close()

    url1 = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="
    origin = orig
    url2 ="&destination="
    destination = dest
    url3 = "&mode=car&key="

    url_full = url1+origin+url2+destination+url3+API_KEY
    print(url_full)

    output = requests.get(url_full).json()

    pp.pprint(output)
    
    distance = ''
    duration = ''
    for obj in output['rows']:
        for data in obj['elements']:
            distance = data['distance']['text']
            duration = data['duration']['text']
            
            print('Distance : '+ distance)
            print('Duration : '+ duration)
    
    return render_template("calculate.html", distance=distance,duration=duration)
    
if __name__ == "__main__" :
    app.run(debug=True)
    



