import nltk
import pandas as pd 
import streamlit as st 
from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


import re

# load stopwords 
stopwords = set(stopwords.words('english'))

def pre_process(text):
	# lower case
	text  = text.lower()

	#remove tags 
	text = re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)

	# remove special characters and digits
	text = re.sub("(\\d|\\W)+"," ",text)

	return text

# helper function to sort 
def _sorter(matrix):
	tuples = zip(matrix.col, matrix.data)
	return sorted(tuples, key=lambda x:(x[1],x[0]),reverse=True)

def extract_top(feature_names, sorted_items,topn=3):
	"""get the feature names and tf-idf score of top 3 items"""
	# use only topn  items from vector
	sorted_items = sorted_items[:topn]

	score_vals = []
	feature_vals = []

	# word, index & corresponding tf-idf score
	for idx, score in sorted_items:

		#keep track of feature names and its correspodning score
		score_vals.append(round(score,3))
		feature_vals.append(feature_names[idx])

	results = {}
	for idx in range(len(feature_vals)):
		results[feature_vals[idx]] = score_vals[idx]

	return results


def generate_keys(df):
	df['abstract'] = df.abstract.apply(lambda x:pre_process(x))

	# Set of abstracts
	docs = df['abstract'].tolist()

	# A vocabulary of words, 
	# ignore words appearing in 85% of documents,
	# Eliminate stop words
	cv = CountVectorizer(max_df=0.85, stop_words = stopwords,max_features = 10000)
	word_count_vector = cv.fit_transform(docs)


	tfidf_transformer = TfidfTransformer(use_idf=True)
	tfidf_transformer.fit(word_count_vector)


	# Feature names
	feature_names = cv.get_feature_names()

	# Get the document we want to extract keywords from
	doc = docs[0]

	# generate tf-idf for the given document
	tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))

	# sort the tf-idf vectors by descending order of scores
	sorted_items = _sorter(tf_idf_vector.tocoo())

	# extract only the topn n=3
	keywords = extract_top(feature_names, sorted_items,3)

	# now print results 
	# st.header('\n======Doc=====')
	# st.markdown(doc)
	st.header('\n======keywords=====')
	for k in keywords:
		st.markdown(k, keywords[k])

	return ''

# if __name__ == '__main__':
# 	df = pd.read_csv('pickle.csv')
# 	generate_keys(df)