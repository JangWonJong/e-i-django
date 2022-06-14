from konlpy.tag import Okt
from nltk.tokenize import word_tokenize
import nltk
import re
import pandas as pd
from nltk import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import tweepy
from icecream import ic

from context.domains import File, Reader

'''
    자연어처리 4단계
	1. Preprocessing
	2. Tokenization
	3. Token Embedding
    4. Document Embedding
'''
class Solution(Reader):
    def __init__(self):
        self.okt = Okt()
        self.file = File()
        self.file.context = './data/'

    def hook(self):
        def print_menu():
            print('0. Exit')
            print('1. kr-Report_2018.txt 읽기.')
            print('2. Tokenization.')
            print('3. Token Embedding.')
            print('4. Document Embedding.')
            print('5. 2018년 삼성사업계획서를 분석해서 워드클라우드를 작성하시오.')
            return input('메뉴 선택 \n')

            while 1:
                menu = print_menu()
                if menu == '0':
                    break
                if menu == '1':
                    self.preprocessing()
                if menu == '2':
                    self.tokenization()
                if menu == '3':
                    self.token_embedding()
                if menu == '4':
                    self.document_embedding()
                if menu == '5':
                    self.draw_wordcloud()
                elif menu == '0':
                    break


    def preprocessing(self):
        file = self.file
        file.fname = 'kr-Report_2018.txt'
        file = self.new_file(file)
        self.okt.pos("삼성전자 글로벌센터 전자사업부", stem=True)
        with open(file, 'r', encoding='UTF-8') as f:
            texts = f.read()
        ic(texts)
        return texts

    def tokenization(self):
        pass

    def token_embedding(self):
        pass

    def document_embedding(self):
        pass

    def draw_wordcloud(self):
        pass

if __name__ == '__main__':
    Solution().hook()