from pymongo import MongoClient
import pymongo
from .database import addUser, changeEmp

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
        #addUser(self)
        pass

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
        self.training=[]
        self.availability=[]
        self.holiday=[]
        tempName=""
        for i in range(0,len(name)):
            if name[i] == " ":
                tempName = tempName + "_"
            else:
                tempName = tempName + name[i]
        file1=open("website/information/"+tempName+".txt","r")
        j=0
        temp=[]
        for line in file1:
            if j==7:
                break
            data=line.strip().split(",")
            temp.append(data[1])
            j+=1
        self.name=temp[0]
        self.age=int(temp[1])
        self.dob=temp[2]
        self.maxHours=temp[3]
        self.empNum=temp[4]
        self.remainingHoliday=float(temp[5])
        self.rate=float(temp[6])

        for line in file1:
            data=line.strip().split(",")
            if data[0] =="endOfTraining":
               break
            self.training.append([data[0],data[1]])
    
        for line in file1:
            data=line.strip().split(",")
            if data[0] == "endOfAvailability":
                break
            self.availability.append([data[0],data[1],data[2]])

        for line in file1:
            data=line.strip().split(",")
            self.holiday.append([data[0],data[1],data[2]])
        file1.close()

    def __init__(self, name):
        self.name=name
        self.info(name)

    def change(self):
        tempName=""
        for i in range(0,len(self.name)):
            if self.name[i] == " ":
                tempName = tempName + "_"
            else:
                tempName = tempName + self.name[i]
        file1=open("website/information/"+tempName+".txt","w")
        file1.write("")
        file1.close()
        file1=open("website/information/"+tempName+".txt","a")
        file1.write("name,"+self.name+"\nage,"+str(self.age)+"\nDOB,"+self.dob+"\nmaxHours,"+self.maxHours+"\nempNum,"+self.empNum+"\nremainingHoliday,"+str(self.remainingHoliday)+"\nrate,"+str(self.rate)+"\n")
        for j in range(len(self.training)):
            file1.write(self.training[j][0]+","+self.training[j][1]+"\n")
        file1.write("endOfTraining\n")
        for t in range(len(self.availability)):
            file1.write(self.availability[t][0]+","+self.availability[t][1]+","+self.availability[t][2]+"\n")
        file1.write("endOfAvailability\n")
        for k in range(len(self.holiday)-1):
            file1.write(self.holiday[k][0]+","+self.holiday[k][1]+","+self.holiday[k][2]+"\n")
        file1.close()
        #changeEmp(self)