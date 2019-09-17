'''
Created on Sep 11, 2018, by Minxuan Zhao

Programming assignment 2
This program takes in APA format references for book/magazine article/journal article
and output the category, and a list of source components.
'''

'''set up variables'''
# constant variables
BOOK = 'BOOK'
MA = 'MAGAZINE ARTICLE'
JA = 'JOURNAL ARTICLE'

#variables
author = ''
title = ''
year = ''
month = ''
pubtitle = ''
volume = ''
issue = ''
pages = ''
publisher = ''
addr = ''
ref = ''

'''Ask user for a APA citation input'''
ref = input("Please enter a reference")

pubtime = ref[ref.find('(')+1:ref.find(')')] #the publication year/month
aftertime = ref[ref.find(')')+3:len(ref)] # the reference content without author and publication time
aftertitle = '' # the reference content without author, publication year/monthe, and title

#find title
if '!' in aftertime:
    title = aftertime[0:aftertime.find('!')+1]
    aftertitle = aftertime[aftertime.find('!')+2:len(aftertime)]
elif '?' in aftertime:
    title = aftertime[0:aftertime.find('?')+1]
    aftertitle = aftertime[aftertime.find('?')+2:len(aftertime)]
else:
    title = aftertime[0:aftertime.find('.')+1]
    aftertitle = aftertime[aftertime.find('.')+2:len(aftertime)]


#find source components by category
author = ref[0:ref.find('(')]
if not pubtime.isdigit(): #Magazine article contains month information, while book and journal have only year as numbers
    print(MA,'---------------------------------------') #list the category magazine article
    year = pubtime[0:4] #publication year
    x = pubtime[6:len(pubtime)].split()
    month = x[0] #take out the month information
    pubtitle = aftertitle[0:aftertitle.find(',')]
    volume = aftertitle[aftertitle.find(',')+2:aftertitle.find('(')]
    issue = aftertitle[aftertitle.find('(')+1:aftertitle.find(')')]
    pages = aftertitle[aftertitle.find(')')+3:len(aftertitle)]
else: 
    year = pubtime
    if ':' in aftertitle: #different from Journal, books have ':' after their address information, and avoid possible ':' in title
        print(BOOK, '---------------------------------------------------') #list the category book
        addr = aftertitle[0:aftertitle.find(':')]
        publisher = aftertitle[aftertitle.find(':')+2:len(aftertitle)-1]
    else:
        print(JA, '----------------------------------------') #list the category journal article
        pubtitle = aftertitle[0:aftertitle.find(',')]
        volume = aftertitle[aftertitle.find(',')+2:aftertitle.find('(')]
        issue = aftertitle[aftertitle.find('(')+1:aftertitle.find(')')]
        pages = aftertitle[aftertitle.find(')')+3:len(aftertitle)]

if pages.endswith('.'):
    pages = pages[0:len(pages)-1] #the source may end with '.', which is not expected for output

'''Printing the output'''
    
print('{:>20}'.format('AUTHORS:'), author)
print('{:>20}'.format('TITLE:'), title)
print('{:>20}'.format('YEAR:'), year)
print('{:>20}'.format('MONTH:'), month)
print('{:>20}'.format('REPUBLICATION TITLE:'), pubtitle)
print('{:>20}'.format('VOLUME:'), volume)
print('{:>20}'.format('ISSUE:'), issue)
print('{:>20}'.format('PAGES:'),pages)
print('{:>20}'.format('PUBLISHER:'), publisher)
print('{:>20}'.format('ADDRESS:'), addr)
print('--------------------------------------------------------')

