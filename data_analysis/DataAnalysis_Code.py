# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 15:17:18 2017

@author: Apurva Kulkarni
"""
import pandas as pd
import numpy as np

#-----------------------------------------DataExtraction--------------------------------------
#Reading dataset from a text file and storing it in DataFrame
data= pd.read_table('Assignment1_ApurvaBakshi_DataSet.txt', low_memory=False)

#-----------------------------------------DataPreProcessing--------------------------------------
#Trimming the columns to analyze on relevent data only
trimData = data[['Anon Student Id','Problem Name','Duration (sec)']].copy() 
trimData1 = data[['Anon Student Id','Problem Name','Duration (sec)','Attempt At Step']].copy()
trimData2 = data[['Anon Student Id','Student Response Type','Outcome']].copy()

#-----------------------------------------DataTransformation--------------------------------------
#Converting duration and attempt at step feilds to a number(float) for performing operations
columnTypes = data.dtypes
trimData['Duration (sec)'] = trimData['Duration (sec)'].apply(pd.to_numeric, errors='coerce')
trimData1['Duration (sec)'] = trimData1['Duration (sec)'].apply(pd.to_numeric, errors='coerce')
trimData1['Attempt At Step'] = trimData1['Attempt At Step'].apply(pd.to_numeric, errors='coerce')
#verifying the convertion
if ((trimData['Duration (sec)'].dtype != "float64") and (trimData1['Attempt At Step'].dtype != "float64")):
    print("error!!")

#-----------------------------------------DataAnalysis--------------------------------------
#1. total time every student spent on a given  problem
totalTimeOnAProblem = trimData.groupby(by = ['Anon Student Id','Problem Name']).sum().reset_index() #reset index used to put Anon Student Id & Problem Name in different columns
print("totalTimeOnAProblem:\n")
print(totalTimeOnAProblem)
#2. total time a given  student spent on all problems
totalTimeOfStudent = totalTimeOnAProblem.groupby(by = ['Anon Student Id']).sum().reset_index()
totalTimeOfStudent['Duration (hrs)'] = totalTimeOfStudent['Duration (sec)'] / (60*60) #in hours
totalTimeOfStudent['Duration (mins)'] = totalTimeOfStudent['Duration (sec)'] / (60) # in minutes
totalTimeOfStudent = totalTimeOfStudent[['Anon Student Id','Duration (sec)','Duration (mins)','Duration (hrs)']].copy()
print("totalTimeOfStudent:\n")
print(totalTimeOfStudent)
#3. average time a given  student spent on a problem
averageTimeOnAProblem = totalTimeOnAProblem.groupby(['Anon Student Id'])['Duration (sec)'].mean().reset_index()
print("averageTimeOnAProblem:\n")
print(averageTimeOnAProblem)
#4. a student who has solved a problem fastest(minimum time)
fastestStudent = totalTimeOnAProblem[totalTimeOnAProblem['Duration (sec)']==min(totalTimeOnAProblem['Duration (sec)'])]
print("fastestStudent:\n")
print(fastestStudent)
#5. a student who has solved a problem slowest(maximum time)
slowestStudent = totalTimeOnAProblem[totalTimeOnAProblem['Duration (sec)']==max(totalTimeOnAProblem['Duration (sec)'])]
print("slowestStudent:\n")
print(slowestStudent)
#6. a student who solved a problem in maximum attempts
maximumAttempts = data[['Anon Student Id','Problem Name','Attempt At Step','Is Last Attempt']][data['Attempt At Step']==max(data['Attempt At Step'])]
print("maximumAttempts:\n")
print(maximumAttempts)
#7. relation in between time student spends and the attempt at spent
reln = np.corrcoef(trimData1['Duration (sec)'],trimData1['Attempt At Step'])
print("coefficiant corelation:\n")
print(reln)
# 8.	How many unique actions are performed by every student
numberOfUniqueActions = trimData2.groupby(by = ['Anon Student Id','Student Response Type','Outcome'])['Anon Student Id'].count().reset_index(name="count")
print("numberOfUniqueActions:\n")
print(numberOfUniqueActions)