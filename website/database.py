from pymongo import MongoClient
import pymongo

def readEmployees():
    myclient=pymongo.MongoClient("mongodb+srv://jackbardoe:of1vlO7rOLG7bfEs@r0s5.hxkyr5l.mongodb.net/?retryWrites=true&w=majority")
    db1 = myclient["Employee"]
    coll1 =db1["List"]
    emps=coll1.find()
    temp=[]
    file1=open("website/information/employees.csv", "w")
    for i in range(len(emps)):
        file1.write(emps[i][1]+","+emps[i][2]+"\n")
        temp.append(emps[i][1])
    file1.close()
    for j in range(len(temp)):
        name=temp[j]
        for k in range(1,len(name)):
            if name[k-1:i] == " ":
                name[k-1:i] = "_"
                break
        coll2= db1[name]
        infos=coll2.find()
        file2=open("website/information/"+name+".txt", "w")
        file2.write("name,"+infos[0][0]+"\nage,"+infos[0][1]+"\nDOB,"+infos[0][2]+"\nmaxHours,"+infos[0][3]+"\nempNum,"+infos[0][4]+"\nremainingHoliday,"+infos[0][5]+"\nrate,"+infos[0][6]+"\n")
        for t in range(len(infos[1])):
            if t%2==1:
                continue
            file2.write(infos[1][t]+","+infos[1][t+1]+"\n")
        file2.write("endOfTraining\n")
        for h in range(len(infos[2])):
            if t%3!=2:
                continue
            file2.write(infos[2][h]+","+infos[2][h+1]+","+infos[2][h+2]+"\n")
        file2.write("endOfAvailability\n")
        for n in range(len(infos[3])):
            if t%3!=2:
                continue
            file2.write(infos[3][n]+","+infos[3][n+1]+","+infos[3][n+2]+"\n")
        file2.close()
    myclient.close()

def readUsers():
    myclient=pymongo.MongoClient("mongodb+srv://jackbardoe:of1vlO7rOLG7bfEs@r0s5.hxkyr5l.mongodb.net/?retryWrites=true&w=majority")
    db = myclient["Users"]
    coll =db["Details"]
    users=coll.find()
    file1=open("website/information/logins.csv", "w")
    for i in range(len(users)):
        file1.write(users[i][1]+","+users[i][2]+"\n")
    file1.close()
    myclient.close()

def readRotas():
    myclient=pymongo.MongoClient("mongodb+srv://jackbardoe:of1vlO7rOLG7bfEs@r0s5.hxkyr5l.mongodb.net/?retryWrites=true&w=majority")
    db = myclient["Rotas"]
    collections=db.list_collection_names()
    for i in range(len(collections)):
        coll=db[collections[i]]
        roles=coll.find()
        name=collections[i]
        newname=""
        for j in range(len(name)):
            if name[i:i+1]=="/":
                newname=newname+"-"
            else:
                newname=newname+name[i:i+1]
        file1=open("website/information/rotas/"+newname+".txt", "w")
        for line in roles:
            file1.write(line[0]+","+line[1]+","+line2)
        file1.close()
    myclient.close()


def addUser(user):
    myclient=pymongo.MongoClient("mongodb+srv://jackbardoe:of1vlO7rOLG7bfEs@r0s5.hxkyr5l.mongodb.net/?retryWrites=true&w=majority")
    db = myclient["Users"]
    coll =db["Details"]
    post={"email":user.name,"password":user.pword,"fname":user.fname,"lname":user.lname,"cname":user.cname}
    coll.insert_one(post)
    myclient.close()

def changeEmp(emp):
    myclient=pymongo.MongoClient("mongodb+srv://jackbardoe:of1vlO7rOLG7bfEs@r0s5.hxkyr5l.mongodb.net/?retryWrites=true&w=majority")
    db = myclient["Employee"]
    coll= db[emp.name]
    coll.drop()
    coll1=db[name]
    post1={"name":emp.name,"age":emp.age,"hours":emp.maxHours,"number":emp.empNum,"holiday":emp.remainingHoliday,"rate":emp.rate}
    post2={}
    for i in range(len(user.training)):
        #post2.append(user.training[i][0]:user.training[i][1])
        pass
    post3={}
    for j in range(len(user.availability)):
        #post3.append("day"+str(j):user.availability[j][0],"start"+str(j):user.availability[j][1],"end"+str(j):user.availability[j][2])
        pass
    post4={}
    for f in range(len(user.holiday)):
        #post4.append("start"+str(f):user.holiday[f][0],"end"+str(f):user.holiday[f][1],"approval"+str(f):user.holiday[f][2])
        pass
    posts=[post1,post2,post3,post4]
    coll1.insert_many(posts)

def changeRota(day):
    myclient=pymongo.MongoClient("mongodb+srv://jackbardoe:of1vlO7rOLG7bfEs@r0s5.hxkyr5l.mongodb.net/?retryWrites=true&w=majority")
    db = myclient["Rotas"]
    newDay=str(day[0])+"/"+str(day[1])+"/"+str(day[2])
    coll= db[newDay]
    coll.drop()
    coll1=db[newDay]
    file1=open("website/information/rotas/"+str(day[0])+"-"+str(day[1])+"-"+str(day[2])+".txt","r")
    for line in file1:
        data=line.strip().split(",")
        post={"role":data[0],"name":data[1],"hours":data[2]}
        coll1.insert_one(post)
    file1.close()
    myclient.close()