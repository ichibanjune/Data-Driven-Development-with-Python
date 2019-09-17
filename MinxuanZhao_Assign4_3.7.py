'''
Created on Oct 30, 2018 by Minxuan Zhao

This program ask the user for a subfolder name where the course and student info
are stored and a course number that the user would like to know about.
Returns the number of students who are eligible to take the course next semester

This program works with python 3.7
'''
import os

############################################################################
# the main() function run and calls all supportive functions
def main():
    path = input("Please enter the name of the subfolder with files: ") # ask user for the subfolder
    cNum = input("Enter course number or press enter to stop: ") #ask user for the course number
    cName = ""
    
    #keep asking user for course number that the user would like to learn about until they hit enter
    while cNum :
        stuNum = estimateClass(cNum, path) # check if the course exists
        if stuNum == set():
            print("There are 0 students who could take course " + cNum + " None")
        else: # if the course exists
            dictCourseName = initFromFiles(path)[0] # find the dictionary that contains the course numbers and names
            cName = dictCourseName[cNum] # find the course name corresponding to the course number taken in
            print("There are " + str(len(stuNum)) + " students who could take course " + cNum + " " + cName)
        cNum = input("Enter course number or press enter to stop: ") # ask user for next step


#############################################################################
'''with a single parameter of type str, providing the path to a program
description file. The function should construct a dictionary based on the information in the file. The
dictionary should have keys equal to the course numbers, and values for keys equal to the corresponding
course titles, e.g.
{'1001': 'Transfiguration.', '1100': 'Charms.', '1250': 'Defense Against The
Dark Arts.', '1380': 'Potions.', '1420': 'Arithmancy.', '2075': 'Flying.'}
The function must return a tuple, consisting of the program name and the created dictionary
'''
def processProgramFile(filepath):
    dictCourse = {}
    programT = ()
    
    with open(filepath) as file:
        title = [next(file) for i in range(1)]
        pName = title[0].strip('\n') # take the first line from the file for program name
        line = [x.strip() for x in file.readlines()]   # take the rest lines for courses 
    for i in range(len(line)):
        dictCourse[line[i].split()[0]] = line[i][5:] # create a dictionary with keys of course numbers and values of course names
    programT = pName, dictCourse # create a tuple that consists of program name and its courses in a dictionary
    
    return programT # returns the tuple

############################################################################
'''with a single parameter of type str, providing the path to a file
defining prerequisites. The function should construct a dictionary based on the information in the file. A
line in the file of the form 1250: 1001 1100 indicates that 1250 has two prerequisite courses: 1001
and 1100. The dictionary should have keys equal to the course number, and values for keys equal to the
corresponding prerequisite courses. Only courses that have prerequisites should be included in this
dictionary.
The function must return the constructed dictionary
'''

def processPrereqsFile(prereqPath):
    dictPre = {}
    #take out the content from the file
    with open(prereqPath) as file:
        line = [x.strip() for x in file.readlines()]
    #put courses and their prereqs into a dictionary
    for i in range(len(line)):
        dictPre[line[i].split(":")[0]] = line[i].split(" ")[1:]
    
    return dictPre

####################################################################################################
'''with a single parameter, defining the subfolder with the class list
files, as outlined in the Data section. The function should construct a dictionary with keys
corresponding to course numbers. The value for each key must be equal to the set of students who have
taken the course designated by the key.
The function must return the constructed dictionary.
'''
def processClassFiles(classpath):
    dictCourseStu = {}
    current = os.getcwd() # get current directory
    sub = os.path.join(current, classpath) # join the subfolder to the path
    filelist = os.listdir(sub) #take all files from the subfolder
    
    for i in range(len(filelist)): #run through all files in the subfolder
        if filelist[i] != "prereqs.txt" and filelist[i] != "program1.txt" and filelist[i] != "program2.txt": # only work with class list files
            with open(os.path.join(sub, filelist[i])) as file: # for each file, open
                line = [x.strip() for x in file.readlines()]
                if filelist[i][filelist[i].find("c")+1:filelist[i].find("-")] not in dictCourseStu: #if the course is first time loaded
                    dictCourseStu[filelist[i][filelist[i].find("c")+1:filelist[i].find("-")]] = set([line[j].split()[0] for j in range(len(line))]) 
                    # create a new dictionary for the course
                elif filelist[i][filelist[i].find("c")+1:filelist[i].find("-")] in dictCourseStu: # if the dictionary of the course exists
                    for j in range(len(line)):
                        dictCourseStu[filelist[i][filelist[i].find("c")+1:filelist[i].find("-")]].add(line[j].split()[0])
                        # add each line in the file to the existing dictionary with the corresponding course list
    
    return dictCourseStu

#############################################################################################
'''with a single parameter, defining the subfolder with the files.
The method should call functions specified in items a-c above to process data provided in the files. The
function should return a tuple with the constructed dictionaries for program courses, class lists and
prerequisites.
'''
def initFromFiles(subfolder):
    current = os.getcwd()# get current working directory
    sub = os.path.join(current, subfolder) # join the subfolder
    
    p1 = processProgramFile(os.path.join(sub,"program1.txt")) #take courses for program 1
    p2 = processProgramFile(os.path.join(sub,"program2.txt")) # take courses for program 2
    dictCour= dict(p1[1],**p2[1]) #create a dictionary that contains all course numbers and names, regardless of program
    prereqs = processPrereqsFile(os.path.join(sub,"prereqs.txt")) #load a dictionary with courses and their prerequisites
    
    classList = processClassFiles(sub) # load class list and students who took or is taking the class

    report = dictCour, classList, prereqs # create a tuple including courses, class lists, and prerequisites
    
    return report

################################################################################################
'''which will be passed a course number and other parameters of your
choosing, and which will return a set of students who would be eligible to take the course, specified by
the parameter, in the next semester. If the parameter does not refer to a valid course number, the
function should return an empty set. Note: this function should not be working with files, but should
get all needed information from the appropriate data structures created from files
'''
#this function will be passed a course number and the subfolder where the class files are stored
def estimateClass(cn, path):
    student = set()
    allStu = set()
    dictCourseStu = initFromFiles(path)[1] # load class list into a dictionary
    dictPre = initFromFiles(path)[2] # load course prerequisites into a dictionary
    
    for n in dictCourseStu:
        allStu = allStu.union(dictCourseStu[n]) # create a set with all enrolled students
    
    k = 1
    if cn not in dictCourseStu.keys(): #if the taken in course number does not exist
        student = set() #no student
    elif cn in dictPre.keys(): # if the taken in course has one or more prereqs
        for elem in dictPre[cn]:
            if k == 1:  # run only once
                student = student.union(dictCourseStu[elem]) # join the students who have taken the first prerequisites
                k += 1
            else:
                student = student.intersection(dictCourseStu[elem]) # if multiple prerequisites exist, only include student who took all prereqs
        student = student.difference(dictCourseStu[cn]) # take out of students who have taken the course
    else: # if the taken in course has no prereqs
        student = allStu.difference(dictCourseStu[cn]) # all students - students who took the course = students who are eligible to take the course next semester
    
    return student

####################################################################################
#call the main function
main()





    
