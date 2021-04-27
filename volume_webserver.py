from adafruit_servokit import ServoKit
import json
from time import sleep
from threading import Thread
from flask import Flask, render_template, request
app = Flask(__name__)


kit = ServoKit(channels=16)
kit.servo[0].set_pulse_width_range(600,2500)
kit.servo[1].set_pulse_width_range(580,2500) #note modified pulse range
kit.servo[2].set_pulse_width_range(600,2500)
kit.servo[3].set_pulse_width_range(600,2500)
kit.servo[4].set_pulse_width_range(600,2500)
kit.servo[5].set_pulse_width_range(600,2500)
kit.servo[6].set_pulse_width_range(600,2500)
kit.servo[7].set_pulse_width_range(600,2500)
kit.servo[8].set_pulse_width_range(600,2500)
kit.servo[9].set_pulse_width_range(600,2500)
volume0 = [3,18,32,46,60,74,90,105,121,136,151,167]; #OG servo angles
volume1 = [1,15,31,45,60,74,90,104,120,136,150,165];
volume2 = [3,17,32,46,59,73,88,104,117,133,149,164];
volume3 = [3,18,34,48,62,77,92,107,123,138,153,168];
volume4 = [2,16,31,44,61,76,89,104,119,132,145,159]; #try 160?
volume5 = [3,18,32,46,60,74,90,105,121,136,151,167];
volume6 = [3,18,32,46,60,74,90,105,121,136,151,167];
volume7 = [3,18,32,46,60,74,90,105,121,136,151,167];
volume8 = [3,18,32,46,60,74,90,105,121,136,151,167];
volume9 = [3,18,32,46,60,74,90,105,121,136,151,167];

pageload_count = 0 #global because it gets updated concurrently while other functions are using
levels_list = [0,0,0,0,0,0,0,0,0,0]
with open('data.txt') as json_file: #open data file with saved volume locations
    levels_list = json.load(json_file)

#kit.servo[0].angle = volume0[v0]
#set all servo angles
volume = levels_list[0]
kit.servo[0].angle = volume0[volume]
volume = levels_list[1]
kit.servo[1].angle = volume1[volume]
volume = levels_list[2]
kit.servo[2].angle = volume2[volume]
volume = levels_list[3]
kit.servo[3].angle = volume3[volume]
volume = levels_list[4]
kit.servo[4].angle = volume4[volume]
volume = levels_list[5]
kit.servo[5].angle = volume5[volume]
volume = levels_list[6]
kit.servo[6].angle = volume6[volume]
volume = levels_list[7]
kit.servo[7].angle = volume7[volume]
volume = levels_list[8]
kit.servo[8].angle = volume8[volume]
volume = levels_list[9]
kit.servo[9].angle = volume9[volume]

def timer_function(levels_list):
    #update save file, only if no updates have beeen made for 15 seconds
    global pageload_count
    loadcheck=pageload_count
    sleep(15)
    if loadcheck == pageload_count:
        print(levels_list)
        with open('data.txt', 'w') as outfile:
            json.dump(levels_list, outfile)
        
        print("Save File Successful")
    '''
    else:
        print("don't update save file")'''

@app.route("/")
def index():
   with open('data.txt') as json_file:
       levels_list = json.load(json_file)
        
   templateData = {
      'servo0' : levels_list[0],
      'servo1' : levels_list[1],
      'servo2' : levels_list[2],
      'servo3' : levels_list[3],
      'servo4' : levels_list[4],
      'servo5' : levels_list[5],
      'servo6' : levels_list[6],
      'servo7' : levels_list[7],
      'servo8' : levels_list[8],
      'servo9' : levels_list[9]
    }
   return render_template('index.html', **templateData)

@app.route("/<levels>/")
def action(levels):
    global pageload_count
    levels_list = list(levels.split(",")) #converts raw csv data from webpage into a list
    #converts list data from string type to int type
    levels_list[0] = int(levels_list[0],10)
    levels_list[1] = int(levels_list[1],10)
    levels_list[2] = int(levels_list[2],10)
    levels_list[3] = int(levels_list[3],10)
    levels_list[4] = int(levels_list[4],10)
    levels_list[5] = int(levels_list[5],10)
    levels_list[6] = int(levels_list[6],10)
    levels_list[7] = int(levels_list[7],10)
    levels_list[8] = int(levels_list[8],10)
    levels_list[9] = int(levels_list[9],10)
    print (levels_list) #show volume levels in terminal
    
    #set all servo angles
    volume = levels_list[0]
    kit.servo[0].angle = volume0[volume]
    volume = levels_list[1]
    kit.servo[1].angle = volume1[volume]
    volume = levels_list[2]
    kit.servo[2].angle = volume2[volume]
    volume = levels_list[3]
    kit.servo[3].angle = volume3[volume]
    volume = levels_list[4]
    kit.servo[4].angle = volume4[volume]
    volume = levels_list[5]
    kit.servo[5].angle = volume5[volume]
    volume = levels_list[6]
    kit.servo[6].angle = volume6[volume]
    volume = levels_list[7]
    kit.servo[7].angle = volume7[volume]
    volume = levels_list[8]
    kit.servo[8].angle = volume8[volume]
    volume = levels_list[9]
    kit.servo[9].angle = volume9[volume]
    
    pageload_count += 1
    thr = Thread(target=timer_function, args=[levels_list])
    thr.start()
    return ""
    
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
    
