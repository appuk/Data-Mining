# -*- coding: utf-8 -*-
import pandas as pd

"""-----------------------------------------DataExtraction--------------------------------------
Reading the Dataset and storing it in DataFrame"""
data= pd.read_csv('Dataset.csv')

"""-----------------------------------------Training the BKT Model on Per-KC basis--------------------------------------
the below steps calculate the probability that he already knew a skill before that step and probability that he will perform a correct action"""
p_G = 0.3 #the probability that student didnt learn the skill but guessed the answer
p_S = 0.1 #the probability that student learned the skill but slipped it
data['p_KC1']=BKT(data,'KC_1')
data['c_KC1'] =  data['p_KC1'].apply(lambda x: (x*(1-p_S)) + ((1-x)*p_G )) # this column contains the probability that student will perform a correct action
data['p_KC27']=BKT(data,'KC_27')
data['c_KC27'] =  data['p_KC27'].apply(lambda x: (x*(1-p_S)) + ((1-x)*p_G ))
data['p_KC24']=BKT(data,'KC_24')
data['c_KC24'] =  data['p_KC24'].apply(lambda x: (x*(1-p_S)) + ((1-x)*p_G ))
data['p_KC14']=BKT(data,'KC_14')
data['c_KC14'] =  data['p_KC14'].apply(lambda x: (x*(1-p_S)) + ((1-x)*p_G ))
data['p_KC22']=BKT(data,'KC_22')
data['c_KC22'] =  data['p_KC22'].apply(lambda x: (x*(1-p_S)) + ((1-x)*p_G ))
data['p_KC20']=BKT(data,'KC_20')
data['c_KC20'] =  data['p_KC20'].apply(lambda x: (x*(1-p_S)) + ((1-x)*p_G ))
data['p_KC21']=BKT(data,'KC_21')
data['c_KC21'] =  data['p_KC21'].apply(lambda x: (x*(1-p_S)) + ((1-x)*p_G ))

'''
-----------------------------------------Design of a Multi-Expert Model for multi-KC step--------------------------------------'''
data['c_multiKC'] = MultiExpertModel(data)
print(data)