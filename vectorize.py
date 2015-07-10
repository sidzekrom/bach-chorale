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
transitionMatrix = {}
#we are assuming that the same HMM is generating all the chorales

def getindex(note):
    return ((((note[0] * 4 + note[1]) * 3 + note[2]) * 2 + note[3]) * 2)\
     + note[4]

for line in bookOfLists:
    states = {}
    rifle = []
    prev = []
    index = 0
    for note in line:
        classified_note = classify(note)
        if getindex(classified_note) not in states:
            states[getindex(classified_note)] = 1
            global_sum_states[getindex(classified_note)] = 1
        else:
            states[getindex(classified_note)] += 1
            global_sum_states[getindex(classified_note)] += 1
        rifle.append(classified_note)
        if ((str(prev + classified_note) not in transitionMatrix)\
        and index != 0):
            transitionMatrix[str(prev + classified_note)] = 1
        elif(index != 0):
            transitionMatrix[str(prev + classified_note)] += 1
        prev = classified_note
        index += 1
    bookOfClasses.append(rifle)
    universal_states.append(states)
#panthi code to achieve the dicts and lists
