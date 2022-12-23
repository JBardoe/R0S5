
#This is a method to find which employees are on the required day
def daySchedule():
    #This reads the file which containes the necessary information
    scheduled=[]
    file1=open("daySchedule.csv","r")
    for line in file1:
        data=line.strip().split(",")
        employee=data[0]
        role=data[1]
        logins.append([employee,role])
    file1.close()
    #This returns the table of employees and roles
    return scheduled


