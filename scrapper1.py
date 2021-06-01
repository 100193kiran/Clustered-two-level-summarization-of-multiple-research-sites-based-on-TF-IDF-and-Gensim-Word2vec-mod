import requests
from bs4 import BeautifulSoup
import json
import pandas as pd 

class gScholarScraper(object):

    def __init__(self, keyword, N):
        self.keyword = keyword
        self.google_scholar_url = "http://scholar.google.com/scholar"
        self.url = self.google_scholar_url+"?hl=en&as_sdt=0%2C5&q="+keyword.replace(' ', '+')+"&btnG="
        self.N = N
        

    def getContent(self, i):
        r = requests.get(self.url)
        content = r.content
        file = open("output.html", 'wb')
        file.write(content)
        file.close()
        return content

    def getTitle(self, paper):
        title = paper.find('h3', {'class': 'gs_rt'})
        #print title.text
        try:
            return title.text
        except Exception as e:
            return ""

    def getURL(self, paper):
        url = paper.find('h3', {'class': 'gs_rt'})
        #print url.a.get('href')
        try:
            return url.a.get('href')
        except Exception as e:
            return ""

    def getAuthors(self, paper):
        authors = paper.find('div', {'class': 'gs_a'})
        #print authors.text
        try:
            return authors.text
        except Exception as e:
            return ""

    def getAbstract(self, paper):
        abstract = paper.find('div', {'class': 'gs_rs'})
        #print abstract.text
        try:
            return abstract.text
        except Exception as e:
            return ""

    def getCited(self, paper):
        cited = paper.find('div', {'class': 'gs_fl'})
        cited = str(cited.text).replace('Cited by ', "").split(' ')[0]
        #print cited
        try:
            return cited
        except Exception as e:
            return ""

    def main(self):
        papersList = list()
        for i in range(int(N)):
            content = self.getContent(i)
            soup = BeautifulSoup(content)
            papers = soup.find_all('div', {'class' : 'gs_ri'})
            for paper in papers:
                paperDict = dict()
                paper = BeautifulSoup(str(paper))
                paperDict['title'] = self.getTitle(paper)
                paperDict['url'] = self.getURL(paper)
                paperDict['authors'] = self.getAuthors(paper)
                paperDict['abstract'] = self.getAbstract(paper)
                paperDict['cited'] = self.getCited(paper)
                papersList.append(paperDict)
        return papersList
            


N = 4


def create_df1(keyword, N=N):
    scholar = gScholarScraper(keyword, N)
    data = scholar.main()
    cols = ('title','url','authors','abstract','cited')
    df = pd.DataFrame(list(data),columns=cols)
    return df.to_csv(f'{keyword}.csv')

