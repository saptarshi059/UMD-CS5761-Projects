'''
Program Name: related_words.py
Author: SAPTARSHI SENGUPTA
Major: Computer Science / 1st Year / Graduate Student (MS) / University of Minnesota Duluth
Date: 11/08/18

Program Details: This program attempts to model distributional similarity. Using the notion of context vectors and cooccurences, 
				 such a model is formalized. When a word is supplied to the program, it returns the top N words which are similar to 
				 it based on distributional semantics i.e. it returns those words which occur in similar contexts as the given word.

Code Usage: In order to use this program -
				* A user must have the Python programming language compiler installed.
				
				* The user should type the following command in either command prompt or linux shell i.e. 
				  				python related_words.py <WORD> <CORPUS>
				 
			    In the above prompt, 

				* <WORD> is the input word we want related words for.

				* <CORPUS> is the name of the corpus file we want to train the model on.

				* Example Usage: python related_words.py friend corpus.txt
				  Example Output: good 30 0.65
				  				  bad  10 0.4
				  				  and so on
				
				  The output fields can be interpreted as follows: related word, number of times it occured in the corpus, its 
				  similarity with the given word.

Program Algorithm: The program has the following underlying logic -
				> Using the input word supplied, its location(s) in the corpus are found.
					
				> Window / surrounding words for the input word are extracted in both the right and left directions, starting
				  from the given index, till a sentence boundary ('.') is met. Let us assume that this list of words is called the 
				  master list. These words are extracted starting from each location as calculated above. 
					
				> For each term in the vocabulary, the program computes how many times the words from the master list appear in their
				  surrounding contexts, for each of their occurence in the corpus.

				> Thus, a count or context vector gets generated for each term.

				> Cosine Similarities between these vectors and the vector for the input word are computed.

				> The top N (here N = 20) words are printed out in decreasing order of similarity.			 
'''
from __future__ import division
from collections import Counter
import re
import sys
import math
import string

def gen_cv_terms(word,index):
	#For preventing sentence boundary crossovers.
	flag_right = 0
	flag_left = 0
	
	#This was an alternate path explored so as to improve code efficiency.
	#window_size = 5 #Number of words to be explored left and right of the target/vocabulary word. 

	index_of_word = index

	context_vector_terms = [] #The terms which surround word.
	j = 1 #Distance of the term from the center word / 'word'.

	#Generating the terms in the context window for word.
	while (flag_right != 1) or (flag_left != 1):
		
		#The outer if conditions are checking for index out of bounds errors
		if (index_of_word+j) <= len(corpus_tokenized) - 1:

			if corpus_tokenized[index_of_word+j] == '.':
				flag_right = 1

			if flag_right != 1:
				context_vector_terms.append(corpus_tokenized[index_of_word+j])

		if (index_of_word-j) <= len(corpus_tokenized) - 1:

			if corpus_tokenized[index_of_word-j] == '.':
				flag_left = 1

			if flag_left != 1:
				context_vector_terms.append(corpus_tokenized[index_of_word-j])

		j = j + 1

	return context_vector_terms

def gen_cv():

	for word in vocabulary.keys():
		indices = [i for i, x in enumerate(corpus_tokenized) if x == word] #Locations where word occurs.
		cv = {}

		for term in cv_ipword_terms:
			cv[term] = 0 #Initializing each term in the context vector to 0.

		temp = []

		for i in indices:
			temp = gen_cv_terms(corpus_tokenized[i],i) #Generating the surrounding terms for the word at that index.
			for j in temp:
				if j in cv_ipword_terms:
					cv[j] = cv[j] + 1

		cv_vocab[word]=cv	

def cosine_sim(v1,v2):

	v1_len = 0
	v2_len = 0
	dot_product = 0

	for i in v1.keys():
		v1_len = v1_len + pow(v1[i],2)

	for i in v2.keys():
		v2_len = v2_len + pow(v2[i],2)

	for i in v1.keys():
		if i in v2.keys():
			dot_product = dot_product + v1[i]*v2[i]

	similarity = dot_product / (v1_len * v2_len)

	return similarity

ipword = sys.argv[1] #This is the word whose similar words are required.
corpus_file = open(sys.argv[2],'r') #This is the corpus file object which has been read in.
corpus = ''

for line in corpus_file:
	corpus = corpus + line.lower()

corpus_file.close()

corpus_tokenized = re.findall(r"[\w]+|[\.\!\?\:\,\;\"\(\)\#\$\%\^\&\*\-\_\/\\\@\']", corpus) #Tokenizing the corpus.
vocabulary = Counter(corpus_tokenized)

#Cleaning up the Vocabulary of the corpus.
for word in vocabulary.keys():
	#Trimming the vocabulary. If the frequency of the word in the corpus is less than 5, it gets removed from the vocabulary.
	if corpus_tokenized.count(word) < 5:
		del vocabulary[word]
	
	#Deleting numbers from the vocabulary
	if word.isdigit() == True:
		del vocabulary[word]

	#Deleting all punctuation from vocabulary
	if word in string.punctuation:
		del vocabulary[word]

indices = [i for i, x in enumerate(corpus_tokenized) if x == ipword] #Locations where the input word occurs.
cv_ipword_terms1 = []
cv_ipword_terms = [] #This list holds the window words of the input word, for each location / index it occurs in.

for index in indices:
	cv_ipword_terms1.append(gen_cv_terms(ipword,index))

for i in cv_ipword_terms1:
	cv_ipword_terms = cv_ipword_terms + i

cv_vocab = {} #This will be a list of context vectors for each word in the vocabulary.
cosine_similiarities = [] #This is the list which holds the cosine similarities between each word and ipword.

gen_cv() #Generating context vectors for each word in the vocabulary.

#This is done to delete those entries in the context vector of a word which occur 0 times in the corpus with respect to the input 
#words context vector i.e. those words from cv_ipwords_terms which are not present in the surroundings of a vocabulary word are 
#deleted from its context vector. This is done to improve the system performance.
for word in cv_vocab.keys():
	for i in cv_vocab[word].keys():
		if cv_vocab[word][i] == 0:
			del cv_vocab[word][i]

#This is done to delete the vector of those words for which no term from cv_ipwords_terms occur in their surrounding contexts.
for word in cv_vocab.keys():
	if len(cv_vocab[word]) == 0:
		del cv_vocab[word]

for word in cv_vocab.keys():
	cosine_similiarities.append((word,cosine_sim(cv_vocab[word],cv_vocab[ipword])))

#Sorting the list of cosine similarity values in descending order.
cosine_similiarities.sort(key=lambda x:x[1], reverse = True)

#Displaying the result.
for i in range(20):
	print cosine_similiarities[i][0], corpus_tokenized.count(cosine_similiarities[i][0]) ,cosine_similiarities[i][1]