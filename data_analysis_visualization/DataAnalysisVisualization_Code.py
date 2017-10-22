import pandas as pd
import datetime as dt
pd.options.mode.chained_assignment = None

"""-----------------------------------------DataExtraction--------------------------------------
Reading an Andes log file from a dat file and storing it in DataFrame"""
data=pd.read_table('Assignment2_ApurvaBakshi_DataSet.dat', index_col=False, header = 4, sep = '\t',error_bad_lines=False, warn_bad_lines=False, engine='python')
data.columns=['time','action']

"""-----------------------------------------DataMunging--------------------------------------
Trimming the data to only store DDE and DDE-Post commands. """
trimData = data[data['action'].str.contains('DDE-POST|DDE\s', na=False)].reset_index().drop('index',1)

"""new Dataframe to store student information contained in "DDE (read-student-info "DAC2D" 1)"""
studentData =trimData[trimData['action'].str.contains('read-student-info|close-problem', na=False)] #stored close-problem as a flag to mark end of one student data

"""-----------------------------------------DataTransformation--------------------------------------
extracting student id from the commands for convinience by making a separate column"""
studentData['student']=studentData['action'].apply(lambda x:x.split('"')[1] if 'read-student-info' in x else x)

"""converting time column from string to datetime for performing operations"""
studentData['time']=studentData['time'].apply(lambda x:dt.datetime.strptime(x,'%M:%S') if x.count(':') is 1 else dt.datetime.strptime(x,'%H:%M:%S'))


"""-----------------------------------------DataAnalysis--------------------------------------
----------------------------------calculating time spent by each student"""
studentData['time'] = studentData['time'].shift(-1) - studentData['time'] #time difference in between read student info and close problem commands
studentData1 =studentData[~studentData['action'].str.contains('close-problem', na=False)] #removing the close problem commands as we dont need them
"""calculate total time by grouping with student"""
totalTimeOfStudent = studentData1.groupby(by = ['student']).sum().reset_index() #adding up all the time values to find total time
totalTimeOfStudent= totalTimeOfStudent.drop('action',1) #as we have extracted student info, we dont need the whole command
totalTimeOfStudent.columns=['student','time in mins'] #renaming the columns to be precise
"""converting the time format data into number of minutes"""
totalTimeOfStudent['time in mins']=totalTimeOfStudent['time in mins'].apply(lambda x:x.seconds/60)
print( "the total time spent for each student:")
print(totalTimeOfStudent)

"""------------------------------calculating actions performed per minute
by calculating difference in between indexes of read student info and close problem log, we can find out how many actions were taken in between"""
numberOfActions=pd.DataFrame(columns= ['actions','student'])
numberOfActions['actions'] = studentData.reset_index()['index'].diff().shift(-1).reset_index().drop(['level_0'],axis=1)
studentData = studentData.reset_index().drop(['index'],axis=1)
numberOfActions['student'] = studentData['student'].copy()
"""sum of number of actions performed by a student in all sessions"""
numberOfActions = numberOfActions.groupby(by = ['student']).sum().reset_index()
numberOfActions = numberOfActions[numberOfActions['student'].str.contains('S10NAMc', na=False)].reset_index().drop(['index'],axis=1) # eliminate close problem commands
actionsPerMinute=pd.DataFrame(columns= ['student','actions'])
actionsPerMinute['student'] = numberOfActions['student'].copy()
actionsPerMinute['actions'] = numberOfActions['actions']/totalTimeOfStudent['time in mins']
print("the number of actions performed per minute:")
print(actionsPerMinute)


"""-----------------------------------DataVisualization-------------------------------------
first install plotly : pip install plotly
"""
import plotly
import plotly.graph_objs as go

"""-----------------------------visualize the actions per minute"""
apm = go.Scatter(
        x = actionsPerMinute['student'],
        y = actionsPerMinute['actions'],
        name = 'Actions Per Minute',
        line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4,
        dash = 'dot')
        )
data1 = [apm]
""" Edit the layout"""
layout = dict(title = 'Student Actions Per Minute',
              xaxis = dict(title = 'Student ID'),
              yaxis = dict(title = 'Actions Per Minute'),
              )
fig = dict(data = data1, layout = layout)
plotly. offline. plot(fig, filename='actionsPerMinute.html')
"""-------------------------------visualization the total time"""
Ttim = go.Scatter(
        x = totalTimeOfStudent['student'],
        y = totalTimeOfStudent['time in mins'],
        name = 'Total Times in Minutes',
        line = dict(
               color = ('rgb(22, 96, 167)'),
               width = 4,
               dash = 'dot')
        )
data2= [Ttim]
layout = dict(title = 'Per Student Total Times in Minutes',
              xaxis = dict(title = 'Student ID'),
              yaxis = dict(title = 'Total Times in Minutes'),
              )
fig = dict(data = data2, layout = layout)
plotly. offline. plot(fig, filename='totalTimeOfStudent.html')