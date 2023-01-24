import pymongo

def openFile():
    #client1= MongoClient("mongodb+srv://jackbardoe:William1@r0s5.hxkyr5l.mongodb.net/?retryWrites=true&w=majority")
    #database1=client1["Users"]
    #collection1=database1["Details"]

    #+Read into logins file

    #client1.close()

    logins=[]
    file1=open("logins.csv","r")
    for line in file1:
        data=line.strip().split(",")
        logins.append([data[0],data[1]])
    file1.close()
    return logins




myclient=pymongo.MongoClient("mongodb+srv://jackbardoe:of1vlO7rOLG7bfEs@r0s5.hxkyr5l.mongodb.net/?retryWrites=true&w=majority")
print(myclient.list_database_names())

db = myclient["Users"]


