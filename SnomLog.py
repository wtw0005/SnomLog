from flask import *
import os
from datetime import datetime
import sys
import sched, time
import threading
from keyword import iskeyword
app = Flask(__name__)
SnomStatus = {}
f = open("LogEvents.txt", "a")


def CheckUp():
    print("Checker Thread Started")
    keylist = list(SnomStatus)
    timeO = datetime.now()
    
    for i in keylist:
        difference = timeO - timeO.strptime(SnomStatus[host],"%H:%M:%S")     
        if (difference.hours > 2):
            f.write("[X]SNOM DOWN "+ keylist(i) + "Did not report in two hours!")
            
    time.sleep(3000)
    CheckUp()


        

    return true

def LogHandler():
        #Get a request that says I got a call, log IP and request with time.
        #If no requests flag as down send me an email
        print("Writing to Log")
        time = datetime.now()
        current_time = time.strftime("%H:%M:%S")
        f.write(current_time + ": " + "New call from " + request.remote_addr +"\n")
        SnomStatus[request.remote_addr] = current_time
     
        print("Current Key Directory")
        for pair in SnomStatus.items():
            print(pair)
        return "Success"
       

@app.route('/LogInvite',methods=['GET','POST'])
def LogSnom():
    print('Snom called')
    Status = LogHandler() 
    return render_template("index.html")
    
@app.route('/',methods=['POST','GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    statuscheck = threading.Thread(target=CheckUp)
    statuscheck.start()
    app.run(host='172.27.66.107', port=62420, debug=True)
    
