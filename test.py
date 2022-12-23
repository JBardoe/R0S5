#This imports the library to this python project
import pymongo

#This establishes the connection to the datanase
client1= pymongo.MongoClient("mongodb+srv://jackbardoe:William1@r0s5.hxkyr5l.mongodb.net/?retryWrites=true&w=majority")

#This cycles through sections of the database
database1=client1["Users"]
collection1=database1["Details"]

#This is an example of adding a document to the database
direct1={"email": "kerrywoods@btinternet.com", "password": "password1", "fname": "Kerry", "lname": "Woods", "cname": "NHS"} 
collection1.insert_one(direct1)

