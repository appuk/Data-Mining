# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.model_selection import train_test_split
from id3 import Id3Estimator
from sklearn import preprocessing
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import roc_auc_score
from sklearn.metrics import average_precision_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestClassifier

'''-----------------------------------------DataPreProcessing--------------------------------------'''

data= pd.read_csv('AssignmentData.csv')
X=data[['SCHOOL','Class','STUDENTID','Gender','Activity','TRANSITIONS','NumACTIVITIES','FORMATchanges','NumFORMATS']]
#X_transformed stores all the numerical format of the training data as the classification algorithms cannot take string as input
X_transformed = X.copy()
Y=data['ONTASK']
for y in X.columns:
       if (X[y].dtype == object):
          le = preprocessing.LabelEncoder()
          le.fit(X[y].unique())
          X_transformed[y] = le.transform(X[y])
#Split the training data and labels in 70/30 train-test split
#stratify is used to do balanced random assignment according to the training label (ONTASK).
X_train,X_test,Y_train,Y_test=train_test_split(X_transformed,Y,test_size=0.3, stratify=Y) 
Y_test = Y_test.to_frame()
Y_test.columns = ['actualONTASK']

#-----------------------------------------Classification algorithm--------------------------------------


decisionTree = tree.DecisionTreeClassifier(max_depth=15, criterion='entropy')
decisionTree = decisionTree.fit(X_train,Y_train)
Y_test['usingDecisionTree'] = decisionTree.predict(X_test)

randomforest= RandomForestClassifier(max_depth=15, random_state=0, criterion='entropy')
randomforest = randomforest.fit(X_train,Y_train)
Y_test['usingRandomForest'] = randomforest.predict(X_test)

id3 = Id3Estimator()
id3 = id3.fit(X_train,Y_train)
Y_test['usingID3'] = id3.predict(X_test)


#-----------------------------------------K Fold Cross validation--------------------------------------

predict = cross_val_predict(decisionTree, X_train,Y_train, cv=10)
Y_test_KFold = np.array(list(predict))
Y_test_KFold=pd.DataFrame(np.array(Y_test_KFold).ravel(),columns=['using DecisionTree and KFold'])

predict = cross_val_predict(randomforest, X_train,Y_train, cv=10)
Y_test_KFold['using Random Forest and KFold'] = np.array(list(predict))

predict = cross_val_predict(id3, X_train,Y_train, cv=10)
Y_test_KFold['using Id3Estimator and KFold'] = np.array(list(predict))

Y_test_KFold = Y_test_KFold[11091:]

#-----------------------------------------Data Transformation--------------------------------------
#Y_transformed stores all the numerical format of the training labels for the purpose of performance evaluation

Y_test_transformed = Y_test.copy()
for y in Y_test.columns:
    le = preprocessing.LabelEncoder()
    le.fit(Y_test[y].unique())
    Y_test_transformed[y] = le.transform(Y_test[y])
    
Y_test_KFold_transformed = Y_test_KFold.copy()
for y in Y_test_KFold.columns:
    le = preprocessing.LabelEncoder()
    le.fit(Y_test_KFold[y].unique())
    Y_test_KFold_transformed[y] = le.transform(Y_test_KFold[y])

#-----------------------------------------Performance evaluation--------------------------------------
performance=pd.DataFrame(columns=['DecisionTree','DecisionTreeandK','RandomForest','RandomForestandK','ID3','ID3andK'],index=['roc','average precision','kappa','root mean square error','true negative', 'false positive','false negative','true positive'])
perform = np.zeros(8)
perform[0] = roc_auc_score(Y_test_transformed['actualONTASK'], Y_test_transformed['usingDecisionTree'])
perform[1] = average_precision_score(Y_test_transformed['actualONTASK'], Y_test_transformed['usingDecisionTree'])
perform[2] = cohen_kappa_score(Y_test_transformed['actualONTASK'], Y_test_transformed['usingDecisionTree'])
perform[3] = mean_squared_error(Y_test_transformed['actualONTASK'], Y_test_transformed['usingDecisionTree'])
perform[4],perform[5],perform[6],perform[7] = confusion_matrix(Y_test_transformed['actualONTASK'], Y_test_transformed['usingDecisionTree']).ravel()
performance['DecisionTree'] = perform



perform[0] = roc_auc_score(Y_test_transformed['actualONTASK'], Y_test_transformed['usingRandomForest'])
perform[1] = average_precision_score(Y_test_transformed['actualONTASK'], Y_test_transformed['usingRandomForest'])
perform[2] = cohen_kappa_score(Y_test_transformed['actualONTASK'], Y_test_transformed['usingRandomForest'])
perform[3] = mean_squared_error(Y_test_transformed['actualONTASK'], Y_test_transformed['usingRandomForest'])
perform[4],perform[5],perform[6],perform[7] = confusion_matrix(Y_test_transformed['actualONTASK'], Y_test_transformed['usingRandomForest']).ravel()
performance['RandomForest'] = perform



perform[0] = roc_auc_score(Y_test_transformed['actualONTASK'], Y_test_transformed['usingID3'])
perform[1] = average_precision_score(Y_test_transformed['actualONTASK'], Y_test_transformed['usingID3'])
perform[2] = cohen_kappa_score(Y_test_transformed['actualONTASK'], Y_test_transformed['usingID3'])
perform[3] = mean_squared_error(Y_test_transformed['actualONTASK'], Y_test_transformed['usingID3'])
perform[4],perform[5],perform[6],perform[7] = confusion_matrix(Y_test_transformed['actualONTASK'], Y_test_transformed['usingID3']).ravel()
performance['ID3'] = perform



perform[0] = roc_auc_score(Y_test_transformed['actualONTASK'], Y_test_KFold_transformed['using DecisionTree and KFold'])
perform[1] = average_precision_score(Y_test_transformed['actualONTASK'], Y_test_KFold_transformed['using DecisionTree and KFold'])
perform[2] = cohen_kappa_score(Y_test_transformed['actualONTASK'], Y_test_KFold_transformed['using DecisionTree and KFold'])
perform[3] = mean_squared_error(Y_test_transformed['actualONTASK'], Y_test_KFold_transformed['using DecisionTree and KFold'])
perform[4],perform[5],perform[6],perform[7] = confusion_matrix(Y_test_transformed['actualONTASK'], Y_test_KFold_transformed['using DecisionTree and KFold']).ravel()
performance['DecisionTreeandK'] = perform



perform[0] = roc_auc_score(Y_test_transformed['actualONTASK'], Y_test_KFold_transformed['using Random Forest and KFold'])
perform[1] = average_precision_score(Y_test_transformed['actualONTASK'], Y_test_KFold_transformed['using Random Forest and KFold'])
perform[2] = cohen_kappa_score(Y_test_transformed['actualONTASK'], Y_test_KFold_transformed['using Random Forest and KFold'])
perform[3] = mean_squared_error(Y_test_transformed['actualONTASK'], Y_test_KFold_transformed['using Random Forest and KFold'])
perform[4],perform[5],perform[6],perform[7] = confusion_matrix(Y_test_transformed['actualONTASK'], Y_test_KFold_transformed['using Random Forest and KFold']).ravel()
performance['RandomForestandK'] = perform



perform[0] = roc_auc_score(Y_test_transformed['actualONTASK'], Y_test_KFold_transformed['using Id3Estimator and KFold'])
perform[1] = average_precision_score(Y_test_transformed['actualONTASK'], Y_test_KFold_transformed['using Id3Estimator and KFold'])
perform[2] = cohen_kappa_score(Y_test_transformed['actualONTASK'], Y_test_KFold_transformed['using Id3Estimator and KFold'])
perform[3] = mean_squared_error(Y_test_transformed['actualONTASK'], Y_test_KFold_transformed['using Id3Estimator and KFold'])
perform[4],perform[5],perform[6],perform[7] = confusion_matrix(Y_test_transformed['actualONTASK'], Y_test_KFold_transformed['using Id3Estimator and KFold']).ravel()
performance['ID3andK'] = perform

print(performance)