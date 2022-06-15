import re

import matplotlib.pyplot as plt
import nltk
import pandas as pd
from icecream import ic
from nltk import word_tokenize, FreqDist
from wordcloud import WordCloud

from context.domains import Reader, File
from konlpy.tag import Okt
import tweepy

class Solution(Reader):
    def __init__(self):
        self.file = File()
        self.okt = Okt()
        self.file.context = './data/'

    def hook(self):
        def print_menu():
            print('0. Exit')
            print('1. nltk 다운로드')
            print('2. 전처리')
            print('3. 워드클라우드')
            return input('메뉴 선택 \n')

        while 1:
            menu = print_menu()
            if menu == '0':
                break
            elif menu == '1':
                Solution.download()
            elif menu == '2':
                _ = self.preprocessing()
                ic(_)
            elif menu == '3':
                self.draw_wordcloud()


    @staticmethod
    def download():
        nltk.download('punkt')


    def preprocessing(self):
        self.okt.pos("삼성전자 글로벌센터 전자사업부", stem=True)
        file =  self.file
        file.fname = 'kr-Report_2018.txt'
        path = self.new_file(file)
        with open(path, 'r', encoding='UTF-8') as f:
            texts = f.read()
        texts = texts.replace('\n', ' ')
        tokenizer = re.compile(r'[^ㄱ-힣]+')
        return tokenizer.sub(' ', texts)

    def noun_embedding(self):
        nouns = []
        tokens = word_tokenize(self.preprocessing())
        for i in tokens:
            pos = self.okt.pos(i)
            _ = [j[0] for j in pos if j[1] == 'Noun']
            if len(''.join(_)) > 1:
                nouns.append(' '.join(_))
        return nouns

    def stopword_embedding(self):
        self.okt.pos("삼성전자 글로벌센터 전자사업부", stem=True)
        file = self.file
        file.fname = 'stopwords.txt'
        path = self.new_file(file)
        with open(path, 'r', encoding='UTF-8') as f:
            stopwords = f.read()

        return stopwords.split()

    def morphemes_embedding(self):
        nouns = self.noun_embedding()
        ic(nouns[:10])
        stopwords = self.stopword_embedding()
        morphemes = [text for text in nouns if text not in stopwords]
        ic(morphemes[:10])
        return morphemes

    def draw_wordcloud(self):
        _ = self.morphemes_embedding()
        freqtxt = pd.Series(dict(FreqDist(_))).sort_values(ascending=False)
        ic(type(freqtxt))
        wcloud = WordCloud('./data/D2Coding.ttf', relative_scaling=0.2,
                           background_color= 'white').generate(" ".join(_))
        plt.figure(figsize=(12, 12))
        plt.imshow(wcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

if __name__ == '__main__':
    print(tweepy.__version__)
    Solution().hook()