from flask import Blueprint, render_template, request, flash, redirect, url_for

def getEmployees():
    employees=[]
    file1=open("C:/Users/arron/OneDrive/Documents/GitHub/IA-Website/website/information/employees.csv","r")
    for line in file1:
        data=line.strip().split(",")
        employees.append([data[0],data[1]])
    file1.close()
    return employees

def addEmployee(name, role):
    file1=open("C:/Users/arron/OneDrive/Documents/GitHub/IA-Website/website/information/employees.csv","a")
    file1.write(name+","+role+"\n")
    file1.close()

employee = Blueprint('employee', __name__)

@employee.route('/employeelist', methods=['GET', 'POST'])
def employeeList():
    employees=getEmployees()
    if request.method == "POST":
        return render_template("elistInput.html", employees=employees)
    return render_template("elist.html", employees=employees)

@employee.route('/addemployee', methods=['GET', 'POST'])
def addEmployee():
    employees=getEmployees()
    if request.method == "POST":
        name=request.form.get('empName')
        role=request.form.get('empRole')
        employees.append([name,role])
        addEmployee(name,role)
        return render_template("elist.html", employees=employees)
    return render_template("elistInput.html", employees=employees)

@employee.route('/employeefile', methods=['GET', 'POST'])
def employeeFile():
    return render_template("efile.html")