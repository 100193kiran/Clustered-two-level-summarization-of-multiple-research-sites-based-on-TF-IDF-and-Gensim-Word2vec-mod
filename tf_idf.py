#TF-IDF Algorithm Implemented
import nltk
from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords
nltk.download('stopwords')
import math

stopwords = set(stopwords.words('english'))

def _create_freq_table(text_string) -> dict:
	'''
	Removes topwords and make freq tables
	:text_string : input sting of words
	: return a dictionary of the word frequencies
	'''
	stopwords = set(stopwords.words('english'))
	words = word_tokenize(test_string)
	ps = PortStemmer()

	freq_table = dict()
	for word in words:
		word = ps.stem(word)
		if word in stopwords:
			continue
		if word in freq_table:
			freq_table[word] += 1
		else:
			freq_table[word] = 1

	return freq_table


def _create_frequency_matrix(sentences):
	freq_matrix = {}
	ps = PorterStemmer()

	for sent in sentences:
		freq_table = {}
		words = word_tokenize(sent)
		for word in words:
			word = word.lower()
			word = ps.stem(word)
			if word in stopwords:
				continue

			if word in freq_table:
				freq_table[word] += 1
			else:
				freq_table[word] = 1

		freq_matrix[sent[:15]] = freq_table
	return freq_matrix

def _create_tf_matrix(freq_matrix):
	tf_matrix = dict()

	for sent, f_table in freq_matrix.items():
		tf_table = {}

		count_words_in_sentence = len(f_table)
		for word, count in f_table.items():
			tf_table[word] = count/count_words_in_sentence

		tf_matrix[sent] = tf_table
	return tf_matrix



def _create_documents_per_words(freq_matrix):
	word_per_doc_table = dict()

	for sent, f_table in freq_matrix.items():
		for word, count in f_table.items():
			if word in word_per_doc_table:
				word_per_doc_table[word] += 1
			else:
				word_per_doc_table[word] = 1

	return word_per_doc_table


def  _create_idf_matrix(freq_matrix, count_doc_per_words, total_documents):
	idf_matrix = dict()

	for sent, f_table in freq_matrix.items():
		idf_table = {}

		for word in f_table.keys():
			idf_table[word] = math.log10(total_documents/float(count_doc_per_words[word]))

		idf_matrix[sent] = idf_table

	return idf_matrix


def _create_tf_idf_matrix(tf_matrix,idf_matrix):
	tf_idf_matrix = dict()

	for (sent1,f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):
		tf_idf_table = {}

		for (word1, value1), (word2, value2) in zip(f_table1.items(), f_table2.items()):
			tf_idf_table[word1] = float(value1*value2)

		tf_idf_matrix[sent1] = tf_idf_table
	return tf_idf_matrix


def  _score_sentences(tf_idf_matrix) -> dict:
	"""
	Scores a sentence by its word's TF
	Basic algorithm:  adding the TF frequency of every non-stop words in a sentence
	divided by total number of words in the sentence
	: returns : dict 
	"""
	sent_value = {}

	for sent, f_table in tf_idf_matrix.items():
		total_sent_score = 0

		count_words = len(f_table)
		for word, score in f_table.items():
			total_sent_score += score
		if count_words > 0:
			sent_value[sent] = total_sent_score / count_words

	return sent_value


def _find_average_score(sent_value) -> int:
	"""
	Finds the average score from the sentence value dictionary
	:returns : int
	"""
	sumValues = 0

	for entry in sent_value:
		sumValues += sent_value[entry]

	#Average value of a sentence from original summary_text
	tot_sent = len(sent_value)
	avg = (sumValues/tot_sent) if tot_sent > 0 else sumValues

	return avg
	

def _generate_summary(sentences, sent_value, threshold):
	sent_count = 0
	summary = ''
	
	for sent in sentences:
		if sent[:15] in sent_value and sent_value[sent[:15]]>=(threshold):
			summary += " "+sent
			sent_count += 1

	return summary

def run_summarization(text):
	"""
	:param text: Plain Summary text of long articles
	:return: summarized summary text
	"""
	# 9 step procedure
	# 1 Sentence tokenize
	sentences = sent_tokenize(text)
	total_documents = len(sentences)

	# 2 Create the frequency matrix of the words in each sentence.
	freq_matrix = _create_frequency_matrix(sentences)

	# 3 Calculate the TermFrequency and generate a matrix
	tf_matrix = _create_tf_matrix(freq_matrix)

	# 4 Creating table for documents per words
	count_doc_per_words = _create_documents_per_words(freq_matrix)

	# 5 calculat the IDF and generate a matrix
	idf_matrix = _create_idf_matrix(freq_matrix,count_doc_per_words,total_documents)

	# 6 Calculate tf_idf and generate a matric
	tf_idf_matrix = _create_tf_idf_matrix(tf_matrix, idf_matrix)

	# 7 Important Algorithms: Score the sentences
	sentence_scores = _score_sentences(tf_idf_matrix)

	# 8 Find the threshold
	threshold = _find_average_score(sentence_scores)

	# 9 Important Algorithm: Generate the summary
	summary = _generate_summary(sentences,sentence_scores,1.3*threshold)

	return summary