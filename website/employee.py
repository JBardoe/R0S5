from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import employ
from .database import readEmployees

def getEmployees():
    #readEmployees()
    employees=[]
    file1=open("website/information/employees.csv","r")
    for line in file1:
        data=line.strip().split(",")
        employees.append([data[0],data[1]])
    file1.close()
    return employees

def appendEmployee(name, role):
    file1=open("website/information/employees.csv","a")
    file1.write(name+","+role+"\n")
    file1.close()
    for i in range(1,len(name)+1):
            if name[i-1:i] == " ":
                name[i-1:i] = "_"
                break
    file2=open(name+".txt","w")
    file2.write("name,"+name+"\nage,0\nDOB,DD/MM/YYYY\nmaxHours,40\nempNum,0000000\nremainingHoliday,0\nrate,0\nendOfTraining\nendOfAvailability")
    file2.close()


employee = Blueprint('employee', __name__)

@employee.route('/employeelist', methods=['GET', 'POST'])
def employeeList():
    employees=getEmployees()
    if request.method == "POST" and (request.form.get('emp')!=None):
        emp=request.form.get('emp')
        return redirect(url_for('employee.employeeFile', emp = emp))
    elif request.method == "POST":
        return redirect(url_for('employee.addEmployee'))

    return render_template("elist.html", employees=employees)

@employee.route('/addemployee', methods=['GET', 'POST'])
def addEmployee():
    employees=getEmployees()
    if request.method == "POST":
        name=request.form.get('empName')
        role=request.form.get('empRole')
        employees.append([name,role])
        appendEmployee(name, role)
        return redirect(url_for('employee.employeeList'))
    return render_template("elistInput.html", employees=employees)


@employee.route('/employeefile/<emp>', methods=['GET', 'POST'])
def employeeFile(emp):
    if request.method == "POST":
        return redirect(url_for('employee.editEmployee', emp=emp))
    newEmployee=employ(emp)
    return render_template("efile.html",employee=newEmployee)

@employee.route('/editemployee/<emp>', methods=['GET', 'POST'])
def editEmployee(emp):
    employee = employ(emp)
    if request.method=="POST":
        if request.form.get('age'):
            employee.age=request.form.get('age')
        if request.form.get('dob'):
            employee.dob="this is in fact the issue"
        if request.form.get('hrs'):
            employee.maxHours=request.form.get('hrs')
        if request.form.get('num'):
            employee.empNum=request.form.get('num')
        if request.form.get('hol'):
            employee.remainingHoliday=request.form.get('hol')
        if request.form.get('rat'):
            employee.rate=request.form.get('rat')
        if request.form.get('trainRole') and request.form.get('trainQual'):
            employee.training.append([request.form.get('trainRole'),request.form.get('trainQual')])
        if request.form.get('holiStart') and request.form.get('holiEnd') and request.form.get('holiApp'):
            employee.holiday.append([request.form.get('holiStart'),request.form.get('holiEnd'),request.form.get('holiApp')])
        employee.change()
        return redirect(url_for('employee.employeeFile',emp=emp))
    return render_template("editEfile.html", employee=employee)