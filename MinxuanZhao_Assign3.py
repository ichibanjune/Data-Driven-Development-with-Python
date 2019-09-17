'''
Created on Sep 27, 2018. By Minxuan Zhao

CS799 Homework 3

This program is designed to processing monthly sales data in coffee shop and
create summary analysis of the data.
It allows user to select for the fisrt x days in a month and display a matrix chart
that shows sales for each day in each hour.
Then it ask for user for which specific day the user would like to see 
a histogram for each hour.
'''

'''set up constant variables'''
import orderlog
ORDERS = orderlog.orderlst
del ORDERS[0] # remove the headers
OPEN = 360 # the shop opening time (6am) minutes from 00:00
CLOSE = 1440 # the shop close time (24pm) minutes from 00:00
TIMEPERIOD = 60 # the time interval for which the data is summarized

 
'''Function composeOrderMatrix, takes in one parameter - number of days, with a default value of 31.
The function create and return a two-dimensional list,representing the order summary matrix shown in 
the interaction as the shaded part of the order summary display.'''
def composeOrderMatrix(day = 31):
    if day <= 0 or day > 31: day = 31
    day = int(day) 
    rown = int((CLOSE - OPEN)/TIMEPERIOD) # the row number is the number of time interval
     
    OrderMatrix = [] # create an empty list
    new = [] # create a temporary empty list
    
    # create a two-dimensional list of 0s with row number is the number of time interval
    # and the column number is the number of days (the parameter)
    for i in range(rown): 
        for j in range(day): 
            new.append(0) 
        OrderMatrix.append(new)
        new = []
    
    #insert values to the matrix based on the date and time information subtracted from the ORDERS list
    x = 0
    for x in range(len(ORDERS)):
        d = int(ORDERS[x][0][8:10]) # subtract the date information 
        if d <= day:  # the matrix will be updated only if the record date is in the range (smaller than day parameter)
            hr = int(ORDERS[x][0][11:13]) # subtract the hour of the record
            min = int(ORDERS[x][0][14:16]) # subtract the minute of the record
            t = int((hr * TIMEPERIOD + min - OPEN) / TIMEPERIOD) # calculate the time interval of the record
            OrderMatrix[t][d - 1] += 1 # the value matching the date and time interval of the record will be updated
        x += 1 # next record
         
    return OrderMatrix # the function returns a two-dimensional list
 
'''Function printOrderSummaryMatrix(), with a single parameter, a two-dimensional
list of integers. The function should display the content of the matrix '''
def printOrderSummaryMatrix(m):    
    print("ORDER SUMMARY".center(40))  # print title
    print("")
    print("TIME \ DAY".center(16), end = '| ') # this line doesnt end
    for i in range(1,len(m[0]) + 1): # print the day number that
        print('{:>2}'.format(i), end = ' ') # right align for each value, values are separated by a space
    print("\n" + "------------------" + "---" * len(m[0]))
    for i in range(1, int((CLOSE - OPEN)/TIMEPERIOD)): # print the OrderMatrix
        print('{:>17}'.format(str(int(OPEN/TIMEPERIOD) + i - 1) + ":00 - " + 
                              str(int(OPEN/TIMEPERIOD) + i - 1) + ":59 |"), end = " ") # first row shows the time interval
        for j in range(len(m[0])):
            print("{:>2}".format(m[i-1][j]), end = " ") # print the matrix value, right align, values are separated by a space within each column
        print("")


'''Function printHistogram(), which accepts two parameters: a two-dimensional list storing
matrix values and a column number (0-based). 
The function display a histogram, as shown twice in the interaction above for column values 0 and 9. 
The histogram visualizes the numbers from the specified column of the matrix using * symbols, left aligned. '''

def printHistogram(m, c):
    print("\n           NUMBER OF ORDERS PER 60 min FOR DAY " + str(c)) # print header
    print("") # empty line
    for i in range(int((CLOSE - OPEN)/TIMEPERIOD)):
        print('{:>17}'.format(str(int(OPEN/TIMEPERIOD) + i ) + ":00 - " + 
                          str(int(OPEN/TIMEPERIOD) + i ) + ":59 |"), end = " ") # print time interval for the first row
        print("*" * m[i][c - 1])  # take out the value from the matrix parameter and produce corresponding number of *s 


'''method main(), to start the program flow, read user input and call other methods as
needed'''

def main():
    day = eval(input("How many days would you like to include?")) # ask user for a number of days that the report want to include
    order_m = composeOrderMatrix(day) # create a order summary matrix based on the user's request, through function  composeOrderMatrix
    printOrderSummaryMatrix(order_m) # print the order summary matrix
    
    whichday = 0 
    while whichday != -1: # the loop will end if user input -1
        # ask user which day in the date range he/she wants to see a histogram for each time interval data
        whichday = eval(input("Enter day number from 1 to " + str(day) + " to see a histogram, or -1 to exit: ")) 
        if day >= whichday > 0 : printHistogram(order_m, whichday) # print the histogram for day number within the range

    print("Bye!")
main()   

