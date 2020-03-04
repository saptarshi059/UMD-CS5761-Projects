'''
Program Name: decision-list-test.py
Author: SAPTARSHI SENGUPTA
Major: Computer Science / 1st Year / Graduate Student (MS) / University of Minnesota Duluth
Date: 10/23/18

Program Details: This program is the 2nd in the series of 3 programs written to predict the sentiment of a movie review file. This program uses the supplied decision list
				 to make predictions about a movie review i.e. classifying it as either positive or negative review. This is essentially thus, the "testing" phase of the
				 entire process.

Code Usage: In order to use this program -
				* A user must have the Python programming language compiler installed.
				
				* The user should type the following command in either command prompt or linux shell i.e. 
				  				python decision-list-test.py "decision-list-file.txt" "test-data-file.txt" > "output-predictions.txt"
				 
			    In the above prompt, 

				* "decision-list-file.txt" is the name of our file containing the decision list obtained using the "decision-list-train.py" program.
				  We used the file "sentiment-decision-list.txt" obtained from the first program.

				* "test-data-file.txt" is the name of the test data file containing the reviews whose sentiment is needed to be predicted. The test data is a 
				  small set of 200 review files. The name of our file was "sentiment-train.txt".

				* "output-predictions.txt" is the file which will contain the list of predictions made by our classifier. We named our file 
				  "sentiment-system-answers.txt".
				
				* In order to use this program, the "decision-list-file.txt" must be formatted such that each entry is represented as a tuple of the form, 
				  (<feature>, <log-likelihood ratio>, <class>)

				* The output of the program is written to "output-predictions.txt" using the ">" operator.
				 

Program Algorithm: The program has the following underlying logic -
				 
				 The decision list is applied to each review in the test data, starting with the highest or topmost or "most likely" entry. A check is made to see whether that
				 entry (feature) is present in the review or not. If it is, then the review is assigned the class associated with that feature and the next review is checked.
				 If the feature is not present in the file, the remaining features are checked for presence stopping at the first one which is present. If none of the 
				 features are present, then the reveiw is assigned a default class (either 0/1). Default class has been taken to be 0 here.
'''
import sys
testing_data = open (sys.argv[2] , 'r')

decision_list = []
test_data = []
predictions = []

with open(sys.argv[1]) as f:
    content = f.readlines()
content = [x.strip() for x in content] #removing new line characters.

for i in content:
	decision_list.append(eval(i)) #Eval is a function which converts a string to a tuple provided the string has ',' to indicate tuple entry boundaries. 
								  #It is used to to obtain the decision list entries as a tuple.

for line in testing_data:
		test_data.append(line.split())

for review in test_data:
	flag = 0
	
	for feature in decision_list: 
		if feature[0] in review:
			predictions.append( (review[0], feature[2]) ) #If the feature is present in the given review file, 
														  #assign the review the sentiment class correspondign to the feature. 
			flag = 1
			break

	if flag == 0:
		predictions.append( (review[0], 0) ) #Assigining default class to the review after examining 
											 #all the features in the decision list.

for result in predictions:
	print result