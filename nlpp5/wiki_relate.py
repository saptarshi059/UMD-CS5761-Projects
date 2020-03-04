'''
Program Name: wiki_relate.py
Author: SAPTARSHI SENGUPTA
Major: Computer Science / 1st Year / Graduate Student (MS) / University of Minnesota Duluth
Date: 11/21/18

Program Details: This program calculates the relatedness between two words by utilizing their wikipedia entries. It proposes a measure of relatedness which is based on the number of overlapping or 
				 common words in a window of the first N (as supplied by the user) terms of their respective wiki entries. It divides the number of common words found in both entries (in the window 
				 of size N) by N. This is the relatedness measure which is returned with an accuracy of 4 places of decimal. The program returns a self similarity (when both words entered
				 are the same) score of 1.0000. If it finds that either one of the words do not exist in wikipedia, it returns a score of -1.0000.

Code Usage: In order to use this program -
				* A user must have the Python programming language compiler installed.
				
				* The user should type the following command in either command prompt or linux shell i.e. 
				  				python wiki_relate.py

				* The user will be prompted to enter the value of N (number of window words) followed by the words for which they wish to measure the relatedness. The program runs until 
				  the user enters 'EXITNOW' for either of the two words. 

				* A snippet of the program in execution would look like this:
				
					//
					This is the wikipedia-based-relatedness program by Saptarshi Sengupta CS 5761.
					Input your value of N: 100

					You may run the program multiple times. In order to exit, type 'EXITNOW' for either one of the input words.

					Word1: india
					Word2: china 

					Overlaps = ['billion', 'china', 'world', 'area', 'country', 'people', 'political', 'asia', 'rd', 'first', 'bce', 'republic', 'emerged', 'largest', 'populous', 'east', 'based']

					relatedness: 0.2100

					Word1: exitnow
					Word2: adfjkask
					
					wiki_relate has ended.
					//

Program Algorithm: The program has the following underlying logic -
				 
				//PreProcessing			
	
				1. The content from each page is retrieved as a unicode string and converted to a normal lowercase string.
				2. All non-word characters such as punctuation were removed along with numbers and stop words.

				//Main Algorithm
				
				1. The program first performs all the preprocessing steps for both entry strings.
				2. It then splits each string into a list of tokens.
				3. The number of overlapping words are calculated (in the window of size N) between each list.
				4. The result from step 3 is divided by N.
				5. The result from step 4 is then rounded up to 4 places of decimal which is finally returned as the output.

				A. If either word does not exist in wikipedia, a score of -1.0000 is returned.
				B. If both words are the same, a score of 1.0000 is returned.
'''
from __future__ import division
from nltk.corpus import stopwords
import nltk #This module was used to remove stop words from the wikipedia entries.
import re
import wikipedia #This module provides an implementation of the MediaWiki API.

stop_words = set(stopwords.words('english'))

def calc_relatedness(w1,w2):
	
	#Checking to see if the pages for the given words exist or not.
	try:
		s = wikipedia.summary(w1)
		w1_exists = True
	except wikipedia.exceptions.PageError:
		w1_exists = False

	try:
		s = wikipedia.summary(w2)
		w2_exists = True
	except wikipedia.exceptions.PageError:
		w2_exists = False

	#If either word does not have a wikipedia entry, -1 is returned as the similarity score. 
	if (w1_exists == False) or (w2_exists == False):
		print "\nOverlaps =",[]
		return -1
	else:
		#Accessing the pages for the 2 words.
		w1_page = wikipedia.page(w1)
		w2_page = wikipedia.page(w2)

		#Retreiving the content from the pages of the words and converting them from unicode to a normal lower case string.
		w1_content = w1_page.content.encode('utf-8').lower()
		w2_content = w2_page.content.encode('utf-8').lower()

		#Filtering out stop words, punctuations and numbers.
		w1_content = re.sub(r'\W|\d', ' ',w1_content)
		w2_content = re.sub(r'\W|\d', ' ',w2_content)

		w1_content_filtered = []
		w2_content_filtered = []

		for term in w1_content.split():
			if term not in stop_words:
				w1_content_filtered.append(term)

		for term in w2_content.split():
			if term not in stop_words:
				w2_content_filtered.append(term)

		#Taking the first N words from each entry.
		w1_n = w1_content_filtered[0:n]
		w2_n = w2_content_filtered[0:n]

		#Finding the common words in the window of the first N words.
		overlapping_words = []
		for w in w1_n:
			if w in w2_n:
				overlapping_words.append(w)

		#Calculating relatedness.
		rel = len(overlapping_words)/n

		#Not printing repeated words fron the list above.
		print "\nOverlaps =",list(set(overlapping_words))
		return rel

print "This is the wikipedia-based-relatedness program by Saptarshi Sengupta CS 5761."

print "Input your value of N:",
n = int(raw_input())

print "\nYou may run the program multiple times. In order to exit, type 'EXITNOW' for either one of the input words.\n"

while True:
	word1 = raw_input('Word1: ')
	word2 = raw_input('Word2: ')
	if (word1.upper() != 'EXITNOW') and (word2.upper() != 'EXITNOW'):
		rel_measure = calc_relatedness(word1,word2)
		print "\nrelatedness:",
		print "%.4f" % round(rel_measure,4) #Displaying the relatedness measure with 4 decimal place precision.
		print
	else:
		break

print "\nwiki_relate has ended."