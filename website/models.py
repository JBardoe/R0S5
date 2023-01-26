from pymongo import MongoClient
import pymongo

def readLogins():
    client1= pymongo.MongoClient("mongodb+srv://jackbardoe:of1vlO7rOLG7bfEs@r0s5.hxkyr5l.mongodb.net/?retryWrites=true&w=majority")
    database1=client1["Users"]
    collection1=database1["Details"]

    client1.close()


class user:
    email=""
    pword=""
    fname=""
    lname=""
    cname=""

    def __init__(self, email, pword, fname, lname, cname):
        self.email=email
        self.pword=pword
        self.fname=fname
        self.lname=lname
        self.cname=cname

    def add(self):
        client1= pymongo.MongoClient("mongodb+srv://jackbardoe:of1vlO7rOLG7bfEs@r0s5.hxkyr5l.mongodb.net/?retryWrites=true&w=majority")
        database1=client1["Users"]
        collection1=database1["Details"]

        pass #add db functionality

class employ:
    name=""
    age=0
    dob=""
    maxHours=0
    empNum=""
    remainingHoliday=0
    rate=0
    training=[]
    availability=[]
    holiday=[]

    def info(self, name):
        tempName=name
        for i in range(1,len(tempName)+1):
            if tempName[i-1:i] == " ":
                tempName[i-1:i] = "_"
                break
        file1=open(tempName+".txt","r")
        j=0
        temp=[]
        for line in file1:
            if j==7:
                break
            data=line.strip().split(":")
            temp.append(data[1])
            j+=1
        self.name=temp[0]
        self.age=int(temp[1])
        self.dob=temp[2]
        self.maxHours=int(temp[3])
        self.empNum=temp[4]
        self.remainingHoliday=int(temp[5])
        self.rate=float(temp[6])
        t=0
        for line in file1:
            if t<7:
                t+=1
                continue
            data=line.strip.split(",")
            if data[0] =="endOfTraining":
                break
            self.training.append([data[0],data[1]])
        p=0
        for line in file1:
            if p<t:
                p+=1
                continue
            data=line.strip().split(",")
            if data[0] == "endOfAvailability":
                break
            self.availability.append([data[0],data[1],data[2]])
        l=0
        for line in file1:
            if l<p:
                l+=1
                continue
            data=line.strip.split(",")
            self.holiday.append([data[0],data[1],data[2]])
        file1.close()

    def __init__(self, name):
        self.name=name
        self.info(name)
    
    