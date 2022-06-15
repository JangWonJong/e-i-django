import urllib.request

import pandas as pd
from bs4 import BeautifulSoup
from icecream import ic

from context.domains import Reader, File

'''
    자연어처리 4단계
	1. Preprocessing
	2. Tokenization
	3. Token Embedding
    4. Document Embedding
'''

class Solution(Reader):
    def __init__(self):
        self.file = File()
        self.file.context = './data/'


    def hook(self):
        def print_menu():
            print('0. Exit')
            print('1. Text Mining.')
            print('2. DF streotype.')
            print('3. Tokenization.')
            print('4. Embedding.')
            return input('메뉴 선택 \n')

        while 1:
            menu = print_menu()
            if menu == '0':
                break
            if menu == '1':
                self.crawling()
            elif menu == '2':
                self.preprocessing()
            elif menu == '3':
                self.tokenization()
            elif menu == '4':
                self.embedding()
            elif menu == '0':
                break

    def preprocessing(self):
        self.streotype()
        ic(self.movie_comment.head(5))
        ic(self.movie_comment)


    def crawling(self):
        file = self.file
        file.context = './save/'
        file.fname = 'movie_reviews.txt'
        path = self.new_file(file)
        f = open(path, 'w', encoding='UTF-8')

        for no in range(1, 501):
            url = 'https://movie.naver.com/movie/point/af/list.naver?&page=%d' % no
            html = urllib.request.urlopen(url)
            soup = BeautifulSoup(html, 'html.parser')

            reviews = soup.select('tbody > tr > td.title')
            for rev in reviews:
                rev_lst = []
                title = rev.select_one('a.movie').text.strip()
                score = rev.select_one('div.list_netizen_score > em').text.strip()
                comment = rev.select_one('br').next_sibling.strip()

                # -- 긍정/부정 리뷰 레이블 설정
                if int(score) >= 8:
                    label = 1  # -- 긍정 리뷰 (8~10점)
                elif int(score) <= 4:
                    label = 0  # -- 부정 리뷰 (0~4점)
                else:
                    label = 2
                f.write(f'{title}\t{score}\t{comment}\t{label}\n')

        f.close()

    def streotype(self):
        file = self.file
        file.context = './save/'
        file.fname = 'movie_reviews.txt'
        path = self.new_file(file)
        self.movie_comment = pd.read_csv(path, delimiter = '\t',
                           names=['title', 'score', 'comment', 'label'])


    def tokenization(self):
        pass

    def embedding(self):
        pass

if __name__ == '__main__':
    Solution().hook()