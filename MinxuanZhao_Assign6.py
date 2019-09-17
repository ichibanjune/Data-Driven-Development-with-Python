'''
Created on Dec 4, 2018, by Minxuan Zhao
Assignment 6
Python 3.4

The program is designed to create two plots
one shows the average ratings by voters in the four age groups identified in the data for a set of
movies selected by the user.
the second a bar graph, showing what percentage of all votes for a movie are contributed by the specific
age-gender group
'''
import matplotlib as mlp
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
pd.options.mode.chained_assignment = None  

def main():
    moviefile = "IMDB.csv"
    folder = input("Please enter the name of the subfolder with the data file:") # ask user for the subfolder where it has the movie data
    moviepath = os.path.join(os.getcwd(), folder, moviefile)
    movieinfo = pd.read_csv(moviepath)
    moviename = movieinfo.iloc[:,0].values.tolist() # create a list of all movie names
    agegroup = pd.DataFrame(movieinfo, columns = ['Title','Genre1','VotesU18','Votes1829','Votes3044','Votes45A']) #columns required for plot1
    agegendergroup = pd.DataFrame(movieinfo, columns = ['Title', 'CVotesU18F','CVotes1829F','CVotes3044F','CVotes45AF', 
                                                     'CVotesU18M', 'CVotes1829M', 'CVotes3044M', 'CVotes45AM']) # columns required for plot2
    
    # create plot 1 with user selected movies
    print("\nPlot1: ratings by age group")
    movienumber = eval(input("How many of the " + str(len(movieinfo)) + " movies would you like to consider?"))
    if movienumber == 1:
        print("Select " + str(movienumber) + " movie")
    else:
        print("Select " + str(movienumber) + " movies")
    pickedmovie = pickMovieWithKeyword(moviename, movienumber)
    pickagegroup = agegroup[agegroup["Title"].isin(pickedmovie)]
    plot1(pickagegroup)
    
    # create plot 2 of a user selected movie
    print ('------------------------------------------------------------------------')
    print ("Plot2: Percentage of raters within gender-age. Select a movie: ")
    plt.figure()    
    movienumber2 = 1
    pickedmovie2 = pickMovieWithKeyword(moviename, movienumber2)
    pickagegender = agegendergroup[agegendergroup["Title"].isin(pickedmovie2)]
    plot2(pickagegender)
    plt.show()
    
'''function pickMovieWithKeyword() take in
one pandas series parameter: moviename,
and one int variable: movienumber
Return a list containing selected movie name'''
def pickMovieWithKeyword(moviename, movienumber):
    pickedmovie = []
    for i in range(movienumber):
        mlist = [] #movie list with keyword in title
        while mlist ==[]: # ensure keep asking user for keyword when there is no matching movie
            keyword = input("\nEnter movie keyword:").strip()
            for j in moviename:
                if keyword.lower() in j.lower():
                    mlist.append(j)
        mdata = pd.DataFrame(mlist, columns = ["Title"])
        mdata["id"] = [k+1 for k in range(len(mdata))] # give a identical number to each movie in the dataframve
        if len(mdata) != 1: # if there are more than 1 movie has the keyword
            print("Which of the following movies would you like to pick (enter number)")
            for j in range(len(mdata)):
                print("\t", mdata.iloc[:,1].iloc[j], mdata.iloc[:,0].iloc[j]) # print matching movies for selection
            movieselect = eval(input("enter a number: "))
        else:
            movieselect = 1
        pick = mdata.loc[mdata["id"] == movieselect, "Title"].iloc[0]
        pickedmovie.append(pick)
        print("Movie #" + str(i+1) + ": \'" + str(pick) + "\'")
    
    return pickedmovie

'''This function creates a plot displays the average ratings by voters in the four age groups identified in the data for a set of
movies selected by the user.
It takes in one parameter of type pandas.dataframe'''
def plot1(pickagegroup):
    plotcontent = pickagegroup.loc[:,("VotesU18", "Votes1829", "Votes3044", "Votes45A")] # selected columns will be plotted
    for i in range(len(pickagegroup)):
        plt.plot(["<18", "18-29", "30-44", ">44"], plotcontent.iloc[i,:], "-o")
        plt.annotate(pickagegroup["Title"].iloc[i] + "(" + pickagegroup["Genre1"].iloc[i] + ")" , (["<18"],plotcontent.iloc[i,0]))
    plt.title("Ratings by age group")
    plt.ylabel("Rating")
    plt.xlabel("Age range")
    plt.grid()
    plt.grid(linestyle = "--", linewidth = 0.5)
    plt.savefig("plot1.jpg", format = "jpg")

'''Plot 2 displays a bar graph, showing what percentage of all votes for a movie are contributed by the specific
age-gender group.
It takes in one parameter of type pandas.dataframe'''
def plot2(pickagegender):
    order = ["Title", "CVotesU18F", "CVotes1829F", "CVotes3044F", "CVotes45AF", "CVotesU18M", "CVotes1829M", "CVotes3044M", "CVotes45AM", "TotalVoters"]
    pickagegender["TotalVoters"] = pickagegender.sum(axis = 1) # calculate total votes
    pickagegender = pickagegender[order]
    for i in range(1, len(pickagegender.columns)-1):
        pickagegender.iloc[0,i] = round( (pickagegender.iloc[0,i] / pickagegender.iloc[0,-1]) * 100 , 1) # calculate percentage for each group
    label = ['<18f', '18-29f', '30-44f', '>44f','<18m', '18-29m', '30-44m', '>44m']
    x = np.arange(8)
    y = np.arange(4)
    z = np.arange(4,8)
    plt.bar(x,0)
    plt.bar(y, pickagegender.iloc[0,1:5], color = "m")
    plt.bar(z, pickagegender.iloc[0,5:-1], color = "skyblue")
    plt.xticks(x, label,fontsize = 10, rotation=30)
    plt.ylabel("% of raters")
    name = pickagegender["Title"].iloc[0]
    plt.title("Percentage of raters within gender-age group for "+ "'" + name + "'")
    new = [x for x in pickagegender.iloc[0, 1:-1]]
    for m,n in enumerate(new):
        plt.text(m - 0.5, n+0.5 ,str(n) + "%")
    plt.savefig("plot2.jpg", format = "jpg")

main()








































