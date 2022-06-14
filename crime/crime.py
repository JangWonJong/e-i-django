import numpy as np
from icecream import ic
import pandas as pd
from sklearn import preprocessing

from context.domains import Reader, File
import folium


class Solution(Reader):

    def __init__(self):
        self.file = File()
        #self.reader = Reader()
        #self.printer = Printer()
        self.file.context = './data/'
        self.crime_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        self.crime_columns = ['살인', '강도', '강간', '절도', '폭력']

    def hook(self):
        def print_menu():
            print('0. Exit')
            print('1. crime_in_seoul.csv, 구글맵 API 를 이용해서 서울시내 경찰서 주소목록파일을 작성하시오.')
            print('2. us-states.json, us_unemployment.csv 를 이용해서 미국 실업률 지도(folium_test.html)를 작성하시오.')
            print('3. cctv_in_seoul.csv, pop_in_seoul.csv 를 이용해서 서울시내 경찰서 주소목록파일(cctv_pop.csv)을 작성하시오.')
            print('4. police_pos.csv, 를 이용해서 경찰서 범죄검거율 정규화파일(police_norm.csv)을 작성하시오.')
            print('5. 주어진 데이터를 활용해서 서울시내 경찰서 범죄발생과 검거율 현황지도(폴리움)를 작성하시오.')
            return input('메뉴 선택 \n')

        while 1:
            menu = print_menu()
            if menu == '0':
                break
            if menu == '1':
                self.save_police_pos()
            if menu == '2':
                self.folium_test()
            if menu == '3':
                self.save_cctv_pos()
            if menu == '4':
                self.save_police_norm()
            if menu == '5':
                self.draw_crime_map()
            elif menu == '0':
                break

    '''def save_police_pos(self):
        self.file.fname = 'crime_in_seoul'
        self.myprint(self.csv(self.file))'''

    '''def save_police_pos2(self, fname):
        self.file.fname = fname
        self.myprint(self.csv(self.file))'''

    def save_police_pos(self):
        file = self.file
        file.fname = 'crime_in_seoul'
        crime = self.csv(file)
        station_names = []
        for name in crime['관서명']:
            station_names.append(f'서울{str(name[:-1])}경찰서')
        #print(f'station_names range: {len(station_names)}')
        for i, name in enumerate(station_names):
            print(f'name {i} {name}')
        gmaps = self.gmaps()

        '''
        a = gmaps.geocode('서울종암경찰서', language='ko')
        #print(a)
        [{'address_components': [{'long_name': '２８３', 'short_name': '２８３', 'types': ['premise']},
         {'long_name': '노원로', 'short_name': '노원로', 'types': ['political', 'sublocality', 'sublocality_level_4']},
         {'long_name': '노원구', 'short_name': '노원구', 'types': ['political', 'sublocality', 'sublocality_level_1']},
         {'long_name': '서울특별시', 'short_name': '서울특별시', 'types': ['administrative_area_level_1', 'political']},
         {'long_name': '대한민국', 'short_name': 'KR', 'types': ['country', 'political']},
         {'long_name': '139-230', 'short_name': '139-230', 'types': ['postal_code']}],
          'formatted_address': '대한민국 서울특별시 노원구 노원로 283',
          'geometry': {'location': {'lat': 37.6421389, 'lng': 127.0710473},
          'location_type': 'ROOFTOP',
          'viewport': {'northeast': {'lat': 37.6434878802915, 'lng': 127.0723962802915},
          'southwest': {'lat': 37.6407899197085, 'lng': 127.0696983197085}}}, 
          'partial_match': True, 'place_id': 'ChIJQ9zARmW5fDURgrNe_TNJWP4', 
          'plus_code': {'compound_code': 'J3RC+VC 대한민국 서울특별시', 'global_code': '8Q99J3RC+VC'}, 
          'types': ['establishment', 'point_of_interest', 'police']}]
        '''

        station_addrs = []
        station_lats = []
        station_lngs = []
        for i, name in enumerate(station_names):
            if name != '서울종암경찰서':
                temp = gmaps.geocode(name, language= 'ko')
            else:
                temp = self.jongampolice()

            #print(f'name {i} = {temp[0].get("formatted_address")}')
            '''
            0번 중부서인경우는 "대한민국 서울특별시 중구 수표로 27"이 담긴다.
            1번 종로서인경우는 "대한민국 서울특별시 종로구 율곡로 46"이 담긴다.
            '''
            station_addrs.append(temp[0].get('formatted_address'))
            t_loc = temp[0].get('geometry')
            station_lats.append(t_loc['location']['lat'])
            station_lngs.append(t_loc['location']['lng'])

        gu_names = []
        for name in station_addrs:
            temp = name.split()
            gu_name = [gu for gu in temp if gu[-1] == '구'][0]
            gu_names.append(gu_name)
        crime['구별'] = gu_names
        ic(crime)
        crime.to_csv('./save/police_pos.csv', index=False)

    def save_cctv_pos(self):
        file = self.file
        file.fname = 'cctv_in_seoul'
        #print(self.csv(self.file))
        cctv = self.csv(file)

        '''
             기관명    소계  2013년도 이전  2014년  2015년  2016년
        0    강남구  2780       1292    430    584    932
        1    강동구   773        379     99    155    377
        2    강북구   748        369    120    138    204
        3    강서구   884        388    258    184     81
        4    관악구  1496        846    260    390    613

        '''
        # 헤더는 2행, 사용하는 컬럼은 B, D, G, J, N 을 사용한다.
        file.fname = 'pop_in_seoul'
        cols = 'B, D, G, J, N'
        pop = self.xls(file, header=[1], cols=cols, skiprows=[2])
        #print(pop)
        '''
             자치구          합계        한국인     등록외국인   65세이상고령자
        0     합계        10197604.0  9926968.0  270636.0  1321458.0
        1    종로구        162820.0   153589.0    9231.0    25425.0
        2     중구        133240.0   124312.0    8928.0    20764.0
        3    용산구        244203.0   229456.0   14747.0    36231.0
        4    성동구        311244.0   303380.0    7864.0    39997.0
        '''
        #cctv.rename(columns={'기관명': '구별'}, inplace=True)
        #pop.rename(columns = {'자치구':'구별'}, inplace=True)
        cctv_pop = pd.DataFrame()
        cctv_pop.to_csv('./save/cctv_pop.csv')
        cctv.rename(columns = {cctv.columns[0]:'구별'}, inplace=True)
        cctv.drop(columns={cctv.columns[2],
                           cctv.columns[3],
                           cctv.columns[4],
                           cctv.columns[5]}, inplace=True)
        #ic(cctv)
        pop.rename(columns = {pop.columns[0]:'구별',
                              pop.columns[1]:'인구수',
                              pop.columns[3]:'외국인',
                              pop.columns[4]:'고령자'}, inplace=True)
        #pop.drop(26, axis=0)
        pop.dropna(how = 'all', inplace=True)
        pop['외국인비율'] = pop['외국인'] / pop['인구수'] * 100
        pop['고령자비율'] = pop['고령자'] / pop['인구수'] * 100
        #print(pop)
        #ic(pop)
        #cctv_pop = list[zip(cctv, pop)]
        #cctv_pop = pd.concat([cctv, pop], axis=1, join='inner')
        cctv_pop = pd.merge(cctv, pop)
        ic(cctv_pop)
        #cor1 = ['고령자비율'], ['소계'] # 상관계수 구하기
        #cor2 = ['외국인비율'], ['소계'] # 상관계수 구하기

        cor1 = np.corrcoef(cctv_pop['고령자비율'], cctv_pop['소계'])
        cor2 = np.corrcoef(cctv_pop['외국인비율'], cctv_pop['소계'])
        ic(f'고령자비율과 CCTV의 상관계수 {str(cor1)} \n'
           f'외국인비율과 CCTV의 상관계수 {str(cor2)} ')

        '''
         고령자비율과 CCTV 의 상관계수 [[ 1.         -0.28078554]
                                     [-0.28078554  1.        ]] 
         외국인비율과 CCTV 의 상관계수 [[ 1.         -0.13607433]
                                     [-0.13607433  1.        ]]
        r이 -1.0과 -0.7 사이이면, 강한 음적 선형관계,
        r이 -0.7과 -0.3 사이이면, 뚜렷한 음적 선형관계,
        r이 -0.3과 -0.1 사이이면, 약한 음적 선형관계,
        r이 -0.1과 +0.1 사이이면, 거의 무시될 수 있는 선형관계,
        r이 +0.1과 +0.3 사이이면, 약한 양적 선형관계,
        r이 +0.3과 +0.7 사이이면, 뚜렷한 양적 선형관계,
        r이 +0.7과 +1.0 사이이면, 강한 양적 선형관계
        고령자비율 과 CCTV 상관계수 [[ 1.         -0.28078554] 약한 음적 선형관계
                                    [-0.28078554  1.        ]]
        외국인비율 과 CCTV 상관계수 [[ 1.         -0.13607433] 거의 무시될 수 있는
                                    [-0.13607433  1.        ]]
        '''

        cctv_pop.to_csv('./save/cctv_pop.csv')

        '''
        표준화는 데이터의 평균을 0, 표준편차를 1로 만드는 것이다.
        x = (x - mu) / sigma
        scale = (x - np.mean(x, axis=0)) / np.std(x, axis=0)
        정규화는 최대값을 1, 최솟값을 0으로 만드는 것이다.
        '''
    def save_police_norm(self):

        file = self.file
        file.context = './data/'
        file.fname = 'crime_in_seoul'
        crime_in_seoul = self.csv(file)
        file.context = './save/'
        file.fname = 'police_pos'
        police_pos = self.csv(file)
        police = pd.pivot_table(police_pos, index='구별', aggfunc=np.sum)
        police['살인검거율'] = police['살인 검거'] / police['살인 발생'] * 100
        police['강도검거율'] = police['강도 검거'] / police['강도 발생'] * 100
        police['강간검거율'] = police['강간 검거'] / police['강간 발생'] * 100
        police['절도검거율'] = police['절도 검거'] / police['절도 발생'] * 100
        police['폭력검거율'] = police['폭력 검거'] / police['폭력 발생'] * 100
        police.drop(columns={police.columns[1],
                             police.columns[3],
                             police.columns[5],
                             police.columns[7],
                             police.columns[9]}, inplace=True)

        for i in self.crime_rate_columns:
            police[i].loc[police[i]> 100] = 100
        police.to_csv('./save/police.csv', sep=',', encoding='UTF-8')
        police.rename(columns={police.columns[0]:'살인',
                               police.columns[1]:'강도',
                               police.columns[2]:'강간',
                               police.columns[3]:'절도',
                               police.columns[4]:'폭력',}, inplace=True)

        ''' 
       police.rename(columns={
            '살인 발생': '살인',
            '강도 발생': '강도',
            '강간 발생': '강간',
            '절도 발생': '절도',
            '폭력 발생': '폭력'
        }, inplace=True)
        '''
        ic(police)

        x = police[self.crime_rate_columns].values
        min_max_scalar = preprocessing.MinMaxScaler()

        x_scaled = min_max_scalar.fit_transform(x.astype(float))
        police_norm = pd.DataFrame(x_scaled, columns=self.crime_columns, index=police.index)
        police_norm[self.crime_rate_columns] = police[self.crime_rate_columns]
        police_norm['범죄'] = np.sum(police_norm[self.crime_rate_columns], axis=1)
        police_norm['검거'] = np.sum(police_norm[self.crime_columns], axis=1)
        police_norm.to_csv('./save/police_norm.csv', sep=',', encoding='UTF-8')
        """ 
        피쳐 스케일링(Feature scalining)은 해당 피쳐들의 값을 일정한 수준으로 맞춰주는 것이다.
        이때 적용되는 스케일링 방법이 표준화(standardization) 와 정규화(normalization)다.
        
        1단계: 표준화(공통 척도)를 진행한다.
            표준화는 정규분포를 데이터의 평균을 0, 분산이 1인 표준정규분포로 만드는 것이다.
            x = (x - mu) / sigma
            scale = (x - np.mean(x, axis=0)) / np.std(x, axis=0)
        2단계: 이상치 발견 및 제거
        3단계: 정규화(공통 간격)를 진행한다.
            정규화에는 평균 정규화, 최소-최대 정규화, 분위수 정규화가 있다.
             * 최소최대 정규화는 모든 데이터를 최대값을 1, 최솟값을 0으로 만드는 것이다.
            도메인은 데이터의 범위이다.
            스케일은 데이터의 분포이다.
            목적은 도메인을 일치시키거나 스케일을 유사하게 만든다.              
        """

    def folium_test(self):
        #self.file.fname = 'us-states'
        #states = self.json(self.file)
        self.file.fname = 'us_unemployment'
        unemployment = self.csv(self.file)

        bins = list(unemployment["Unemployment"].quantile([0, 0.25, 0.5, 0.75, 1]))
        m = folium.Map(location=[48, -102], zoom_start=5)
        folium.Choropleth(
            geo_data='./data/us-states.json',
            name="choropleth",
            data=unemployment,
            columns=["State", "Unemployment"],
            key_on="feature.id",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=0.5,
            legend_name="Unemployment Rate (%)",
            bins= bins,
            reset=True
        ).add_to(m)

        m.save("./save/folium_test.html")


    def draw_crime_map(self):
        file = self.file
        file.fname = 'crime_in_seoul'
        crime = self.csv(file)
        self.file.fname = 'geo_simple'

        station_names = []
        for name in crime['관서명']:
            station_names.append(f'서울{str(name[:-1])}경찰서')
        # print(f'station_names range: {len(station_names)}')
        for i, name in enumerate(station_names):
            print(f'name {i} {name}')
        gmaps = self.gmaps()

        station_addrs = []
        station_lats = []
        station_lngs = []
        for i, name in enumerate(station_names):
            if name != '서울종암경찰서':
                temp = gmaps.geocode(name, language='ko')
            else:
                temp = self.jongampolice()

            station_addrs.append(temp[0].get('formatted_address'))
            t_loc = temp[0].get('geometry')
            station_lats.append(t_loc['location']['lat'])
            station_lngs.append(t_loc['location']['lng'])


    def jongampolice(self):
        return [{'address_components': [{'long_name': '2 3', 'short_name': '2 ３', 'types': ['premise']},
                                 {'long_name': '서울', 'short_name': '종암로',
                                  'types': ['political', 'sublocality', 'sublocality_level_4']},
                                 {'long_name': '성북구', 'short_name': '성북구',
                                  'types': ['political', 'sublocality', 'sublocality_level_1']},
                                 {'long_name': '서울특별시', 'short_name': '서울특별시',
                                  'types': ['administrative_area_level_1', 'political']},
                                 {'long_name': '대한민국', 'short_name': 'KR',
                                  'types': ['country', 'political']},
                                 {'long_name': '139-230', 'short_name': '139-230',
                                  'types': ['postal_code']}],
          'formatted_address': '서울 성북구 종암로23길 52',
          'geometry': {'location': {'lat': 37.60388169879458, 'lng': 127.04001571848704},
                       'location_type': 'ROOFTOP',
                       'viewport': {'northeast': {'lat': 37.60388169879458, 'lng': 127.04001571848704},
                                    'southwest': {'lat': 37.60388169879458, 'lng': 127.04001571848704}}},
          'partial_match': True, 'place_id': 'ChIJQ9zARmW5fDURgrNe_TNJWP4',
          'plus_code': {'compound_code': 'J3RC+VC 대한민국 서울특별시', 'global_code': '8Q99J3RC+VC'},
          'types': ['establishment', 'point_of_interest', 'police']}]

if __name__ == '__main__':
    Solution().hook()
    #Solution().save_police_pos()
    #Solution().save_police_pos3()
    #Solution().save_cctv_pos()
    #Solution().folium_test()
    #Solution().draw_crime_map()