'''
Program Name: decision-list-eval.py
Author: SAPTARSHI SENGUPTA
Major: Computer Science / 1st Year / Graduate Student (MS) / University of Minnesota Duluth
Date: 10/23/18

Program Details: This is the final program in the series of the 3 programs used to predict the sentiment of a movie review. This 
				 program displays the accuracy of classification and generates important information related to classification 
				 such as the confusion matrix and the precision (P), recall (R) and F1 statistics for both classes.

Code Usage: In order to use this program -
				* A user must have the Python programming language compiler installed.
				
				* The user should type the following command in either command prompt or linux shell i.e. 
				  				python decision-list-eval.py "gold-standard.txt" "system-predictions.txt"
				 
			    In the above prompt, 

				* "gold-standard.txt" is the name of file which has the "correct" class of the test data. For our implementation,
				  we use a file called "sentiment-gold.txt"

				* "system-predictions.txt" is the file which has the predictions of the decision-list classifier. It is obtained from
				  the previous program ("sentiment-system-answers.txt").

				* All outputs are displayed via STDOUT.

Program Algorithm: The program has the following underlying logic -
				 Using the system predicitions that it has been supplied with, the program simply calculates how many files 
				 were assigned the correct sentiment class and displays this as a percentage out of 200 (total number of review
				 files). Finally, the confusion matrix (each cell described below) is created and the P, R and F1 measures for
				 both positive and negative sentiment classes are calculated. 
				 
'''
from __future__ import division
import sys
import math

gold_standard = []
predicted_answers = []

content = open (sys.argv[1] , 'r')
for i in content:
	gold_standard.append(i.split())

with open(sys.argv[2]) as f:
    content = f.readlines()
content = [x.strip() for x in content]

for i in content:
	predicted_answers.append(eval(i))

correctly_classified = 0

for i in range(200):
	if predicted_answers[i][1] == int(gold_standard[i][1]):
		correctly_classified = correctly_classified + 1

print "Classification Accuracy = ", (correctly_classified / 200) * 100 , "%\n"

#Confusion Matirix (CM) Calculation
#Confusion Matrix for the classifier. It is a 2x2 matrix. The first list indicates the first row and 
#the 2nd list, the 2nd row. Each cell has a certain meaning.
#Cell [0][0] - How many negative reviews did the system correctly classify as class 0 (negative). (TN) - True Negative.
#Cell [0][1] - How many negative reviews did the system incorrectly classify as class 1 (positive). (FN) - False Negative.
#Cell [1][0] - How many positive reviews did the system incorrectly classify as class 0 (negative). (FP) - False Positive.
#Cell [1][1] - How many positive reviews did the system correctly classify as class 1 (positive). (TP) - True Positive.

CM = [ [], [] ] 

#Calculations for negative reviews.

true_negative = 0
false_positive = 0

for i in range(200):
	if int(gold_standard[i][1]) == 0 and predicted_answers[i][1] == 0:
		true_negative = true_negative + 1
	elif int(gold_standard[i][1]) == 0 and predicted_answers[i][1] == 1:
		false_positive = false_positive + 1

#Calculations for positive reviews.

true_positive = 0
false_negative = 0

for i in range(200):
	if int(gold_standard[i][1]) == 1 and predicted_answers[i][1] == 1:
		true_positive = true_positive + 1
	elif int(gold_standard[i][1]) == 1 and predicted_answers[i][1] == 0:
		false_negative = false_negative + 1

#Adding the values to the CM

CM[0].append(true_negative)
CM[0].append(false_positive)
CM[1].append(false_negative)
CM[1].append(true_positive)

#Displaying the CM
print "Confusion Matirix:\n"

for i in range(2):
	for j in range(2):
		if i == 0 and j == 0:
			print " TN =",
		if i == 0 and j == 1:
			print " FN =",
		if i == 1 and j == 0:
			print " FP =",
		if i == 1 and j == 1:
			print " TP =",
		print CM[i][j],
	print "\n"

print "REFERENCE:\n"

print "TN = True Negative (How many negative reviews did the system correctly classify as negative)\n"
print "FN = False Negative (How many negative reviews did the system incorrectly classify as positive)\n"
print "FP = False Positive (How many positive reviews did the system incorrectly classify as negative)\n"
print "TP = True Positive (How many positive reviews did the system correctly classify as positive)\n"

#P, R and F calculations for CM

Precision_Negative = ( CM[0][0] / (CM[0][0] + CM[0][1]) ) * 100
Recall_Negative = ( CM[0][0] / (CM[0][0] + CM[1][0]) ) * 100
F1_Negative = (2 * Precision_Negative * Recall_Negative) / (Precision_Negative + Recall_Negative)

Precision_Positive = ( CM[1][1] / (CM[1][1] + CM[1][0]) ) * 100
Recall_Positive = ( CM[1][1] / (CM[1][1] + CM[0][1]) ) * 100
F1_Positive = (2 * Precision_Positive * Recall_Positive) / (Precision_Positive + Recall_Positive)

print "Precision_Negative = ", round(Precision_Negative , 2) , "%" , "\n"
print "Recall_Negative = ", round(Recall_Negative , 2) , "%" , "\n"
print "F1_Negative = ", round(F1_Negative , 2) , "%" , "\n"

print "Precision_Positive = ", round(Precision_Positive , 2) , "%" , "\n"
print "Recall_Positive = ", round(Recall_Positive , 2) , "%" , "\n"
print "F1_Positive = ", round(F1_Positive , 2) , "%" , "\n"