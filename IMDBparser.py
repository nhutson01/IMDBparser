
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 21:21:25 2019

IMDBparser

This program was created as a personal project for learning more about web 
scraping.

@author: Noah Hutson
"""
from bs4 import BeautifulSoup as bs
import numpy as np
import matplotlib.pyplot as plt
import requests
import pandas as pd
import re
import unidecode
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

customList = pd.DataFrame([], columns=['title', 'genre', 'age rating', 'desc', \
                  'dir', 'stars', 'runtime', 'metascore', 'awards', \
                  'ratingText', 'story'])
def getInTheaters():
    movie_list = soup.find('div', class_ = 'list detail')
    movie_containers = soup.find_all('div', class_ = 'list_item')
    mvList = []
    for movie in movie_containers:
        myDeets = []
        myDeets.append(movie.h4.a.text)                          # title
        
        if(movie.find('span', class_='metascore') is not None):
            ms = int(movie.find('span', class_='metascore').text)
            myDeets.append(ms)                                  # metascore
        else:
            myDeets.append("NA")
         
        myDeets[0] = myDeets[0].strip()
        mvList.append(myDeets)
        
    df = pd.DataFrame(mvList)
    df.columns = ['title', 'metascore']
    return(df)
    
def getComingSoon():
    main = soup.find('div', attrs = {'id':'main'})
    movie_list = soup.find('div', class_ = 'list detail')
    movie_containers = soup.find_all('div', class_ = 'list_item')
    mvList = []
    for movie in movie_containers:
        myDeets = []
        myDeets.append(movie.h4.a.text)                              # title
        
        if(movie.find('span', class_='metascore') is not None):
            ms = int(movie.find('span', class_='metascore').text)
            myDeets.append(ms)                                  # metascore
        else:
            myDeets.append("NA")
        
        myDeets[0] = myDeets[0].strip()
        mvList.append(myDeets)
    
    df = pd.DataFrame(mvList)
    df.columns = ['title', 'metascore']
    return(df)
    
def printMovieDetails(movie):
    print(f"\n-----{movie['title']}-----")
    if(movie['age rating'] != 'NA'):
        print(f"{movie['age rating']}", end=' | ')
    if(movie['runtime'] != 'NA'):
        print(movie['runtime'], end=' | ')
    if(movie['genre'] != 'NA'):
        if(len(movie)>8):
            for genre in movie['genre']:
                if(genre == movie['genre'][-1]):
                    print(genre)
                else:
                    print(genre, end=' | ')
        else:
            print(movie['genre'])
    if(movie['metascore'] != 'NA'):
        print(f"\n{movie['metascore']} Metascore")
    if(movie['desc'] != "NA"):
        print(f"\n{movie['desc']}")
    if(movie['dir'] != "NA"):
        print(f"\nDirected by {movie['dir']}")
    if len(movie['stars'])>0 and \
    movie['stars'][0] != "NA":
        print("Starring: ", end='')
        for star in movie['stars']:
            if star == movie['stars'][-1]:
                if star == movie['stars'][0]:
                    print(f"{star}")
                else:
                    print(f"and {star}")
            else:
                print(star, sep=', ', end=', ')
    if(len(movie)>8):
        if(movie['awards'] != "NA"):
            print()
            print(movie['awards'])
        if(movie['ratingText'] != "NA"):
            print("\nIMDB score:",movie['ratingText'])
    
            
def getTitle(mySoup):
    if("No results found for " in mySoup.text):
        print("\n-----No results found.-----")
        return(0)
    sections = mySoup.find_all('div', class_='findSection')
    for sec in sections:
        if sec.h3.text == 'Titles':
            titleSec = sec
    if sections is None:
        sec = mySoup.find('div', class_='findSection')
        titleURL = sec.tr.find('a')['href']
    else: 
        if(len(sections)<1):
            print("\n-----No results found.-----")
            return(0)
        titleURL = titleSec.tr.find('a')['href']
    url = base + titleURL
    t = requests.get(url)
    soup2 = bs(t.text, 'html.parser')
    title = soup2.h1.text.strip()
    subtext = soup2.find('div', class_='subtext')
    deets = subtext.text
    if(deets is not None):
        s = re.match('^\s+(\S+\s?\S*)\s', deets)
        ageRating = s.group(1).strip()
    else:
        ageRating = "NA"
    if(subtext.time is not None):
        time = subtext.time.text.strip()
    else:
        time = "NA"
    if(ageRating == time or ageRating in time):
        ageRating = "NA"
    if(subtext.find_all('a') is not None):
        genreTags = subtext.find_all('a')
        genres = []
        for genre in genreTags:
            if(genre == genreTags[-1]):
                releaseDate = genre.text.strip() #not used yet
            else:
                genres.append(genre.text.strip())
                if (genre.text in ageRating):
                    ageRating = "NA"
    else:
        genres = "NA"
    
    if(soup2.find('div', class_='ratingValue') is not None):
        ratingText = soup2.find('div', class_='ratingValue').strong['title']
        ratingVal = re.match('^(.{3})', ratingText).group(1) # not used yet
        userVotes = re.match('^.+on (.+) user', ratingText).group(1) # not used yet
    else:
        ratingText = "NA"
    plotSum = soup2.find('div', class_='plot_summary')
    items = plotSum.find_all('div')
    if("Add a Plot" in items[0].text.strip() or \
       "See full summary" in items[0].text.strip()):
        desc = "NA"
    else:
        desc = items[0].text.strip()
    if(len(items)>1):
        director = items[1].a.text.strip()
        starTags = plotSum.find_all('a')
        stars = []
        for star in starTags:
            if star == starTags[-1]\
            or star.text.strip() == director or \
            "Add a Plot" in star.text.strip() or \
            "See full summary" in star.text.strip() or \
            "more credit" in star.text.strip():
                continue
            else:
                stars.append(star.text.strip())
    else:
        director = "NA"
        stars = ["NA"]
    
    if(soup2.find('div', class_='titleReviewBarItem') is not None):
        metascore = soup2.find('div', class_='titleReviewBarItem').span.text
        if "user" in metascore or \
        "(" in metascore or \
        "critic" in metascore:
            metascore = "NA"
        
    else:
        metascore = "NA"
    if(soup2.find('span', class_='awards-blurb') is not None):
        awards = soup2.find('span', class_='awards-blurb').text.strip()
        awards = re.sub('\s+', ' ', awards)
    else:
        awards = "NA"
    if(soup2.find('div', class_='article', attrs = {'id':'titleStoryLine'})):
        if(soup2.find('div', class_='article', attrs = {'id':'titleStoryLine'}).p \
           is not None):
            story = soup2.find('div', class_='article', \
                               attrs = {'id':'titleStoryLine'}).p.span.text.strip()
        else:
            story = "NA"
    else:
        story = "NA"
    df = pd.DataFrame([[title, genres, ageRating, desc, director, stars, \
                       time, metascore, awards, ratingText, story]])
    df.columns = ['title', 'genre', 'age rating', 'desc', \
                  'dir', 'stars', 'runtime', 'metascore', 'awards', \
                  'ratingText', 'story']
    return(df)

def printMultipleTitles(df):
    global customList
    prevCustomList = customList
    choiceNum2 = 1
    deletedMovie = ''
    deleted = 0
    while(choiceNum2 != 0):
        choiceNum2 = 1
        i = 1
        if(isinstance(customList, pd.DataFrame) or isinstance(customList, list)):
            if(len(prevCustomList) > len(customList)):
                if(df.equals(pd.DataFrame(prevCustomList))): # we are viewing list
                    df = pd.DataFrame(customList, columns = ['title', 'genre', 'age rating', 'desc', \
                                                             'dir', 'stars', 'runtime', 'metascore', 'awards', \
                                                             'ratingText', 'story'])
                if(len(df) > len(customList)):
                    df = pd.DataFrame(customList, columns = ['title', 'genre', 'age rating', 'desc', \
                                                             'dir', 'stars', 'runtime', 'metascore', 'awards', \
                                                             'ratingText', 'story'])
                    deleted = 1
        
        if(len(df)==0):
            return
        validTitles = [] # keep track of title #s
        mScores = []
        anyNotRated = 0
        for v in df.values:
            title = v[0]
            if(len(df)>2):
                title = df.iloc[i-1]['title']
            validTitles.append(str(i))
            print(f"\nTitle #{i}: {title}")
            i = i+1
            try:
                mScores.append((v[0],int(v[-1])))
            except ValueError:
                anyNotRated = 1
                continue

        npScores = np.array(mScores)
        noneRated = 0
        if(len(df['metascore'])>0 and len(df[df.metascore != "NA"]['metascore'].values)>0):
            df = df.fillna("NA")
            df[df.metascore != "NA"] = df[df.metascore != "NA"].astype({'metascore': 'int16'})
            highMS = np.max(df[df.metascore != "NA"]['metascore'])
            highMovie = df[df['metascore']==highMS].title.values[0]
            msMean = df[df.metascore != "NA"]['metascore'].mean().round(2)
            i = 0
            for name in df['title'].values:
                if(name == highMovie):
                    highIndex = i+1
                    break
                i = i+1
                
        else:
            noneRated = 1
            print("\nNone of these titles have a Metascore rating.")
        if(noneRated == 0):
            print(f"\n#{highIndex} {highMovie} is the highest rated movie of this selection, \
with a Metascore rating of {highMS}.", end=' ')
            print(f"\nThe average Metascore rating of this selection is {msMean}.")
            if anyNotRated:
                print(f"Keep in mind, not all of these titles have been rated.")
            else:
                print()
        print(f"\nEnter a title number to view more information about it.\n\
i.e. '1' to view details on {df.iloc[1-1]['title']}\n\nEnter 'b' to select another \
list of movies.\nEnter 'w' to write this list to a file.\n\
Enter 'g' to graph the ratings.\nEnter 'q' to quit.")
        
        if(str(choiceNum2) not in validTitles):
            print("\n****Please enter a valid number****")
        if(deleted == 1):
            print(f"\nDeleted {deletedMovie}.")
        choiceNum2 = input("Enter title number: ")
    
        if(choiceNum2 == 'q' or choiceNum2 == 'Q' or choiceNum2 == 'b'\
           or choiceNum2 == 'B'):
            break
        
        if(choiceNum2 == 'w' or choiceNum2 == 'W'):
            writeListToCsv(df)
        
        if(choiceNum2 == 'g' or choiceNum2 == 'G'):
            graphList(df)
        
        if(choiceNum2 not in validTitles):
            continue
        
        title = df.iloc[int(choiceNum2)-1]['title'].strip()
        title = title.replace(' ', '+')
        title = re.sub(r'\s+', '+', title)
        title = unidecode.unidecode(title) # remove accented characters
        if (re.match(r'^(.+)\+\(\d{4}\)', title) is not None):
            title = re.match(r'^(.+)\+\(\d{4}\)', title).group(1).strip()
        titleToUrl = findTitle + title
     
        r = requests.get(titleToUrl)
        if(r.status_code != 200):
            print("\nError! Page not found!")
        
        searchSoup = bs(r.text, 'html.parser')
        
        myDf = getTitle(searchSoup)
        if(isinstance(myDf, int)):
            continue
        printMovieDetails(myDf.iloc[0])
        
        if(re.match(r'^(.+)\(\d{4}\)', myDf.iloc[0]['title'])) is None:
            name = myDf.iloc[0]['title']
        else:
            name = re.match(r'^(.+)\(\d{4}\)', myDf.iloc[0]['title']).group(1).strip()
        inCustom = False
        try:
            for val in customList['title'].values:
                if name in val:
                    inCustom = True
                    break
        except TypeError:
            for val in customList:
                print(val)
        
        if(myDf.iloc[0]['story'] is None or \
           myDf.iloc[0]['desc'] == myDf.iloc[0]['story'] or
           myDf.iloc[0]['story'] == "NA"):
            print()
            if(inCustom == False):
                answer = input("Enter 'y' to add movie to custom list, or anything else \
to continue: ")
                if(answer == 'y' or answer == 'Y'):
                    customList = customList.append(myDf.iloc[0])
                    continue
            else:
                myInp = input("Enter 'd' to delete movie from custom list, or anything \
else to continue.")
                if(myInp == 'd' or myInp == 'D'):
                    i = 0
                    for val in customList['title'].values:
                            if name in val:
                                valToRmv = val
                    for val in customList:
                        if val[0] == myDf.iloc[0]['title']:
                            customList1 = customList[0:i]
                            customList2 = customList[i+1::]
                            customList = customList1 + customList2
                            break
                        i = i+1
                    deletedMovie = valToRmv
                    customList = customList[customList['title'] != valToRmv]
            continue
        else:
            choiceNum2 = 1
            choiceNum2 = input("Enter 's' to view this title's storyline, 'q' to quit\n\
Or enter anything else to continue: ")
            if(choiceNum2 == 'q' or choiceNum2 == 'Q'):
                break
            if(choiceNum2 == 's'):
                print("\nStoryline")
                print("----------------")
                print(myDf.iloc[0]['story'])
                if(inCustom):
                    myInp = input("Enter 'd' to delete movie from custom list, or anything \
else to continue.")
                    if(myInp == 'd' or myInp == 'D'):
                        i = 0
                        for val in customList['title'].values:
                            if name in val:
                                valToRmv = val
                        for val in customList:
                            if val[0] == myDf.iloc[0]['title']:
                                customList1 = customList[0:i]
                                customList2 = customList[i+1::]
                                customList = customList1 + customList2
                                break
                            i = i+1
                        deletedMovie = valToRmv
                        customList = customList[customList['title'] != valToRmv]
                    continue
            if(inCustom) == False:
                answer = input("Enter 'y' to add movie to custom list, or anything else \
to continue: ")
                if(answer == 'y' or answer == 'Y'):
                    customList = customList.append(myDf.iloc[0])
                    continue
            if(inCustom):
                    myInp = input("Enter 'd' to delete movie from custom list, or anything \
else to continue.")
                    if(myInp == 'd' or myInp == 'D'):
                        i = 0
                        for val in customList['title'].values:
                            if name in val:
                                valToRmv = val
                        for val in customList:  
                            if val[0] == myDf.iloc[0]['title']:
                                customList1 = customList[0:i]
                                customList2 = customList[i+1::]
                                customList = customList1 + customList2
                                break
                            i = i+1
                        deletedMovie = valToRmv
                        customList = customList[customList['title'] != valToRmv]
                    continue
    return(choiceNum2)
    
def viewCustomList():
    if(len(customList)==0):
        print("\nCustom list is empty!")
        return
    tmp = pd.DataFrame(customList)
    ch2 = printMultipleTitles(tmp)
    return ch2

def writeListToCsv(df):
    fileName = input("\nEnter the name of the file to write to: ")
    if(".csv" in fileName):
        df.to_csv(fileName, index=False)
    else:
        fileName = fileName + ".csv"
        df.to_csv(fileName, index=False)

def importList():
    global customList
    fileName = input("\nEnter the name of the file to import: ")
    if(".csv" in fileName):
        try:
            df = pd.read_csv(fileName)
        except FileNotFoundError:
            print("\nError! could not find ", fileName)
            return
    else:
        fileName = fileName + ".csv"
        try:
            df = pd.read_csv(fileName)
        except FileNotFoundError:
            print("\nError! could not find", fileName)
            return
    if(len(customList)>0):
        choice = input("Enter 'o' to overwrite custom list, or anything else to append to it.\n")
        if(choice == 'o'):
            customList = df
        else:
            customList = customList.append(df)
    else:
        customList = df
        
def graphList(df):
    fig, (ax1, ax2) = plt.subplots(2, figsize=(5,10), constrained_layout=True)
    
    tmp = df[df.metascore != "NA"].set_index('title')['metascore']
    tmp.plot(kind="bar", ax=ax1)
    ax1.set_title("Metascore Ratings", fontsize=16)
    ax1.set_xlabel("Movie Titles", fontsize=16)
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation = 90)
    ax1.set_ylabel("Ratings", fontsize=16)
    tmp.plot(kind='hist', bins=20, ax=ax2)
    ax2.set_title("Metascore Histogram", fontsize=16)
    ax2.set_ylabel("Frequency",fontsize=16)
    ax2.set_xlabel("Ratings",fontsize=16)
    
    plt.show()
    print("If it's difficult to read the movie titles, try saving the graphs.")
    save = input("Enter 's' to save these graphs. or anything else to continue.\n")
    if(save == 's' or save == 'S'):
        graphName = input("Enter file name to save to: ")
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation = 90, fontsize=12)
        fig.set_size_inches(15.5, 10.5)
        fig.savefig(graphName, dpi=100)
        
base = "https://www.imdb.com"
inTheaters = "https://www.imdb.com/movies-in-theaters/?ref_=nv_mv_inth"
topMovies = "https://www.imdb.com/chart/top?ref_=nv_mv_250"
comingSoon = "https://www.imdb.com/movies-coming-soon/?ref_=nv_mv_cs"
selectMonth = "https://www.imdb.com/movies-coming-soon/"
findTitle = "https://www.imdb.com/find?"
choices = [inTheaters, comingSoon, selectMonth, '', findTitle]

soup = bs(requests.get(selectMonth).text, 'html.parser')
currYear = soup.find('div', class_='nav').option.text
currYear = currYear.strip()
currYear = re.findall(r'\d+', currYear)

validMonths = ['1','2','3','4','5','6','7','8','9','10','11','12',\
               '01','02','03','04','05','06','07','08','09']

validYears = range(2011, int(currYear[0])+1)

validChoices = ['1','2','3', '4', '5', '6', '7']
choiceNum = 1

while(choiceNum != 0):
    print(f"\n{len(customList)} titles in custom list.")
    print("\nMovies in theaters: 1\nComing soon: 2\n\
Select month in current year: 3\nSelect month and year: 4\n\
Search for a title: 5\nView custom list: 6\n\
Import custom list: 7\nOr 'q' to quit.")
    choiceNum = input("Enter your choice: ")
    
    if(choiceNum == 'q' or choiceNum == 'Q'):
        break
    
    if(choiceNum not in validChoices):
        print("\n****Please enter a valid option****\n")
        continue
    
    if(choiceNum=='3'):
        choices[int(choiceNum)-1] = selectMonth + f"{currYear[0]}-"
        month = 0
        while(month not in validMonths):
            month = input("Enter a month's date (i.e. '6' for June): ")
            if(month not in validMonths):
                print("\n****Please enter a valid month****\n")
                continue
            month = "{:02d}".format(int(month))
            choices[int(choiceNum)-1] = choices[int(choiceNum)-1] + month
            
    if(choiceNum=='4'):
        year = 0
        while(year not in validYears):
            try:
                year = int(input("Enter a year (earliest 2011, latest current year): "))
            except ValueError:
                print("\n****Please enter a valid year****\n")
                continue
            
            if(int(year) not in validYears):
                print("\n****Please enter a valid year****\n")
                continue
            choices[int(choiceNum)-1] = selectMonth + f"{year}-"
        month = 0
        while(month not in validMonths):
            month = input("Enter a month's date (i.e. '6' for June): ")
            if(month not in validMonths):
                print("\n****Please enter a valid month****\n")
                continue
            month = "{:02d}".format(int(month))
            choices[int(choiceNum)-1] = choices[int(choiceNum)-1] + month
            
    if(choiceNum=='5'):
        search = input("Enter the title you are searching for: ")
        search = search.replace(' ', '+')
        choices[int(choiceNum)-1] = findTitle + search
    
    if(choiceNum=='6'):
        ch2 = viewCustomList()
        if(ch2 == 'q' or ch2 == 'Q'):
            break
        continue
    
    if(choiceNum=='7'):
        importList()
        continue
        
    url = choices[int(choiceNum)-1]
    r = requests.get(url)

    if(r.status_code != 200):
        print("\nError! Page not found!")


    soup = bs(r.text, 'html.parser')
    
    if(choiceNum==validChoices[0]):
        df = getInTheaters()
        ch2 = printMultipleTitles(df)
        
        if(ch2 == 'q' or ch2 == 'Q'):
            break
    elif(choiceNum==validChoices[4]):
        df = getTitle(soup)
        if(isinstance(df, int)):
            continue
        printMovieDetails(df.iloc[0])
        
        if(df.iloc[0]['story'] is None or \
           df.iloc[0]['desc'] == df.iloc[0]['story'] or
           df.iloc[0]['story'] == "NA"):
            if(df.iloc[0]['title'] in pd.DataFrame(customList).values) == False:
                print()
                answer = input("Enter 'y' to add movie to custom list, or anything else \
to continue: ")
                if(answer == 'y' or answer == 'Y'):
                    customList = customList.append(df.iloc[0])
                continue
            myInp = input("Enter 'd' to delete movie from custom list, or anything \
else to continue.")
            if(myInp == 'd' or myInp == 'D'):
                i = 0
                for val in customList['title'].values:
                    if name in val:
                        valToRmv = val
                for val in customList:
                    if val[0] == df.iloc[0]['title']:
                        customList1 = customList[0:i]
                        customList2 = customList[i+1::]
                        customList = customList1 + customList2
                        break
                    i = i+1
                customList = customList[customList['title'] != valToRmv]
            continue
        else:
            choiceNum2 = 1
            choiceNum2 = input("Enter 's' to view this title's storyline, 'q' to quit\n\
Or enter anything else to continue: ")
            if(choiceNum2 == 'q' or choiceNum2 == 'Q'):
                break
            if(choiceNum2 == 's'):
                print("\nStoryline")
                print("----------------")
                print(df.iloc[0]['story'])
                if(df.iloc[0]['title'] in pd.DataFrame(customList).values):
                    myInp = input("Enter 'd' to delete movie from custom list, or anything \
else to continue.")
                    if(myInp == 'd' or myInp == 'D'):
                        i = 0
                        for val in customList['title'].values:
                            if name in val:
                                valToRmv = val
                        for val in customList:
                            if val[0] == df.iloc[0]['title']:
                                customList1 = customList[0:i]
                                customList2 = customList[i+1::]
                                customList = customList1 + customList2
                                break
                            i = i+1
                        customList = customList[customList['title'] != valToRmv]
                    continue
            if(df.iloc[0]['title'] in pd.DataFrame(customList).values) == False:
                answer = input("Enter 'y' to add movie to custom list, or anything else \
to continue: ")
                if(answer == 'y' or answer == 'Y'):
                    customList = customList.append(df.iloc[0])
    else:
        df = getComingSoon()
        ch2 = printMultipleTitles(df)
        
        if(ch2 == 'q' or ch2 == 'Q'):
            break
    
    
print("\nGoodbye!")
