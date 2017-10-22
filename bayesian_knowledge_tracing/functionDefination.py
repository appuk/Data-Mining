import pandas as pd
import numpy as np

"""-----------------------------------------Function implementing the BKT Model--------------------------------------"""
def BKT(data,kc):
    """Declaring variables"""
    p_L = [0.5,] # array storing P(L0) and temperory storage of P(L1) P(L2) for calculating the probability
    p_L_n = [0,] # the probability that a particular student already knew the skill before the current question
    p_Lnminus1 = [0,] # array storing P(ln-1)
    p_T = 0.7 #the probability that the student transitioned from not learning to learning the skill
    p_G = 0.3 #the probability that student didnt learn the skill but guessed the answer
    p_S = 0.1 #the probability that student learned the skill but slipped it
    probability=[0,] # the probability of all student that they already knew the skill before the current question
    n=1
    m=1
    students = data[['Student']][data[kc]==1].reset_index().drop(['index'],axis=1)
    currentStudent = students['Student'][0]
    for x in range(0 ,len(data)):
        if data[kc][x]==1:
            if data['Student'][x] != currentStudent: # if new student, reset all the value
                p_L = [0.5,]
                p_L_n = [0,]
                p_Lnminus1 = [0,]
                n=1
                currentStudent = data['Student'][x] # set the new student as current student
            if data['Correct'][x]==1: # If correct
                p_Lnminus1.append((p_L[n-1] * (1-p_S))/((p_L[n-1] * (1-p_S)) + ((1 - p_L[n-1]) * p_G)))
            else : # If Incorrect
                p_Lnminus1.append((p_L[n-1] * p_S)/((p_L[n-1] * p_S) + ((1 - p_L[n-1]) * (1- p_G))))
            p_L_n.append(p_Lnminus1[n] + ((1 - p_Lnminus1[n]) * p_T))
            probability.append(p_Lnminus1[n] + ((1 - p_Lnminus1[n]) * p_T))
            p_L.append(p_Lnminus1[n]) #for accessing P(Ln-1)
            n+=1
        else:
            probability.append(np.nan) #KC is not equal to 1, hence probability will be invalid here
        m+=1 
    return probability[1:]

"""-----------------------------------------Function implementing the Multi Expert Model--------------------------------------"""
def MultiExpertModel(data):
    correctnessOfKC=data[['Student','StepID','c_KC1','c_KC27','c_KC24','c_KC14','c_KC22','c_KC20','c_KC21']]
    correctnessOfKC= correctnessOfKC.fillna(1) # fill al na values with 1 to not generate an error while multiplying the values.
    correctnessOfKC['c_multiKC']=correctnessOfKC['c_KC1']*correctnessOfKC['c_KC27']*correctnessOfKC['c_KC24']*correctnessOfKC['c_KC14']*correctnessOfKC['c_KC22']*correctnessOfKC['c_KC20']*correctnessOfKC['c_KC21']
    return correctnessOfKC['c_multiKC']