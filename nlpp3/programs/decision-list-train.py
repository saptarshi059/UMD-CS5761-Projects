'''
Program Name: decision-list-train.py
Author: SAPTARSHI SENGUPTA
Major: Computer Science / 1st Year / Graduate Student (MS) / University of Minnesota Duluth
Date: 10/23/18

Program Details: This program is the starting point in a series of 3 programs used to predict the sentiment class of a movie review.
				 For performing this task, the program makes use of an idea called decision lists which is computed using the
				 Log Likelihood Ratio of the selected features. This program is used to generate the decision list 
				 (training our classifier).

Code Usage: In order to use this program -
				* A user must have the Python programming language compiler installed.
				
				* The user should type the following command in either command prompt or linux shell i.e. 
				  				python decision-list-train.py "training_file_name.txt" > "generated_decision_list.txt"
				 
			    In the above prompt, 

				* "training_file_name.txt" is the name of movie reviews file which will be used to train the classifier. Note that,
				   the file must be formatted in such a way that each line represents a review with the first field indicating the
				   name of the review file followed by its sentiment class (0 for negative review & 1 for positive). For the purposes
				   of this program, we used a file called "sentiment-train.txt" which contained a subset of movie reviews from the 
				   dataset used by Pang, Lee and Vaithyanathan [http://www.aclweb.org/anthology/W02-1011].

				* "generated_decision_list.txt" is the name of the file to which the created decision list will be written to. For
				   our implementation, we created a file called "sentiment-decision-list.txt"

				* This program generates the decision list to be used for classification and writes the list to an output
				   text file which is performed using the ">" operator.
				

Program Algorithm: This program has the following underlying logic -
				  A decision list entry for a feature for this task is created by using the following formula:

				 			abs( log( P(positive_reviews|feature)/P(negative_reviews|feature) ) , 

				 		where P(positive_reviews|feature) gives the count of positive sentiment files having the given feature 
				 		divided by the total number of files containing that feature. Similar logic applies to the negative 
				 		sentiment probability calculation. The denominator being the same for both these probabilities gets cancelled
				 		out and what remains is simply the count of the number of positive sentiment files having the given feature
				 		divided by the number of negative sentiment files having the given feature.

				 Using the given formula, the entire list is populated for the selected set of features. For the purposes of this 
				 implementation, only unigram and bigram features have been used. 9 bigram features have been used and 19 unigram
				 features were used. These features were selected using a combination of intuition and studying of the training 
				 data. It should be noted that, log base 10 has been used in the calculations.

				 The list so obtained, is sorted in descending order of log-likelihood.
'''
from __future__ import division
from collections import Counter
import operator
import math
import sys

def create_training_list():
	training_data = open(sys.argv[1] , "r")
	for line in training_data:
		train_data.append(line.split())

#This function computes the entire decision list for the set of features
def prob(feature):
	pos_count = 0
	neg_count = 0
	global i

	#At first, the ratios for the positive features get calculated followed by the bigrams.
	if i < u:

		for review in train_data:

			if review[1] == '1' and (feature[0] in review):
				pos_count = pos_count + 1
			
			if review[1] == '0' and (feature[0] in review):
				neg_count = neg_count + 1

	else:

		for review in train_data:
			temp = ' '.join(review[2:]) #The entire review was reconsrtucted as a string in order to match bigrams. The counting 
										#was started from the 2nd element because the first 2 
										#are the review names and their sentiment class.
			
			if review[1] == '1' and (feature[0] in temp):
				pos_count = pos_count + 1

			if review[1] == '0' and (feature[0] in temp):
				neg_count = neg_count + 1

	LLR = abs( math.log10(pos_count / neg_count) )
	decision_list.append( (feature[0], LLR , feature[1]) )
	i = i + 1

features = [('!',0), ('?',0) , ('.',1), ('poor',0) ,('love' , 1), ('brilliant',1), ('kick',1) ,('remarkable', 1) ,('wonderful' , 1) , ('super', 1), ('still', 1), ('beautiful', 1), ('bad', 0), 
		('worst', 0), ('awful',0), ('painfully',0), ('kill',0) ,('dull',0) ,('disappoint',0) ,('very good', 1), ('not even',0), ('fast forward',0), ('must see',1), ('love it',1), ('so bad',0)
		,('waste of',0), ('my god',1), ('believe me',0)]

train_data = []
decision_list = []
create_training_list()
i = 0
u = len(features) - 9 #Total number of features - number of bigram features = number of unigram features.
for f in features:
	prob(f)

decision_list.sort(key = lambda x:x[1] , reverse = True) #Sorting the decision list.

for i in decision_list:
	print i