from flask import Blueprint, render_template, request, flash, redirect, url_for

def getEmployees():
    employees=[]
    file1=open("C:/Users/arron/OneDrive/Documents/GitHub/IA-Website/website/information/employees.csv","r")
    for line in file1:
        data=line.strip().split(",")
        employees.append([data[0],data[1]])
    file1.close()
    return employees

def appendEmployee(name, role):
    file1=open("C:/Users/arron/OneDrive/Documents/GitHub/IA-Website/website/information/employees.csv","a")
    file1.write(name+","+role+"\n")
    file1.close()
    for i in range(1,len(name)+1):
            if name[i-1:i] == " ":
                name[i-1:i] = "_"
                break
    file2=open(name+".txt","w")
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
    return render_template("efile.html", emp=emp)