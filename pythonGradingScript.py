"""
Generate final grades for students
NJCU grading guidelines are here: https://www.njcu.edu/directories/offices-centers/registrar/grading-system
Take a weighted average of homeworks and exams, dropping the lowest N grades before averaging homework.
"""

import pandas as pd


gradeFile = "cs125_grades_2023.csv"
outputFile = "cs125_computed_final_grades_2023.csv"
numToDrop = 2
numExtraCredits = 1
totalToDrop = numToDrop + numExtraCredits
homeworkKey = "Homework" # homework columns have the word $homeworkKey in them
examKey = "Exam" # exam columns have the word $examKey in them
homeworkWeight = 0.6
examWeight = 0.4


dataframe = pd.read_csv(gradeFile)
dataframe["homeworkSubtotal"] = dataframe.filter(regex=homeworkKey).mean(axis=1).apply(lambda x : x * homeworkWeight)
dataframe.to_csv(outputFile)
