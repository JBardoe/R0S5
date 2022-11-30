username="16bardoejac"
password="password"

def authenticate(username,password):
    #This opens the logins file and gets all of the approved logins
    logins=[]
    file1=open("logins.csv","r")
    for line in file1:
        data=line.strip().split(",")
        logins.append([data[0],data[1]])
    file1.close()

    #This checks if the given login was present in the file
    flag=False
    for i in range(len(logins)):
        if(username==logins[i][0] and password==logins[i][1]):
            flag=True
    
    #This returns whether it was present
    return flag

authenticate(username,password)


