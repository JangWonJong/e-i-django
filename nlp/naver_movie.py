import urllib.request

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from icecream import ic
from matplotlib import font_manager, rc
rc('font', family=font_manager.FontProperties(fname='C:/Windows/Fonts/malgunsl.ttf').get_name())
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['axes.unicode_minus'] = False
import math
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
            print('1. Preprocessing : Text Mining.')
            print('2. Preprocessing : DF streotype.')
            print('3. Tokenization.')
            print('4. Embedding.')
            print('5. Postprocessing.')
            print('6. visualize.')
            print('7. rating_distribution.')
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
            elif menu == '5':
                self.postprocessing()
            elif menu == '6':
                self.visualize()
            elif menu == '7':
                self.rating_distribution()
            elif menu == '0':
                break

    def preprocessing(self):
        self.streotype()
        df = self.movie_comment
        ic(df.head(5))
        # 코멘트가 없는 리뷰 데이터(NaN) 제거
        df = df.dropna()
        # 중복 리뷰 제거
        df = df.drop_duplicates(['comment'])
        # 영화 리스트 확인
        movie_lst = df.title.unique()
        ic('전체 영화 편수 =', len(movie_lst))
        ic(movie_lst[:10])
        # 각 영화 리뷰 수 계산
        cnt_movie = df.title.value_counts()
        ic(cnt_movie[:20])
        # 각 영화 평점 분석
        info_movie = df.groupby('title')['score'].describe()
        info_movie.sort_values(by=['count'], axis=0, ascending=False)
        # 긍정, 부정 리뷰 수
        df.label.value_counts()


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
        return self.movie_comment

    def visualize(self):
        df = self.streotype()
        top10 = df.title.value_counts().sort_values(ascending=False)[:10]
        top10_title = top10.index.tolist()
        top10_reviews = df[df['title'].isin(top10_title)]
        ic(top10_title)
        ic(top10_reviews.info())
        movie_title = top10_reviews.title.unique().tolist()  # -- 영화 제목 추출
        avg_score = {}  # -- {제목 : 평균} 저장
        for t in movie_title:
            avg = top10_reviews[top10_reviews['title'] == t]['score'].mean()
            avg_score[t] = avg

        plt.figure(figsize=(10, 5))
        plt.title('영화 평균 평점 (top 10: 리뷰 수)\n', fontsize=17)
        plt.xlabel('영화 제목')
        plt.ylabel('평균 평점')
        plt.xticks(rotation=20)

        for x, y in avg_score.items():
            color = np.array_str(np.where(y == max(avg_score.values()), 'orange', 'lightgrey'))
            plt.bar(x, y, color=color)
            plt.text(x, y, '%.2f' % y,
                     horizontalalignment='center',
                     verticalalignment='bottom')
        plt.show()

    def rating_distribution(self, avg_score ,top10_reviews):
        fig, axs = plt.subplots(5, 2, figsize=(15, 25))
        axs = axs.flatten()
        for title, avg, ax in zip(avg_score.keys(), avg_score.values(), axs):
            num_reviews = len(top10_reviews[top10_reviews['title'] == title])
            x = np.arange(num_reviews)
            y = top10_reviews[top10_reviews['title'] == title]['score']
            ax.set_title('\n%s (%d명)' % (title, num_reviews), fontsize=15)
            ax.set_ylim(0, 10.5, 2)
            ax.plot(x, y, 'o')
            ax.axhline(avg, color='red', linestyle='--')  # -- 평균 점선 나타내기

        plt.show()

    def tokenization(self):
        pass

    def embedding(self):
        pass
    def postprocessing(self):
        pass
if __name__ == '__main__':
    Solution().hook()