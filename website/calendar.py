from flask import Blueprint, render_template, request, flash, redirect, url_for
import datetime
from .models import employ
from .employee import getEmployees as getElist
from .database import readRotas, changeRota

def monthDays():
    days=[
        [1,31],
        [2,28],
        [3,31],
        [4,30],
        [5,31],
        [6,30],
        [7,31],
        [8,31],
        [9,30],
        [10,31],
        [11,30],
        [12,31]
        ]
    return days

def increaseRange(weekRange):
    startDay=weekRange[0][0]
    startMonth=weekRange[0][1]
    startYear=weekRange[0][2]
    endDay=weekRange[1][0]
    endMonth=weekRange[1][1]
    endYear=weekRange[1][2]
    days=monthDays()
    if startYear%4==0:
        days[1][1]=29
    if days[endMonth-1][1]==endDay:
        startDay=1
        startMonth+=1
    else:
        startDay=endDay+1
        startMonth=endMonth
    endDay+=69
    while endDay>days[endMonth-1][1]:
        endDay-=days[endMonth-1][1]
        endMonth+=1
    weekRange=[[startDay,startMonth,startYear],[endDay,endMonth,endYear]]
    return weekRange

def decreaseRange(weekRange):
    days=monthDays()
    startDay=weekRange[0][0]
    startMonth=weekRange[0][1]
    startYear=weekRange[0][2]
    endDay=weekRange[1][0]
    endMonth=weekRange[1][1]
    endYear=weekRange[1][2]
    if startDay==1:
        endMonth-=1
        endDay=days[startMonth-1][1]
    else:
        endMonth=startMonth
        endDay=startDay-1
    startDay-=69
    while startDay<1:
        startMonth-=1
        startDay+=days[startMonth-1][1]
    weekRange=[[startDay,startMonth,startYear],[endDay,endMonth,endYear]]
    return weekRange

def getWeeks(today):
    startYear=22
    startMonth=1
    startDay=3
    endYear=22
    endMonth=3
    endDay=13
    yearFlag=False
    while not yearFlag:
        if today[2]>endYear:
            startYear+=1
            endYear+=1
            startDay-=1
            endDay-=1
            if (endYear-1)%4==0:
                startDay-=1
                endDay-=1
            if startDay<1:
                startDay+=7
            if endDay<1:
                endDay+=16
        else:
            yearFlag=True
    flag=False
    weekRange=[[startDay,startMonth,startYear],[endDay,endMonth,endYear]]
    while not flag:
        if today[1]<=weekRange[1][1] and today[1]>=weekRange[0][1]:
            if today[1]!=weekRange[0][1] and today[1]!=weekRange[1][1] or today[1]==weekRange[0][1] and today[0]>=weekRange[0][0] or today[1]==weekRange[1][1] and today[0]<=weekRange[1][0]:
                return weekRange
            elif today[1]==weekRange[0][1] and today[0]<=weekRange[0][0]:
                weekRange=decreaseRange(weekRange)
                return weekRange
            else:
                weekRange=increaseRange(weekRange)
                return weekRange
        else:
            weekRange=increaseRange(weekRange)

def getCalendar(today):
    weekRange=getWeeks(today)
    days=monthDays()
    weeks=[weekRange[0]]
    currentDay=weekRange[0][0]
    currentMonth=weekRange[0][1]
    currentYear=weekRange[0][2]
    for i in range(9):
        if currentDay+7>days[currentMonth-1][1]:
            currentDay+=7
            currentDay-=days[currentMonth-1][1]
            currentMonth+=1
        else:
            currentDay+=7
        weeks.append([currentDay,currentMonth,currentYear])
    return weeks

def getDays(weeks):
    everyDay=[]
    days=monthDays()
    currentDay=weeks[0][0]
    currentMonth=weeks[0][1]
    currentYear=weeks[0][2]
    everyDay.append([currentDay,currentMonth,currentYear])
    for i in range(70):
        if (currentDay+1)>days[currentMonth-1][1]:
            currentDay=1
            currentMonth+=1
        else:
            currentDay+=1
        everyDay.append([currentDay,currentMonth,currentYear])
    return everyDay

def getExisting(weeks):
    everyDay=getDays(weeks)
    existings=[]
    for i in range(len(everyDay)):
        try:
            file1=open("website/information/rotas/"+str(everyDay[i][0])+"-"+str(everyDay[i][1])+"-"+str(everyDay[i][2])+".txt","r")
            file1.close()
        except FileNotFoundError:
            existings.append("Incomplete")
        else:
            existings.append("Completed")
    return existings

def fixWeeks(weeks):
    for l in range(len(weeks)):
        weeks[l][0]+=1
    return weeks

def lastWeek(day):
    days=monthDays()
    if (day[0]-7)<1:
        day[0]=(day[0]-7)+days[day[1]-2][1]
        day[1]-=1
    else:
        day[0]-=7
    return day

def nextWeek(day):
    days=monthDays()
    if day[0]+7>days[day[1]-1][1]:
        day[0]=(day[0]+7)-days[day[1]-1][1]
        day[1]+=1
    else:
        day[0]+=7
    return day

def toString(dateList):
    date=str(dateList[0])+"-"+str(dateList[1])+"-"+str(dateList[2])
    return date

def toArray(date):
    dateList=[]
    start=0
    end=0
    for i in range(len(date)-1):
        if date[i+1]=="-" or date[i+1]=="/":
            end=i+1
            dateList.append(int(date[start:end]))
            start=end+1
    dateList.append(int(date[start:len(date)]))
    return dateList

def getWeekdays(week):
    weekDays=[]
    days=monthDays()
    weekDays.append([week[0],week[1],week[2]])
    for i in range(6):
        if (week[0]+1)>(days[week[1]-1][1]):
            week[0]=1
            week[1]+=1
            weekDays.append([week[0],week[1],week[2]])
        else:
            week[0]+=1
            weekDays.append([week[0],week[1],week[2]])
    return weekDays

def yesterday(day):
    days=monthDays()
    if day[0]-1<1:
        day[0]=days[day[1]-2][1]
        day[1]-=1
    else:
        day[0]-=1
    return day

def tomorrow(day):
    days=monthDays()
    if day[0]+1>days[day[1]-1][1]:
        day[0]=1
        day[1]+=1
    else:
        day[0]+=1
    return day

def getFloorPlan(day):
    employees=[]
    try:
        file1=open("website/information/rotas/"+str(day[0])+"-"+str(day[1])+"-"+str(day[2])+".txt","r")
        file1.close()
    except FileNotFoundError:
        file1=open("website/information/rotas/"+str(day[0])+"-"+str(day[1])+"-"+str(day[2])+".txt","x")
        file1.close()
    else:
        file1=open("website/information/rotas/"+str(day[0])+"-"+str(day[1])+"-"+str(day[2])+".txt","r")
        for line in file1:
            data=line.strip().split(",")
            employees.append([data[0],data[1],data[2]])
        file1.close()
    return employees

def appendRole(day,role):
    file1=open("website/information/rotas/"+str(day[0])+"-"+str(day[1])+"-"+str(day[2])+".txt","a")
    file1.write(str(role[0])+","+str(role[1])+","+str(role[2])+"\n")
    file1.close()

def getEmployees(days):
    employees=[[],[],[],[],[],[],[]]
    for i in range (len(days)):
        try:
            file1=open("website/information/rotas/"+str(days[i][0])+"-"+str(days[i][1])+"-"+str(days[i][2])+".txt","r")
            file1.close()
        except FileNotFoundError:
            pass
        else:
            file1=open("website/information/rotas/"+str(days[i][0])+"-"+str(days[i][1])+"-"+str(days[i][2])+".txt","r")
            for line in file1:
                data=line.strip().split(",")
                employees[i].append(data[1])
    return employees

def getFloorPlanHours(day):
    employees=[]
    try:
        file1=open("website/information/rotas/"+str(day[0])+"-"+str(day[1])+"-"+str(day[2])+".txt","r")
        file1.close()
    except FileNotFoundError:
        pass
    else:
        file1=open("website/information/rotas/"+str(day[0])+"-"+str(day[1])+"-"+str(day[2])+".txt","r")
        for line in file1:
            data=line.strip().split(",")
            employees.append([data[0],data[1],data[2]])
        file1.close()
    return employees

def hoursWorked(table):
    total=0.0
    markers=[]
    for j in range(len(table[2])-1):
        if table[2][j:j+1]==":" or table[2][j:j+1]=="-":
            markers.append(j)
    startTime=datetime.time(int(table[2][0:markers[0]]),int(table[2][markers[0]+1:markers[1]]))
    endTime=datetime.time(int(table[2][markers[1]+1:markers[2]]),int(table[2][markers[2]+1:len(table[2])]))
    totalTime=datetime.datetime.combine(datetime.date.today(), endTime) - datetime.datetime.combine(datetime.date.today(), startTime)
    total+=totalTime.total_seconds()
    return total

def getHours(days):
    total=0.0
    for day in days:
        tables=getFloorPlanHours(day)
        if tables:
            for i in range(len(tables)):
                total+=hoursWorked(tables[i])
    hours=round((total/3600),2)
    return hours

def getCost(days):
    cost=0.0
    floorPlans=[]
    for day in days:
        tables=getFloorPlanHours(day)
        if tables:
            floorPlans.append(tables)
    for i in range(len(floorPlans)):
        for j in range(len(floorPlans[i])):
            employee=employ(floorPlans[i][j][1])
            hours=round((hoursWorked(floorPlans[i][j])/3600),2)
            cost+=round(employee.rate*hours,2)
    return cost

def findIssues(days):
    week=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    hoursIssue=hoursIssues(days)
    if hoursIssue:
        return hoursIssue
    else:
        for i in range(len(days)):
            holidayIssue=holidayIssues(days[i])
            if holidayIssue:
                return holidayIssue
            else:
                trainingIssue=trainingIssues(days[i])
                if trainingIssue:
                    return trainingIssue
                else:
                    availabilityIssue=availabilityIssues(days[i], week[i], i)
                    if availabilityIssue:
                        return availabilityIssue
                    else:
                        return None

def holidayIssues(day):
    issue=""
    table=getFloorPlanHours(day)
    date=datetime.date(int(day[0]),int(day[1]),int(day[2]))
    for line in table:
        employee=employ(line[1])
        for row in employee.holiday:
            start=datetime.datetime.strptime(row[0], '%d/%m/%y')
            end=datetime.datetime.strptime(row[1], '%d/%m/%y')
            if date>=start and date<=end:
                issue="Error: "+employee.name+" scheduled on "+str(day[0])+"/"+str(day[1])+"/"+str(day[2])+". On holiday."
                return issue
    return None


def trainingIssues(day):
    issue=""
    table=getFloorPlanHours(day)
    found=False
    for line in table:
        employee=employ(line[1])
        trained=False
        for row in employee.training:
            if line[0]==row[0]:
                trained=True
                break
        if not trained:
            found=True
            break
    if found:
        issue="Error: On "+str(day[0])+"/"+str(day[1])+"/"+str(day[2])+", "+employee.name+" lacks required training for job role."
        return issue
    else:
        return None 

def hoursIssues(days):
    issue=""
    employees=[]
    for day in days:
        table=getFloorPlanHours(day)
        for line in table:
            there=False
            for employee in employees:
                if employee[0].name==line[1]:
                    there=True
            if not there:
                employees.append([employ(line[1]),0])
    for day in days:
        table=getFloorPlanHours(day)
        for line in table:
            for i in range(len(employees)):
                if line[1]==employees[i][0].name:
                    employees[i][1]+=round((hoursWorked(line)/3600),2)
                    break
    for j in range(len(employees)):
        if employees[j][1]>float(employees[j][0].maxHours):
            issue="Error: "+employees[j][0].name+" scheduled over maximum hours."
            return issue
    return None

def getStartEnd(between):
    times=[]
    index=0
    for i in range(len(between)+1):
        if between[i:i+1]=="-":
            times.append(between[0:i])
            index=i
            break
    times.append(between[i+1:len(between)])
    start=datetime.datetime.strptime(times[0], '%H:%M')
    end=datetime.datetime.strptime(times[1], '%H:%M')
    finalTimes=[start,end]
    return finalTimes

def availabilityIssues(day, weekDay, index):
    issue=""
    table=getFloorPlanHours(day)
    for line in table:
        employee=employ(line[1])
        if employee.availability[index][1]=="N/A":
            issue="Error: "+employee.name+" scheduled on "+weekDay+". Outside availability."
            return issue
        else:
            scheduled=getStartEnd(line[2])
            startScheduled=scheduled[0]
            endScheduled=scheduled[1]
            startEmp=datetime.datetime.strptime(employee.availability[index][1], '%H:%M')
            endEmp=datetime.datetime.strptime(employee.availability[index][2], '%H:%M')
            if startScheduled<startEmp or endScheduled>endEmp:
                issue="Error: On "+str(day[0])+"/"+str(day[1])+"/"+str(day[2])+", "+employee.name+" scheduled outside availability."
                return issue
    return None

def getCurrentHours(emp, days):
    total=0
    for day in days:
        table=getFloorPlanHours(day)
        for line in table:
            if line[1]==emp.name:
                total+=round((hoursWorked(line)/3600),2)
                break
    return total

def checkNextHoliday(emp, days):
    date=datetime.datetime.strptime((str(days[0][0])+"/"+str(days[0][1])+"/"+str(days[0][2])), '%d/%m/%y')
    for holiday in emp.holiday:
        start=datetime.datetime.strptime(holiday[0], '%d/%m/%y')
        if start>date:
            return holiday[0]
    return "N/A"

def getOverlay(days):
    employees=getElist()
    emps=[]
    for employee in employees:
        emps.append(employ(employee[0]))
    overlay=[]
    for emp in emps:
        name=emp.name
        maxHours=emp.maxHours
        currentHours=getCurrentHours(emp, days)
        nextHoliday=checkNextHoliday(emp, days)
        overlay.append([name,maxHours,currentHours,nextHoliday])
    return overlay

calendar = Blueprint('calendar', __name__)

@calendar.route('/weekscalendar', methods=['GET', 'POST'])
def weeksCalendar():
    #readRotas()
    now=datetime.date.today()
    today=[int(now.day),int(now.month),int(str(now.year)[2:4])]
    weeks=getCalendar(today)
    weeks=fixWeeks(weeks)
    existing=getExisting(weeks)
    if request.method == "POST":
        if request.form.get('previous'):
            dateList=lastWeek(weeks[0])
            date=toString(dateList)
            return redirect(url_for("calender.weekCalendar", date=date))
        if request.form.get('next'):
            dateList=nextWeek(weeks[9])
            date=toString(dateList)
            return redirect(url_for("calendar.weekCalendar", date=date))
        if request.form.get('weekPlan'):
            weekPlan=request.form.get('weekPlan')
            weekList=toArray(weekPlan)
            week=toString(weekList)
            return redirect(url_for("calendar.weekPlanner", week=week))
    return render_template("calendar.html", weeks=weeks, existing=existing)

@calendar.route('/weekcalendar/<date>', methods=['GET', 'POST'])
def weekCalendar(date):
    dateList=toArray(date)
    weeks=getCalendar(dateList)
    weeks=fixWeeks(weeks)
    existing=getExisting(weeks)
    if request.method == "POST":
        if request.form.get('previous'):
            dateList=lastWeek(weeks[0])
            date=toString(dateList)
            return redirect(url_for("calendar.weekCalendar", date=date))
        if request.form.get('next'):
            dateList=nextWeek(weeks[9])
            date=toString(dateList)
            return redirect(url_for("calendar.weekCalendar", date=date))
        if request.form.get('weekPlan'):
            weekPlan=request.form.get('weekPlan')
            weekList=toArray(weekPlan)
            week=toString(weekList)
            return redirect(url_for("calendar.weekPlanner", week=week))
    return render_template("calendar.html", weeks=weeks, existing=existing)

@calendar.route('/weekplanner/<week>', methods=['GET', 'POST'])
def weekPlanner(week):
    weekList=toArray(week)
    days=getWeekdays(weekList)
    standard=["Mon","Tues","Wed","Thurs","Fri","Sat","Sun"]
    if request.method=="POST":
        #Floor Plan Redirect
        if request.form.get('dayPlan'):
            requested=request.form.get('dayPlan')
            for i in range(7):
                if requested==standard[i]:
                    dayList=days[i]
                    day=toString(dayList)
                    return redirect(url_for("calendar.floorPlan",day=day))
        #Weeks Scroll
        if request.form.get('previous'):
            wantedWeek=lastWeek(days[0])
            previousWeek=toString(wantedWeek)
            return redirect(url_for("calendar.weekPlanner", week=previousWeek))
        if request.form.get('next'):
            wantedWeek=tomorrow(days[6])
            followingWeek=toString(wantedWeek)
            return redirect(url_for("calendar.weekPlanner", week=followingWeek))
        #Employee Overlay
        if request.form.get('overlay'):
            return redirect(url_for("calendar.employeeOverlay", week=week))
    #Day Employees
    employees=getEmployees(days)
    #Hour and Cost Calc
    hours=getHours(days)
    cost=getCost(days)
    #Issue Finding
    issue=findIssues(days)
    return render_template("wplanner.html", days=days, employees=employees, hours=hours, cost=cost, issue=issue)

@calendar.route('/weekplanneremployees/<week>', methods=['GET', 'POST'])
def employeeOverlay(week):
    weekList=toArray(week)
    days=getWeekdays(weekList)
    standard=["Mon","Tues","Wed","Thurs","Fri","Sat","Sun"]
    if request.method=="POST":
        #Floor Plan Redirect
        if request.form.get('dayPlan'):
            requested=request.form.get('dayPlan')
            for i in range(7):
                if requested==standard[i]:
                    dayList=days[i]
                    day=toString(dayList)
                    return redirect(url_for("calendar.floorPlan",day=day))
        #Weeks Scroll
        if request.form.get('previous'):
            wantedWeek=lastWeek(days[0])
            previousWeek=toString(wantedWeek)
            return redirect(url_for("calendar.weekPlanner", week=previousWeek))
        if request.form.get('next'):
            wantedWeek=tomorrow(days[6])
            followingWeek=toString(wantedWeek)
            return redirect(url_for("calendar.weekPlanner", week=followingWeek))
    #Day Employees
    employees=getEmployees(days)
    #Hour and Cost Calc
    hours=getHours(days)
    cost=getCost(days)
    #Issue Finding
    issue=findIssues(days)
    #Overlay Employees
    overlay=getOverlay(days)
    return render_template("wplannerOverlay.html", days=days, employees=employees, hours=hours, cost=cost, issue=issue, overlay=overlay)

@calendar.route('/floorplan/<day>', methods=['GET', 'POST'])
def floorPlan(day):
    dayList=toArray(day)
    employees=getFloorPlan(dayList)
    if request.method == "POST":
        if request.form.get('previous'):
            lastList=yesterday(dayList)
            last=toString(lastList)
            return redirect(url_for("calendar.floorPlan", day=last))
        if request.form.get('next'):
            nextList=tomorrow(dayList)
            nextD=toString(nextList)
            return redirect(url_for("calendar.floorPlan", day=nextD))
        if request.form.get('add'):
            return redirect(url_for("calendar.addRole", day=day))
    return render_template("fplan.html", day=dayList, employees=employees)

@calendar.route('/addrole/<day>', methods=['GET', 'POST'])
def addRole(day):
    dayList=toArray(day)
    employees=getFloorPlan(dayList)
    if request.method == "POST":
        if request.form.get('previous'):
            lastList=yesterday(dayList)
            last=toString(lastList)
            return redirect(url_for("calendar.floorPlan", day=last))
        if request.form.get('next'):
            nextList=tomorrow(dayList)
            nextD=toString(nextList)
            return redirect(url_for("calendar.floorPlan", day=nextD))
        if request.form.get('role') and request.form.get('name') and request.form.get('hours'):
            role=[request.form.get('role'),request.form.get('name'),request.form.get('hours')]
            appendRole(dayList,role)
            #changeRota(dayList)
            return redirect(url_for("calendar.floorPlan", day=day))
    return render_template("fplanInput.html", day=dayList, employees=employees)