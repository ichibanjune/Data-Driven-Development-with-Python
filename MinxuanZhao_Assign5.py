'''
Created on Nov 20, 2018, by Minxuan Zhao
Assignment 5
python 3.4

The program will Ask the user to specify the subfolder in the current working directory, 
where the files are stored, along with the names of the critics, person and movies data files.
Then the program will determine and output the names of three critics, whose ratings of the 
movies are closest to the person’s ratings based on the Euclidean distance.
The program will then identify recommendations of movies for each genre that are rated 
highest by the three critics。
'''

import pandas as pd
import numpy as np
import os
from scipy.spatial import distance

# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)

#     data IMDB.csv ratings.csv p8.csv
def main():
    '''ask the user for the subfolder, name of movies file, name of critics file, and the name of personal ratings file'''
    fileinfo = input("Please enter the name of the folder with files, the name of movies file, \nthe name of critics file, the name of personal ratings file, separated by spaces: \n")
    folder = fileinfo.split()[0]
    moviefile = fileinfo.split()[1]
    critics = fileinfo.split()[2]
    prating = fileinfo.split()[3]
    
    '''create pandas data frames for movie info, critics rating, and personal rating'''
    moviedata = getMovie(folder, moviefile)
    criticsdata = getCriticRate(folder, critics)
    pratingdata = getPersonal(folder, prating)
    
    '''find the three closest critics for the person'''
    critics3 = findClosestCritics(criticsdata, pratingdata)
    
    '''get the movie recommendations for the person'''
    movierecommend = recommendMovies(criticsdata, pratingdata, critics3, moviedata)
    
    print("\n", critics3, "\n") # print the three closest critics
    pname = pratingdata.columns.values.tolist()[1] # take the person's name
    printRecommendations(movierecommend, pname) # use the function to print the movie recommendations for the person

'''The function getMovie() takes in two string: the subfolder and the name of the movie file,
and return a data frame of movie information '''
def getMovie(folder, moviefile):
    moviepath = os.path.join(os.getcwd(), folder, moviefile)
    movieinfo = pd.read_csv(moviepath, usecols = 'Title Year Rating Genre1 Budget Runtime'.split(), encoding = "latin1")
    return movieinfo

'''The function getCriticRate() takes in two string: the subfolder and the name of the critics rating file,
then return a data frame of all critics ratings'''
def getCriticRate(folder, critics):
    criticspath = os.path.join(os.getcwd(), folder, critics)
    criticsrate = pd.read_csv(criticspath, encoding = "latin1")
    return criticsrate

'''The function getPersonal() takes in two string: the subfolder and the name of the personal rating file,
then return a data frame of the personal ratings'''
def getPersonal(folder, prating):
    pratingpath = os.path.join(os.getcwd(), folder, prating)
    pratinginfo = pd.read_csv(pratingpath, encoding = "latin1")
    return pratinginfo

'''Function findClosestCritics takes in two parameters, the first one providing
data about critics ratings, and the second, about personal ratings.
The function should return a list of three critics, whose ratings of movies are most 
similar to those provided in the personal ratings data, based on Euclidean distance.'''
def findClosestCritics(criticsrate, pratinginfo):

    '''select critics ratings of the movies rated by the person'''
    pratedmovie = []
    for i in range(len(pratinginfo)):
        pratedmovie.append(criticsrate[criticsrate.Title == pratinginfo.ix[:,0][i]].values.tolist()[0])
    y = criticsrate.columns.values.tolist()
    criticsD = pd.DataFrame(pratedmovie, columns = y)
    
    '''take out all rating values to numpy array for easy calculation'''
    ratings = criticsD.loc[:,y[1]:].values
    # transpose the np array so each row is ratings for all movies from one critics, ease the euclidean calculation
    ratings = np.transpose(ratings) 
    
    '''take out the personal rating to numpy array'''
    p = pratinginfo.columns.values.tolist()
    prate = pratinginfo.loc[:,p[1]:].values
    
    '''calculate the euclidean distance between each critics and the person'''  
    dist = []  
    for i in range(len(ratings)):
        d = distance.euclidean(ratings[i], prate)
        dist.append(d)
    
    '''sort critics by distance'''
    distcritics = pd.DataFrame(columns = ["critics", "distance"])
    distcritics.critics = y[1:]
    distcritics.distance = dist
    distcritics = distcritics.sort_values(by = ["distance"])
    
    '''take out the closest three critics and put them into a list'''
    closest3 = distcritics.head(3).ix[:,0].values.tolist()

    return closest3
    
'''Function recommendMovies () takes in four parameters:
1 - the critics dataframe
2 - the personal rating dataframe
3 - list of the three closest critics
4 - the movie dataframe
then return a set of movie recommendations based on the average ratings from the closest critics'''
def recommendMovies (criticsrate, pratinginfo, listcritics, movieinfo):
    
    '''find movies not rated by the person, but rated by critics'''
    watchedmovies = pratinginfo.ix[:,0].values.tolist()
    movierating = criticsrate.query("Title not in @watchedmovies")
    
    '''ratings by closest 3 critics'''
    lista = listcritics.copy()
    lista.insert(0,"Title")
    movierating = movierating.filter(items = lista) # new data frame containing all movie ratings by the 3 critics
    
    '''add a column to show average ratings'''
    movierating["AvgRating"] = movierating.mean(axis = 1)
    
    '''add a column to show the genre of the movies'''
    movierating["Genre"] = movierating["Title"].map(movieinfo.set_index("Title")["Genre1"])
    
    '''find the highest rating movie for each genre and copy to new dataframe'''
    maxr = movierating.groupby("Genre")["AvgRating"].transform(max) == movierating["AvgRating"]
    maxrate = movierating[maxr].copy()
    
    '''add movie year and runtime for highest rated movies'''
    maxrate["Year"] = maxrate["Title"].map(movieinfo.set_index("Title")["Year"])
    maxrate["Runtime"] = maxrate["Title"].map(movieinfo.set_index("Title")["Runtime"])
    
    '''sort the data frame by genre'''
    maxrate = maxrate.sort_values(by = ["Genre"])
    
    '''drop the individual ratings from the closest critics,
    keep column: 'Title', 'AvgRating', 'Genre', 'Year', 'Runtime' '''
    maxrate = maxrate.drop( listcritics, axis = 1)
    
    return maxrate

'''function printRecommendations takes in two parameters 
one is data frame containing recommended movie information
second is a string of the person's name
The function produces a printout of all recommendations passed in via the first parameter, 
in alphabetical order by the genre. '''
def printRecommendations (movierecommend, pname):
    
    print("Recommendations for " + pname + ":")
    for i in range(len(movierecommend)):
        if pd.isnull(movierecommend["Runtime"].iloc[i]):
            print('{:<40}'.format("\"" + movierecommend["Title"].iloc[i] + "\"") + "(" + str(movierecommend["Genre"].iloc[i]) + "), rating:",
                  str(round(movierecommend["AvgRating"].iloc[i], 2)) + "," + str(movierecommend["Year"].iloc[i]))    
        else:
            print('{:<40}'.format("\"" + movierecommend["Title"].iloc[i] + "\"") + "(" + str(movierecommend["Genre"].iloc[i]) + "), rating:",
                  str(round(movierecommend["AvgRating"].iloc[i], 2)) + "," + str(movierecommend["Year"].iloc[i]) + ", runs " + str(movierecommend["Runtime"].iloc[i]))

main()