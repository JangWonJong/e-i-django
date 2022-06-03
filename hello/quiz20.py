import random
import urllib.request
from string import ascii_lowercase
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from domains import my100,myRandom,members
from quiz00 import Quiz00



class Quiz20:

    def quiz20list(self) -> str:
        list1 = [1, 2, 3, 4]
        # print(list1,type(list1))
        list2 = ['math', 'english']
        print('리스트1: ', list1[0], list1[-1], list1[-2])
        print('리스트1에서 1번째,2번째 성분출력: ', list1[1:3])
        print('리스트2에서 math출력:', list2[0])
        print('리스트2에서 a출력: ', list2[0][1])
        print('리스트2에서 math english 출력 :', list2[0], list2[1])
        list3 = [1, '2', [1, 2, 3]]
        list4 = [1, 2, 3]
        list5 = [4, 5]
        list4[-2:] = []
        print('리스트4 두배 출력: ', 2 * list4)
        print('리스트4와 리스트5 합치기:', list4 + list5)
        print('리스트4에 리스트5 성분합치기:', list4.append(list5))
        print('리스트4,5에서 [1,2] 출력해보기', list4)
        list6 = [[1, 2], [0, 5]]
        # 2를 출력해보시오
        a = [1, 2]
        b = [0, 5]
        c = [a, b]
        c[0][1] = 10
        print(list6[0][1])
        print(c)

        return None

    def quiz21tuple(self) -> str:
        tuple1 = (1, 2)
        tuple2 = (0, (1, 4))
        print(tuple1 + tuple2)

        return None

    def quiz22dict(self) -> str: return None

    def quiz23listcom(self) -> str:
        print('--------------legacy---------------')
        a = []
        for i in range(5):
            a.append(i)
        print(a)
        print('--------------comprehension---------------')
        a2 = [i for i in range(5)]
        print(a2)
        return None


    def quiz24zip(self)->{}:
        url = 'https://music.bugs.co.kr/chart/track/realtime/total'
        html_doc = urlopen(url)
        soup = BeautifulSoup(html_doc, 'lxml') # html.parser vs lxml
        ls1 = self.find_music(soup, 'title')
        ls2 = self.find_music(soup, 'artist')
        dt = {i:j for i,j in zip(ls1,ls2)}
        print(dt)
        #self.dict1(ls1,ls2)
        #self.dict2(ls1,ls2)
        #self.dict3(ls1, ls2)
        #컴프리헨션 부분 적어놓은 것
        a = [i if i ==0 or i ==0 else i for i in range(10)]
        b = [i if i ==0 or i ==0 else i for i in []]
        c = [(i,j) for i,j in enumerate([])]
        d = {i:j for i,j in zip(ls1,ls2)}
        l = [i + j for i,j in zip(ls1,ls2)]
        l2 = list[zip(ls1,ls2)]
        d1 = dict(zip(ls1,ls2))

    @staticmethod
    def dict1(ls1,ls2) -> None:
        dict = {}
        for i in range(0, len(ls1)):
            dict [ls1[i]] = ls2[i]
        print(dict)

    @staticmethod
    def dict2(ls1, ls2):
        dict = {}
        for i, j in enumerate(ls1):
            dict[j] = ls2[i]
        print(dict)

    @staticmethod
    def dict3(ls1,ls2):
        dict = {}
        for i,j in zip(ls1,ls2):
            dict[i] = j
        print(dict)


    def print_music_list(self, soup)->None:
        artists = soup.find_all('p', {'class': 'artist'})
        artists = [i.get_text() for i in artists]
        # print(''.join(i for i in artists))
        titles = soup.find_all('p', {'class': {'titles'}})
        titles = [i.get_text() for i in titles]
        # print(''.join(i for i in titles))

    def find_rank(self,soup):
        for i,j in enumerate(['artist','title']):
            for i,j in enumerate(self.find_music(soup,j)):
                print(f'{i}위 : {j}')
            print('*'*100)

            ''' self.bugs(soup,'artist')
             self.bugs(soup,'title')'''

    @staticmethod
    def find_music(soup,class_nm)->[]:
        ls = soup.find_all('p', {'class': class_nm})
        return [i.get_text() for i in ls]


    def quiz25dictcom(self)->str:
        #quiz06memberChoic() 를 import 해서 문제해결 여기서 5명 추출
        #students = [members[myRandom(0,23)]]
        #students = [Quiz00.quiz06memberChoice() for i in random.sample(members,5)]
        #scores = [my100() for i in range(5)]
        q = Quiz00
        abc = set([q.quiz06member_choice() for i in range(5)])
        while len(abc) != 5:
            abc.add(q.quiz06member_choice())
        students = list(abc)
        scores = [my100() for i in range(5)]
        d = {i:j for i,j in zip(students,scores)}
        print(d)
        #print(students2)
        #d1 = dict(zip(students,scores))
        #print(d1)



    def quiz26map(self) -> str: return None

    def quiz27melon(self) -> str:
        headers = {'User-Agent':'Mozilla/5.0' }
        url = 'https://www.melon.com/chart/index.htm?dayTime=2022030816'
        req = urllib.request.Request(url, headers=headers)
        soup = BeautifulSoup(urlopen(req).read(), 'lxml')#실시간차트 제목 출력하기
        #print(''.join([i.get_text() for i in soup.find_all('div',{'class':'ellipsis rank01'})[0:3]]))#세로출력
        print([i.get_text().strip() for i in soup.find_all('div', {'class': 'ellipsis rank01'})[0:3]])#가로출력(공백은 있음)

        '''a = soup.find_all('div',{'class':'ellipsis rank02'})
        a = [i.get_text() for i in a]
        print(''.join(i for i in a))'''

        '''a = soup.find_all('div',class_='ellipsis rank02')
        for i in a :
            print(i.get_text())'''


    def quiz28dataframe(self) -> None:
        df = self.quiz24zip()
        df = pd.DataFrame.from_dict(df, orient='index')
        print(df)
        df.to_csv('./save/bugs.csv', sep=',', na_rep='NaN')


    '''
    다음결과 출력
        a   b   c
    1   1   3   5
    2   2   4   6      
    '''

    def quiz29_pandas_df(self) -> object:
        # d1 = {'1':[1,3,5], '2':[2,4,6]}
        # df = pd.DataFrame(d1)
        # df.index = [i for i in range(1,3)]
        # d2 = {'1':[1,3,5], '2':[2,4,6]}
        '''d3 = {'1': [i if i%2==0 else '' for i in range(1,10)]}
        d5 = list(d3)
        d4 = {'2': [i if i%2==1 else '' for i in range(2,10)]}
        d6 = list(d4)'''
        l1 = []
        l2 = []
        c = [chr(i) for i in range(97, 100)]  # ['a', 'b', 'c']
        #e = [i if i ==0 else i for i in range(1,7)]
        [l1.append(i) if i % 2 == 0 else l2.append(i) for i in range(1,7)]
        dict = {'1': l2, '2': l1}
        df3 = pd.DataFrame.from_dict(dict, orient='index', columns=c)
        #print(df3)

        d1 = {'1':[1,3,5]}
        d2 = {'2':[2,4,6]}
        d3 ={i:j for i,j in zip(d1,d2)}

        df5 = pd.DataFrame.from_dict(d3,orient='index',columns=c)
        print(df5)

        #df2 = pd.DataFrame.from_dict(d2, orient='index', columns=c)
        #print(df2)


        return None


