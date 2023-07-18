#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from datetime import datetime

"""
convert input files into proper name format

Parameters
----------
fileName: str
    the filename entered from the command line interface

Returns
-------
str

"""
def convertFile(fileName):
    name = ''
    start = 0
    for i in range(len(fileName)):
        if fileName[i]=='=':
            start = i+1
            break

    for i in range(start, len(fileName)):
        name += fileName[i]

    return name

"""
convert input dates into proper integer format

Parameters
----------
date: str
    the date entered from the command line interface

Returns
-------
int

"""
def convertDate(date):
    res = 0
    b1 = 1
    i = len(date)-1
    for j in range(3):
        base = 1
        temp = 0
        while i >= 0 and date[i]>='0' and date[i]<='9':
            digit = int(date[i])
            temp += base*digit
            base *= 10
            i -= 1
        i -= 1
        if temp < 10:
            base *= 10
        res += temp*b1
        b1 *= 100

    return res
        
"""
find the location of the target str

Parameters
----------
line: str
    each line of str info in the xml file
target: str
    target str to be searched

Returns
-------
int

"""
def findPos(line, target):
    for i in range(len(line)):
        if line[i]==target:
            return i

    return 0

"""
generate information for each event in the xml file

Parameters
----------
line: str
    each line of str info in the xml file
ind: int
    starting indice for the line traversal

Returns
-------
str
"""
def generateInfo(line, ind):
    res = ''
    i = ind
    while i < len(line) and line[i]!='<':
        res += line[i]
        i += 1
    
    return res

"""
read informations in the xml files given an external filename

Parameters
----------
file1: str
    the filename to be read
linePerEvent: int
    number of lines per each event

Returns
-------
list of Dictionary

"""
def readFile(file1, linePerEvent): 
    f = open(file1, "r")
    count = 1
    events = []
    event = {}

    for line in f:
        if count % linePerEvent >= 3 or count % linePerEvent == 0:
            left = findPos(line, '<')+1
            right = findPos(line, '>')
            event[line[left:right]] = generateInfo(line, right+1)
            
        if count % linePerEvent == 0:
            events.append(event)
            event = {}

        count += 1
    
    f.close()
    return events

"""
format time from str to int-form

Parameters
----------
time: str
    the time inputted in str-form

Returns
-------
int

"""
def timeFormat(time):
    return int(time[0:2])*100+int(time[-2:])

"""
add each valid event into output list

Parameters
----------
events: list of Dictionary
    a list of events from the external xml file
circuits: list of Dictionary
    a list of circuits from the xml file
broadcaste: list of Dictionary
    a list of broadcaster from the xml file
curEvents: Dictionary
    current valid event within the events list from the xml file
time: int
    start time of the event
time2: int
    end time of the event
output: list
    list that store expected output events

Returns
-------
void

"""
def addEvent(events, circuits, broadcaste, curEvents, time, time2, output):
    timezone = ''
    output.append('    - id: '+curEvents['id'])
    output.append('      description: '+curEvents['description'])

    curBroadcaster = curEvents['broadcaster']

    for item in circuits:
        if curEvents['location'] == item['id']:
            output.append('      circuit: '+item['name']+' ('+item['direction']+')')
            output.append('      location: '+item['location'])
            timezone = item['timezone']
            break

    date1 = datetime(int(curEvents['year']), int(curEvents['month']), int(curEvents['day']), time//100, time%100)
    date2 = datetime(int(curEvents['year']), int(curEvents['month']), int(curEvents['day']), time2//100, time2%100)
    
    when = date1.strftime("%I:%M %p")+' - '+date2.strftime("%I:%M %p ")+date1.strftime('%A, ')
    when += date1.strftime("%B %d, %Y ")+'('+timezone+')'
    output.append('      when: '+when)
    output.append('      broadcasters: ')

    temp = ''
    for item in broadcaste:
        if item['id'] in curEvents['broadcaster']:
            output.append('        - '+item['name'])

"""
check for valid time

Parameters
----------
events: list of Dictionary
    list of events from the xml file
time: int
    current time of the event
curDate: int
    current date in year-month-day format

Returns
-------
Boolean

"""
def containsTime(events, time, curDate):
    for event in events:
        date = int(event['year']+event['month']+event['day'])
        if timeFormat(event['start']) == time and date == curDate:
            return True
    
    return False

"""
find proper event

Parameters
----------
events: list of Dictionary
    list of events from the xml file
time: int
    start time of the event
curDate: int
    current date in year-month-day format

Returns
-------
list

"""
def findPropereEvent(events, time, curDate):
    for event in events:
        date = int(event['year']+event['month']+event['day'])
        if timeFormat(event['start']) == time and date == curDate:
            return event
    
    return {}


"""
search for valid event from for each day from 12am - 11:59 pm

Parameters
----------
events: list of Dictionary
    a list of events from the external xml file
circuits: list of Dictionary
    a list of circuits from the xml file
broadcaste: list of Dictionary
    a list of broadcaster from the xml file
curEvents: Dictionary
    current valid event within the events list from the xml file
curDate: int
    currentDate year-month-day form
output: list
    list that store expected output events

Returns
-------
void

"""
def searchEvent(events, circuits, broadcaste, curEvents, curDate, output):
    time = 0
    while(time < 2359):

        if(containsTime(events, time, curDate)):
            curEvents = findPropereEvent(events, time, curDate)
            target = timeFormat(curEvents['start'])
            target2 = timeFormat(curEvents['end'])
            addEvent(events, circuits, broadcaste, curEvents, target, target2, output)
           
        if time % 100 == 59:
            time += 40

        time += 1
    
"""
search for valid dates within all the events from the main xml file

Parameters
----------
events: list of Dictionary
    a list of events from the external xml file
circuit: list of Dictionary
    a list of circuits from the xml file
broadcaster: list of Dictionary
    a list of broadcaster from the xml file
curDate: int
    current date in year-month-day format
output: list
    a list of valid events

Returns
-------
void

"""
def searchDate(events, circuits, broadcaster, curDate, output):
    for i in events:
        date = i['year']+i['month']+i['day']
    
        if curDate == int(date):
            date = datetime(curDate//10000, (curDate//100)%100, curDate%100)
            output.append('  - '+date.strftime('%d-%m-%Y:'))
            searchEvent(events, circuits, broadcaster, i, curDate, output)
            break

"""
write expected output to the output.yaml

Parameters
----------
output: list
    The list of expected output elements

Returns
-------
void

"""
def writeToFile(output):
    f2 = open('output.yaml', 'w')
    cnt = 1

    for i in output:
        f2.writelines(i)
        if cnt < len(output):
            f2.writelines('\n')
        
        cnt += 1

    f2.close()
        
"""
process input files from the given date range

Parameters
----------
start: str
    The start date of the search
end: str
    The end date of the search
file1: str
file2: str
file3: str
    The filenames inputted from the terminal

Returns
-------
void

"""
def processData(start, end, file1, file2, file3):
    events = readFile(file1, 11)
    circuits = readFile(file2, 7)
    broadcaster = readFile(file3, 5)
    output = ['events:']
    
    curDate = start

    while(curDate <= end):
        searchDate(events, circuits, broadcaster, curDate, output)

        if curDate % 100 == 31:
            curDate += 69

        curDate += 1
        
    writeToFile(output)

"""
input external commands from the terminal such as filename and input dates

Parameters
----------
start: str
    The start date of the search
end: str
    The end date of the search
file1: str
file2: str
file3: str
    The filenames inputted from the terminal

Returns
-------
void

"""
def inputFile(start, end, file1, file2, file3):
    start = convertDate(start)
    end = convertDate(end)
    file1 = convertFile(file1)
    file2 = convertFile(file2)
    file3 = convertFile(file3)
    processData(start, end, file1, file2, file3)

def main():
    """The main entry point for the program.
    """
    # input start dates and end dates
    inputFile(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    


if __name__ == '__main__':
    main()
