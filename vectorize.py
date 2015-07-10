import sys
import numpy

a = open('chorales.lisp', 'r')

#parse the input as vectors and store vectors

def obtainNum(elemSt):
    a = elemSt.split(" ")
    return int(a[1])

bookOfLists = []

for i in range(130):
    counter = 0
    gun = a.readline()
    if (len(gun) <= 1): #for /n accommodation
        continue
    else:
        while (gun[counter:(counter+2)] != "(("):
            counter += 1
        tribo = gun[(counter+2):(len(gun)-4)]
        stringArr = tribo.split("))((") #separates each vector into an element
        lister = [x.split(") (") for x in stringArr]
#        lister = map(lambda x : x.split(") ("), stringArr) #each vector becomes
        #a list of component elements so lister is a list of lists
        lister2 = [[obtainNum(each) for each in x] for x in lister]
#        lister2 = map(lambda x : map(obtainNum, x), lister)
        bookOfLists.append(lister2)

#comment for git
#lister2 in each iteration is the time series data of the vectors
#bookOfLists is many time series datasets put together

def classify(note):
    classified_note = [0,0,0,0,0]
    classified_note[0] = (note[1]-60)//4
    classified_note[1] = (note[2]-1)//4
    classified_note[2] = (note[3]+4)//3
    classified_note[3] = (note[4]-12)//4
    classified_note[4] = (note[5])
    return classified_note
#self-explanatory changing of 6 list note to 5 list classification

bookOfClasses = []
#map of classify to bookOfLists
universal_states = []
#list of dictionaries of bookOfClasses and its count per line
global_sum_states = {}
#dictionary of total counts of universal_states keys across all lines

for line in bookOfLists:
    states = {}
    rifle = []
    for note in line:
        classified_note = classify(note)
        if str(classified_note) not in states:
            states[str(classified_note)] = 1
            global_sum_states[str(classified_note)] = 1
        else:
            states[str(classified_note)] += 1
            global_sum_states[str(classified_note)] += 1
        rifle.append(classified_note)
    bookOfClasses.append(rifle)
    universal_states.append(states)
#panthi code to achieve the dicts and lists
