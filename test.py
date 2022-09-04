import pymongo

client= pymongo.MongoClient("mongodb+srv://jackbardoe:William1@r0s5.hxkyr5l.mongodb.net/?retryWrites=true&w=majority")

database=client["Users"]
collection=database["Details"]
direct={"email": "kerrybardoe@btinternet.com", "password": "password1", "fname": "Kerry", "lname": "Bardoe", "cname": "NHS"} 
x = collection.insert_one(direct)