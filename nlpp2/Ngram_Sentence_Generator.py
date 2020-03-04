'''
Program Name: Ngram_Sentence_Generator
Author: SAPTARSHI SENGUPTA
Major: Computer Science / 1st Year / Graduate Student (MS) / University of Minnesota Duluth
Date: 10/04/18

Program Details: The Ngram_Sentence_Generator program has been written for generating random sentences based on an N-gram Language Model (LM) learned
				 from the set of supplied input text files. The program works for 3 settings i.e. it can generate sentences based on a unigram , bigram 
				 or trigram model. As the value of ngram changes i.e. as we move from unigrams to trigrams, the language model created becomes more and 
				 more sophisticated and the quality of sentences produced, in terms of coherent meaning, improves on the whole. The logic of the 
				 program for the bigram and trigram models was inspired by the Shannon Visualization Method.

Code Usage: In order to use this program -
				* A user must have the Python programming language compiler installed.
				
				* The user should type the following command in either command prompt or linux shell i.e. 
				  				python Ngram_Sentence_Generator.py m n <file names>
				 
			    In the above prompt, 

				* 'm' is the language model to be created. Limits of m = [1,3]. m = 1 indicates unigram , m = 2 indicates bigram 
				  and m = 3 means trigram.

				* 'n' indicates the number of sentences the user wants to generate.

				* '<file names>' is the list of files the user supplies to the program which are used for creating the LM. It would be desirable that the 
				  program file (.py) be kept in the folder where all the input files are. In this way, the user can avoid typing out the entire
				  path name for the files. However, if they so wish, they can enter the entire file paths as well.
				
				* An example input would be of the form - python Ngram_Sentence_Generator.py 1 5 f1.txt f2.txt
				 
				* What this command does is, output '5' (n = 1) random 'unigram' (m = 1) sentences based on the LM learned from the files 
				  f1.txt and f2.txt.

Program Algorithm: The program has the following underlying logic -
				 
				//PreProcessing			
	
				1. At first, all the input text files are parsed line by line into a list and all words are converted into lowercase.
				2. On each line in the above list, tokenization using regular expressions is performed so as to generate a final list of tokens.
				3. Finally, using this list of tokens, a dictionary of unique tokens i.e. word types was generated (vocabulary).

				//Unigram Sentence Generation Logic

				1. Probability for each unigram was calculated as the count of the unigram / total token count.
				2. A unigram was chosen at random from the vocabulary terms and generated in the resulting sentence.
				3. A random number was generated between 0 and 1. If this number was less than the probability of a '?' / '!' / '.' , the
				   respective stop word term would be added to the sentence and the sentence generation process would end.
				4. Else, unigrams would continue to get generated until the criteria for step 3 is met.

				//Bigram or Trigram Sentence Generation Logic

				1. A combined list of bigrams/trigrams was generated from the supplied input files using regular expressions.
				2. A bigram/trigram was chosen at random from the respective list of bigrams/trigrams.
				3. Using the 2nd/3rd word (called 'start_word') in the generated bigram/trigram , the next bi/trigram is selected using a 
				   probability calculation.
				4. A list of all bi/trigrams which has the 'start_word' as the first term, is generated.
				5. A list of probabilities for each bi/trigram from the above list (4) is calculated using the following formula:
						(number of occurences of the considered bi/trigram) / (total number of bi/trigrams generated).
				6. A random number is generated between the minimum and maximum probability values (5).
				7. A list containing the difference between the random number and each term of (5) is produced.
				8. The next bi/trigram is chosen such that the difference value (7) is minimum for it.
				9. In this way, the entire process starting from (3) is repeated unitl a '?' / '!' / '.' is encountered.

'''

from __future__ import division
from collections import Counter #This module was used to determine the word types and their corresponding frequencies from the list of unigrams produced.
import re #The regular expression module was used for preprocessing the text such as token generation.
import sys
import random #This was used for generating random numbers within a certian range.

def calculate_unigram_probabilities():
	j = 0
	for i in vocabluary.keys():
		uprobs[i] =  s3.count(i) / N
		j = j + 1

def generate_unigram_sentences():
	calculate_unigram_probabilities() #This was defined as a separate function because, it is not desirable that only during the generation 
									  #of unigram sentences, their (unigram) probabilities be calculated. For ex., when generating bigram sentences, 
									  #we only require the unigram probabilities and not the unigram sentences.
	current_word = " "
	boundary_terms=['.', '!', '?']

	prob_period = uprobs['.']
	prob_qmark = uprobs['?']
	prob_exmark = uprobs['!']

	for i in range(int(sys.argv[2])):

		final_sentence = ' '
		sent_words = []

		while (True):
			
			current_wordno = random.randint(0,V-1)
			current_word = vocabluary.keys()[current_wordno]
			sent_words.append(current_word)
			
			r = random.uniform(0,1)

			if r<=prob_qmark:
				sent_words.append('?')
				break

			if r<=prob_exmark:
				sent_words.append('!')
				break

			if r<=prob_period:	#This condition has been placed at the end as it was expected that the probability of '.' would be the highest.
									#Thus, in order to avoid only getting '.' as the stop word, it was placed here.
				sent_words.append('.')
				break

		final_sentence = ' '.join(sent_words)
		print i+1,':',final_sentence

def generate_bigrams():
	for i in range(len(s1)):
	
		p2 = r'(\w+)\s+(?=(\w+))|(\w+)(\.|\?|\:|\,|\;|\-|\_|\")' #This regular expression searches for words followed by words / punctuation marks.
		x = re.findall(p2,s1[i])

		p3 = r'(\?|\:|\.|\!|\,|\;|\-|\_|\")\s+(\w+)' #This regular expression searches for punctuation marks followed by words.
		y = re.findall(p3,s1[i])

		#This loop is used to delete all the '' matches from y and add them to the main bigram list.
		for j in y:
			if j[0]!='':
				x.append(j)

		#This loop is used for filtering out all the '' matches in x.
		for j in x:
			 temp = list(j)
			 if '' in temp:
			 	for k in range(temp.count('')):
			 		temp.remove('')
			 bigrams.append(temp)

def generate_bigram_sentences():

	generate_bigrams()

	for i in range(int(sys.argv[2])):
		
		b = []
		sent_words = [] #This list holds each bigram which was produced.
		boundary_terms = ['.' , '!' , '?']
		j = 0
		start_word = ''
		final_sentence = ''

		while start_word not in boundary_terms: 

			if sent_words == []:
				bigram_no = random.randint(0,len(bigrams))
				sent_words.append(bigrams[bigram_no])
				start_word = sent_words[j][1]
			else:
				start_word = sent_words[j][1]
				
				b = [item for item in bigrams if item[0] == start_word] #Searching for those bigrams whose first element is the current start_word.
				prob_for_each_bigram = []
				for k in b:
					prob_for_each_bigram.append( bigrams.count(k) / len(bigrams) ) #Probability of a bigram is defined as
																				   #number of occurences of the bigram / total number of bigrams.

				start_val = min(prob_for_each_bigram)
				end_val = max(prob_for_each_bigram)

				r = random.uniform(start_val , end_val)

				diff_list = []

				for k in prob_for_each_bigram:
					diff_list.append(abs(r-k))

				index_of_element_with_least_diff = diff_list.index( min(diff_list) )

				bigram = b[index_of_element_with_least_diff]

				sent_words.append(bigram)

				j = j + 1

		#This list holds the terms of the final sentence to be generated
		sent_words1 = []
		j = 0
		generated_word = ''

		#The 2nd condition in the while loop takes care of the stopping criteria. However, the first condition was added just as a safety measure.
		while (j < len(sent_words)) and (generated_word not in boundary_terms):
			if j == 0:
				sent_words1.append(sent_words[j][0])
				sent_words1.append(sent_words[j][1])
			else:
				sent_words1.append(sent_words[j][1])
				generated_word = sent_words[j][1]
			j = j + 1
		
		final_sentence = ' '.join(sent_words1)

		print i+1,':',final_sentence

def generate_trigrams():
	for i in range(len(s1)):
		regex = r'\w+|[,!?&.;":-_]' #This regular expression generates a list of all tokens.
		p1 = re.findall(regex,s1[i])

		j = 0

		#Using this loop, trigrams get generated from the produced list of tokens.
		while j < len(p1) - 2:
			trigrams.append((p1[j] , p1[j+1] , p1[j+2]))
			j = j + 1

def generate_trigram_sentences():

	generate_trigrams()

	for i in range(int(sys.argv[2])):
		
		b = []
		sent_words = [] #This list holds each trigram which was produced.
		boundary_terms = ['.' , '!' , '?']
		j = 0
		start_word = ''
		final_sentence = ''

		while start_word not in boundary_terms: 

			if sent_words == []:
				trigram_no = random.randint(0,len(trigrams))
				sent_words.append(trigrams[trigram_no])
				start_word = sent_words[j][2]
			else:
				start_word = sent_words[j][2] #The 3rd word is chosen as the new start word because it 
				
				b = [item for item in trigrams if item[0] == start_word] #Searching for those trigrams whose first element is the current start_word.
				prob_for_each_trigram = []
				for k in b:
					prob_for_each_trigram.append( trigrams.count(k) / len(trigrams) ) #Probability of a trigram is defined as
																				   #number of occurences of the trigram / total number of trigrams.

				start_val = min(prob_for_each_trigram)
				end_val = max(prob_for_each_trigram)

				r = random.uniform(start_val , end_val)

				diff_list = []

				for k in prob_for_each_trigram:
					diff_list.append(abs(r-k))

				index_of_element_with_least_diff = diff_list.index( min(diff_list) )

				trigram = b[index_of_element_with_least_diff]

				sent_words.append(trigram)

				j = j + 1

		#This list holds the terms of the final sentence to be generated
		sent_words1 = []
		j = 0
		generated_word = ''

		#The 2nd condition in the while loop takes care of the stopping criteria. However, the first condition was added just as a safety measure.
		while (j < len(sent_words)) and (generated_word not in boundary_terms):
			if j == 0:
				sent_words1.append(sent_words[j][0])
				sent_words1.append(sent_words[j][1])
				sent_words1.append(sent_words[j][2])
			else:
				sent_words1.append(sent_words[j][2])
				generated_word = sent_words[j][2]
			j = j + 1
		
		final_sentence = ' '.join(sent_words1)

		print i+1,':',final_sentence

file_number = 3 #It starts from 3 as file names start from the 4th index on the command line (indexing starts from 0).
s1 = [] #This list stores each line of the input file.
s2 = [] #This list stores terms from s1, on which regular expressions have been applied. Each term in this list is in turn another list.
s3 = [] #This list stores the list of lists from s2 as a single list.
uprobs = {} # This is a dictionary which stores the unigram probability for each word type.
bigrams = [] #The entire list of bigrams.
trigrams = [] #The entire list of trigrams.
		
#PREPROCESSING
while file_number < len(sys.argv):

	s1 = [] 
	s2 = [] 
	
	file = open (sys.argv[file_number] , "r" )
	
	for line in file:
		s1.append(line.lower())

	for i in s1:
		s2.append(re.findall(r"[\w]+|[\.\!\?\:\,\;\"\(\)\#\$\%\^\&\*\-\_]", i))

	for i in s2:
		s3 = s3 + i

	file_number = file_number + 1

vocabluary = Counter(s3)
N = sum(vocabluary.values()) #TOKENS
V = len(vocabluary.keys()) #TYPES

print "This program generates random sentences based on an Ngram model. CS 5761 by SAPTARSHI SENGUPTA.\n"
print "Command line settings : " , sys.argv[0] , sys.argv[1] , sys.argv[2]

if int(sys.argv[1]) == 1:
	print "Unigram Model Sentences:\n"
	generate_unigram_sentences()
elif int(sys.argv[1]) == 2:
	print "Bigram Model Sentences:\n"
	generate_bigram_sentences()
elif int(sys.argv[1]) == 3:
	print "Unigram Model Sentences:\n"
	generate_trigram_sentences()