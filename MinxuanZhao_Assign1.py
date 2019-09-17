'''
Created on Sep. 3rd, by Minxuan Zhao

Homework assignment 1
This program takes in the school start time and the students' assigned stop number,
and return the stop timing, how long it takes to school, and the busfare.
'''

# create constant variables
wholetrip = 45 #the length for the whole trip is 45 minutes
drivetime = 3 #the drive time between any two stops in minutes
stoptime = 2 #the minute length of each stop
basecost = 100 #the base cost of the bus ticket in cents
addtime = 4 #the 4 minute increments by which the cost of trip is charged
addcost = 15 #the cost for each 4-minutes of driving from the stop to the school in cents

#ask user to input school start hour and minute, and the stop number
schoolhourStr = input('Please enter the hour when school starts: ')
schoolhour = int(schoolhourStr)

schoolminStr = input('Please enter the minute when school starts: ')
schoolmin = int(schoolminStr)

stopnStr = input('Please enter your stop number (from 1 to 9): ')
stopn = int(stopnStr)

#transfer the school start time to minutes away from 00:00
schooltime = schoolhour * 60 + schoolmin 

#the trip start time in minutes away from 00:00
tripstart = schooltime - wholetrip 

#compute the stop arrival and departure time in minutes
stopavl = tripstart + (stopn - 1) * (drivetime + stoptime)
stopdep = stopavl + stoptime

stopavlh = stopavl // 60 #stop arrival hour
stopavlm = stopavl % 60 #stop arrival minutes

stopdeph = stopdep // 60 #stop departure hour
stopdepm = stopdep % 60 #stop departure minutes

#compute the length of the trip
tripminute = schooltime - stopdep

#compute the cost of the ticket
ticketcents = (tripminute // addtime) * addcost + basecost
ticketcost = ticketcents / 100

#print the output
print('The bus will be at stop number ', stopn, ' between', stopavlh, ':', str(stopavlm).zfill(2),
      ' and ',stopdeph,':', str(stopdepm).zfill(2))
print('The length of the trip from stop number ',stopn,' is ', tripminute,' minutes.')
print('The cost of the ticket from stop number ',stopn,' is $',ticketcost)