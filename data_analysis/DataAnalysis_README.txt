READ ME
========================================================================================================
In this code, I have performed analysis on Dataset taken from PSLC Datashop
I have performed this basic analysis with the help of Numpy and Pandas libraries.
The code contains intuitive comments which should facilitate easy understanding of the functionality performed.

DataSet:
Assistments Math 2004-2005 (912 Students) https://pslcdatashop.web.cmu.edu/DatasetInfo?datasetId=339
This dataset contains information about around 912 students. Every row contains one activity performed by a student. It may be a hint request or an attempt to answer. If the answer is correct, it goes to the next step otherwise it stays on the same step.

Tool used to analyze data: Spyder (Python 3.6): It is an open source, cross platform IDE which supports libraries like NumPy, SciPy, Matplotlib. It also has an embedded IPython console with it

Analysis:
By performing basic operations like sum, mean, min and max I got answers to following questions:
1.	How much time every student spent on a given problem(sum).
2.	How much time a given student spent on all problems in total(sum).
3.	How much time, on an average, a given student spent on one problem (average time).
4.	Who has solved a problem fastest (minimum time).
5.	Who needs to increase the speed (maximum time).
6.	Whose concepts are not clear and requires more learning (maximum attempts).
Also, more question that required complex commands were: 
7.	Is there any relation in between time a student spends and the attempt at step.
I found the correlation coefficient of them which was -0.047 or -4.7%. Negative value proves that as number of attempts increase, the time for solving the problem decreases.
8.	How many unique actions are performed.

Observations on the structure of the data:
There were some of the columns like duration, attempt at step, student response type and outcome which were relevant to what I wanted from the dataset. Remaining columns were either irrelevant or were empty. Hence, Data Preprocessing was necessary. I trimmed the data to columns that I needed. Also, few columns like duration and attempt at step were strings and hence needed to be converted to numeric to perform operations on them.

Challenges I encountered:
Even though I am new to Python, I am familiar with lots of programming languages like C, Java and SQL. This was a plus point for me as well as a challenge. I already know functions from other languages and hence I searched for similar features in Python. That required lots of researching as I was comparing this language to others, and I spent almost 80% time getting to know various commands and how they work, coding, debugging and had to make many corrections. But I believe that is how one learns a language. Instead of theoretical study, we learn it as we do it and implement it in practical. I learned more about python and probably next time will be able to do things faster. I overcame this challenge by giving more time than anyone else with an experience in python would have probably given.
