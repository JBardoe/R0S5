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