from multiprocessing import Process, Manager
import requests 
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
import numpy as np 
import sys

start_time = time.time()

def _get_page_no(showing_text):
	results = int((re.findall(r"(\d+,*\d+) results for all",showing_text)[0].replace(',','')))
	pages = results//200 + 1
	print(f" Total Results: {results} \n Total pages: {pages}")
	return pages 

def _clean(text):
	return text.replace("\n", '').replace("  ",'')

def _get_page_data(url,page_number,data):
	print(f"getting page {page_number + 1}")
	response = requests.get(url+"start="+str(page_number*200))
	soup = BeautifulSoup(response.content, "lxml")

	arxiv_results = soup.find_all("li",{"class","arxiv-result"})

	for arxiv_result in arxiv_results:
		paper = {} 
		paper["titles"]= _clean(arxiv_result.find("p",{"class","title is-5 mathjax"}).text)
		links = arxiv_result.find_all("a")
		paper["arxiv_ids"]= links[0].text.replace('arXiv:','')
		paper["arxiv_links"]= links[0].get('href')
		paper["pdf_link"]= links[1].get('href')
		paper["authors"]= _clean(arxiv_result.find("p",{"class","authors"}).text.replace('Authors:',''))

		split_abstract = arxiv_result.find("p",{"class":"abstract mathjax"}).text.split("▽ More\n\n\n",1)
		if len(split_abstract) == 2:
			paper["abstract"] = _clean(split_abstract[1].replace("△ Less",''))
		else: 
			paper["abstract"] = _clean(split_abstract[0].replace("△ Less",''))

		paper["date"] = re.split(r"Submitted|;",arxiv_results[0].find("p",{"class":"is-size-7"}).text)[1]
		paper["tag"] = _clean(arxiv_results[0].find("div",{"class":"tags is-inline-block"}).text) 
		doi = arxiv_results[0].find("div",{"class":"tags has-addons"})       
		if doi is None:
			paper["doi"] = "None"
		else:
			paper["doi"] = re.split(r'\s', doi.text)[1] 

		data.append(paper)
    
	print(f"page {page_number+1} done")


	



def create_df(keyword):
	url = f'https://arxiv.org/search/?searchtype=all&query={keyword.lower()}&abstracts=show&size=200&order=-announced_date_first&'
	response = requests.get(url+"start=0")
	soup = BeautifulSoup(response.content, "lxml")
	with Manager() as manager:
		data = manager.list()  
		processes = []
		_get_page_data(url,0,data)


		showing_text = soup.find("h1",{"class":"title is-clearfix"}).text
		try:
			for i in range(1,_get_page_no(showing_text)):
				p = Process(target=_get_page_data, args=(url,i,data))
				p.start()
				processes.append(p)
		except IndexError:
			print('Search term not found')
			sys.exit('Try another key word ):')


		for p in processes:
			p.join()

		# Columns of the keyword dataframe
		cols = ('arxiv_ids', 'titles', 'arxiv_links', 'pdf_link', 'authors', 'abstract', 'date', 'tag', 'doi')
		df = pd.DataFrame(list(data),columns=cols)
		
	return df.to_csv(f'{keyword}.csv')
	
