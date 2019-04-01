from flask import Flask, render_template, request
app = Flask(__name__)


from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
kit.servo[0].set_pulse_width_range(600,2500)

v0 = 0
v1 = 0

volume0 = [3,18,32,46,60,74,90,105,121,136,151,167];
volume1 = [3,18,32,46,60,74,90,105,121,136,151,167];

kit.servo[0].angle = volume0[v0]
kit.servo[1].angle = volume1[v1]


@app.route("/")
def index():
   templateData = {
      'levels' : v0
      }
   return render_template('index.html', **templateData)

@app.route("/<levels>")
def action(levels):
    
    v0 = int(levels,10)
    kit.servo[0].angle = volume0[v0]
      
    templateData = {
    'levels' : v0
    }
      
    return render_template('index.html', **templateData)
      

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
