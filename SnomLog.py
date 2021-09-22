from flask import *
import os
from datetime import *
import sys
import sched
import time as t
import threading

from datetime import date
app = Flask(__name__)
SnomStatus = {}

#Make sure we are only reporting between hours, Snoms will not receive calls at night obviously
def BetweenHours(currentTime):
    start = time(8,0,0)
    end = time(15,0,0)
    if (start <= currentTime.time() and currentTime.time() <= end):
        return True
    else:
        return False

    


def CheckUp():
    #This thread will check every hour to see if a Snom has been inactive (Should atleast get a bell every hour)
    currentTime = datetime.now() 
    print("Local time:" , currentTime)
    print("Checking snom status.....")  
    
    for key in SnomStatus:      
        delta = currentTime - SnomStatus[key]
        delta.total_seconds()
        print(delta.total_seconds())
        if(delta.total_seconds() > 7200 and BetweenHours(currentTime)):
            f = open("LogEvents.txt", "a")
            f.write("[X]SNOM DOWN " + key + " Did not report in two hours!\n")
            print("[X]SNOM DOWN " + key + " Did not report in two hours!")
            f.close()
        else:
            print("Status: OK 200")
            
    t.sleep(3600)
    CheckUp()

    return True

def LogHandler(ActiveCalls,CallID,Reason):
        #If we have more than one active call this could indicate an issue or busy line

        if(Reason == "MissedCall"):
            print("[X] Snom " + request.remote_addr + "Missed a call!")
            f = open("LogEvents.txt","a")
            f.write("[X] Snom " + request.remote_addr + "Missed a call!")
            f.close()

        print("Active Calls: ",ActiveCalls)
        if(int(ActiveCalls) > 1):
            print("[X]Detected more than 1 active call collission?")
            f = open("LogEvents.txt","a")
            f.write("[X]Possible Collission on call " + request.remote_addr)
            f.close()
            
        #Resolve IP to host and timestamp calls
        print("Call ID:", CallID)
        f = open("LogEvents.txt", "a")
        schoolname = ""
        print("Writing to Log")
        ctime = datetime.now()
        current_timestr = t.strftime("%H:%M:%S")
        if(request.remote_addr == "10.48.30.5"):
            schoolname = "FHS Relay Snom"
        elif(request.remote_addr == "10.80.30.5"):
            schoolname = "PJHS Relay Snom"
        elif(request.remote_addr == "10.8.30.5"):
            schoolname = "BHS Relay Snom"
        elif(request.remote_addr == "10.16.30.5"):
            schoolname = "CJHS Relay Snom"
        elif(request.remote_addr == "10.32.30.5"):
            schoolname = "DHS Relay Snom"
        elif(request.remote_addr == "10.40.30.5"):
            schoolname = "EJHS Relay Snom"
        elif(request.remote_addr == "10.56.30.241"):
            schoolname = "LSJHS Relay Snom"
        elif(request.remote_addr == "10.88.30.5"):
            schoolname = "SJHS Relay Snom"
        elif(request.remote_addr == "10.96.30.5"):
            schoolname = "UHJHS Relay Snom"
        else:
            schoolname = request.remote_addr

        f.write(current_timestr + ": " + "Snom Activity: " + Reason + " " + schoolname+ ": " + request.remote_addr + "\n")
        f.close()

        #Add the school and time of call to our dictionary to reference time between each call
        SnomStatus[schoolname] = ctime
        
     
        print("Current Key Directory")
        for pair in SnomStatus.items():
            print(pair)
        return "Success"
       

@app.route('/LogInvite',methods=['GET','POST'])
def LogSnom():
    print('Snom called')
    #Process Get Request with Parameters for Active Number of Calls and CallerID
    Status = LogHandler(request.args.get('active', type=str),request.args.get('callid', type=str),request.args.get('reason', type=str))
    #Do not add actual render page, the Snom tries to treat it like a settings file and dies. Super cool feature with no 
    return Response(status=200)
    
@app.route('/',methods=['POST','GET'])
def index():
    return Response(status=200)

if __name__ == "__main__":
    statuscheck = threading.Thread(target=CheckUp)
    statuscheck.start()
    app.run(host='172.27.66.107', port=62420, debug=True)
    
