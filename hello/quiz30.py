import random
import string

import numpy as np
import pandas as pd
from icecream import ic
from domains import memberlist
from context.models import Model


class Quiz30:
    '''
            데이터프레임 문제 Q02
        ic| df:     A   B   C
                1   1   2   3
                2   4   5   6
                3   7   8   9
                4  10  11  12
        '''
    def quiz30_df_4_by_3(self) -> str:

        # df = pd.DataFrame([[1,2,3],
        #                   [4, 5, 6],
        #                   [7, 8, 9],
        #                   [10,11,12]], index=range(1,5), columns=['A','B','C'])
        # 위 식을 리스트결합 형태로 분해해서 조립하시오

        # l1 = list(range(1,4))
        # l2 = list(range(4,7))
        # l3 = list(range(7,10))
        # l4 = list(range(10,13))


        d = {'1':range(1,4), '2':range(4,7), '3':range(7,10), '4':range(10,13)}
        df2 = pd.DataFrame.from_dict(d,orient='index',columns=['A','B','C'])
        ic(df2)

        # d1 = {'1':[1,2,3], '2':[4,5,6], '3':[7,8,9], '4':[10,11,12]}
        # df = pd.DataFrame(d1)
        # df.index = [i for i in range(1,5)]
        # ic(df)



        # val = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
        # idx = range(1, 5)
        # col = ['A', 'B', 'C']
        # df = pd.DataFrame(val, index=idx, columns=col)
        # ic(df)




        return None

    '''
            데이터프레임 문제 Q03.
            두자리 정수를 랜덤으로 2행 3열 데이터프레임을 생성
            ic| df:     0   1   2
                    0  97  57  52
                    1  56  83  80
        '''
    def  quiz31_rand_2_by_3(self) -> str:
        # l1 = [[myRandom(0,100) for i in  range(3)] for i in range(2)]
        # l2 = [str(i) for i in range(2)]
        # columns = [str(i) for i in range(3)]
        # # df = pd.DataFrame({})
        # # df = pd.DataFrame({},columns={})
        # df = pd.DataFrame(l1,index=l2,columns=columns)
        # ic(df)
        # df = pd.DataFrame(np.random.randint(10,100,size=(2,3)))
        # ic(df)

        val = [random.randint(10,100) for i in range(3)]
        idx = range(0,2)
        col = range(0,3)
        df = pd.DataFrame(val, index=idx, columns=col)
        ic(df)

        return None

    '''
               데이터프레임 문제 Q04.
               국어, 영어, 수학, 사회 4과목을 시험치른 10명의 학생들의 성적표 작성.
                단 점수 0 ~ 100이고 학생은 랜덤 알파벳 5자리 ID 로 표기

                 ic| df4:        국어  영어  수학  사회
                           lDZid  57  90  55  24
                           Rnvtg  12  66  43  11
                           ljfJt  80  33  89  10
                           ZJaje  31  28  37  34
                           OnhcI  15  28  89  19
                           claDN  69  41  66  74
                           LYawb  65  16  13  20
                           QDBCw  44  32   8  29
                           PZOTP  94  78  79  96
                           GOJKU  62  17  75  49
       '''

    @staticmethod
    def id(chr_size) ->str:
        return ''.join([random.choice(string.ascii_letters) for i in range(chr_size)]) #아스키레터에서 5개

    def quiz32_df_grade(self) -> str:
        # val = []
        # idx = []
        # col = []
        # df = pd.DataFrame(val, index=idx, columns=col)

        value = np.random.randint(0,100,(10,4))
        #value = [[myRandom(0,100) for i in range(4)] for i in range(10)]
        index = [self.id(chr_size=5) for i in range(10)]
        columns = ['국어','영어','수학','사회']
        df = pd.DataFrame(value, index=index, columns=columns)
        ic(df)
        #d = {i:j for i,j in zip(index,value)}
        d = dict(zip(index,value))
        df2 = pd.DataFrame.from_dict(d,orient='index',columns=columns)
        ic(df2)

        return None

    def quiz33_df_loc(self) -> str:
        '''d = [{'a':1, 'b':2,'c':3,'d':4},{'a':100, 'b':200,'c':300,'d':400},{'a':1000, 'b':2000,'c':3000,'d':4000}]'''
        '''df = self.createDf(keys=['a','b','c','d'],
                           vals=4,
                           len=3)
        ic(df)'''

        #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html
        #grade.csv
        subjects = ['Java', 'Python', 'JS', 'SQL']
        students = memberlist()
        scores = np.random.randint(0, 100, (24,4))
        students_scores = {student : score for student,score in zip(students,scores)}
        students_scores_df = pd.DataFrame.from_dict(students_scores, orient='index', columns=subjects)

        model = Model()
        #model.save_model(fname='grade.csv',dframe=students_scores_df)
        grade_df = model.new_model('grade.csv')
        ic(grade_df)

        print('Q1. 파이썬의 점수만 출력하시오')
        #python_scores = grade_df.iloc[:,1]
        python_scores= grade_df.loc[:,'파이썬']
        ic(python_scores)
        print(type(python_scores))
        print('Q2. 장원종의 점수만 출력하시오')
        s_scores = grade_df.loc['장원종']
        #s_scores = grade_df.loc[['장원종']]
        ic(type(s_scores))
        ic(s_scores)
        print('Q3. 장원종의 과목별 점수를 출력하시오')
        s_scores = grade_df.loc[['장원종']]
        ic(type(s_scores))
        ic(s_scores)


        '''score = np.random.randint(0,100,(4,3))
        sub = ['a','b','c','d']
        a = [{i:j for i,j in zip(sub,score) for _ in range(3)}]
        b = dict(zip(sub,score))
        c = [i for i in range(3)]
        print(a)
        df7 = pd.DataFrame([dict(zip(sub,score)) for _ in range(3)])
        ic(df7)'''

        '''
        d = dict(zip(sub, score))
        df = pd.DataFrame(d)
        ic(df)
        '''
        subj = ['Java', 'Python', 'JS', 'SQL']
        stud = memberlist()
        scores = np.random.randint(0,100,(len(stud),len(subj)))
        df1 = pd.DataFrame(scores,index=stud,columns=subj)
        #ic(df1)
        '''print('Q1. 파이썬의 점수만 출력하시오')
        python_scores = df1.iloc[:,1]
        ic(python_scores)

        print('Q2. 스칼라의 점수만 출력하시오')
        s_scores = df1.loc[['심민혜']]
        ic(s_scores)'''
        df1.to_csv('./save/scores.csv', sep=',', na_rep='NaN')

        '''d = dict(zip(stud,scores))
        df2 = pd.DataFrame.from_dict(d,orient='index',columns=subj)
        ic(df2)'''
        return None


    @staticmethod
    def createDf(keys, vals, len):
        return pd.DataFrame([dict(zip(keys,np.random.randint(0,100, vals)))for _ in range(len)])




    def quiz34(self) -> str:
        # ic(df.iloc[0])
        '''출력했을 때 결과
                ic| df.iloc[0]: a    36
                                b    82
                                c    70
                                d     2
                        Name: 0, dtype: int32
                '''
        # ic(df.iloc[[0]])
        '''출력했을 때 결과
        ic| df.iloc[[0]]:     a   b   c   d
                           0  71  42  91  11
        '''
        # ic(df.iloc[[0,1]])
        '''출력했을 때 결과
        ic| df.iloc[[0,1]]:     a   b   c  d
                             0  73  66  17  5
                             1  73  66  17  5
        '''
        # ic(df.iloc[:3])
        '''출력했을 때 결과
        ic| df.iloc[:3]:     a   b  c   d
                          0  20  77  0  14
                          1  20  77  0  14
                          2  20  77  0  14
        '''
        # ic(df.iloc[[True,False,True]])
        '''출력했을 때 결과
        ic| df.iloc[[True,False,True]]:    a   b   c   d
                                        0  0  66  58  31
                                        2  0  66  58  31
        '''
        # ic(df.iloc[lambda x: x.index % 2 == 0])
        '''출력했을 때 결과
        ic| df.iloc[lambda x: x.index % 2 == 0]:    a  b   c   d
                                                 0  3  7  84  30
                                                 2  3  7  84  30
        '''
        # ic(df.iloc[0, 1])
        '''출력했을 때 결과
        ic| df.iloc[0, 1]: 35
        '''
        # ic(df.iloc[[0, 2], [1, 3]])
        '''출력했을 때 결과
        ic| df.iloc[[0, 2], [1, 3]]:     b   d
                                     0  27  19
                                     2  27  19
        '''
        # ic(df.iloc[1:3, 0:3])
        '''출력했을 때 결과
        ic| df.iloc[1:3, 0:3]:     a   b   c
                                1  60  91  19
                                2  60  91  19
        '''
        # ic(df.iloc[:, [True, False, True, False]])
        '''출력했을 때 결과
        ic| df.iloc[:, [True, False, True, False]]:     a   c
                                                    0  60  19
                                                    1  60  19
                                                    2  60  19
        '''
        # ic(df.iloc[:, lambda df: [0, 2]])
        '''출력했을 때 결과
        ic| df.iloc[:, lambda df: [0, 2]]:     a   c
                                            0  60  19
                                            1  60  19
                                            2  60  19
        '''
        return None

    def quiz35(self) -> str: return None

    def quiz36(self) -> str: return None

    def quiz37(self) -> str: return None

    def quiz38(self) -> str: return None

    def quiz39(self) -> str: return None