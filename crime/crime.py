from context.domains import Reader, Printer, File
import folium

def test():
    pass

class Solution(Reader):

    def __init__(self):
        self.file = File()
        #self.reader = Reader()
        #self.printer = Printer()
        self.crime_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        self.crime_columns = ['살인', '강도', '강간', '절도', '폭력']
        self.file.context = './data/'

    def save_police_pos(self):
        self.file.fname = 'crime_in_seoul'
        self.myprint(self.csv(self.file))

    def save_police_pos2(self, fname):
        self.file.fname = fname
        self.myprint(self.csv(self.file))

    def save_police_pos3(self):
        file = self.file
        file.fname = 'crime_in_seoul'
        crime = self.csv(file)
        station_names = []
        for name in crime['관서명']:
            station_names.append(f'서울{str(name[:-1])}경찰서')
        print(f'station_names range: {len(station_names)}')
        for i, name in enumerate(station_names):
            print(f'name {i} {name}')
        gmaps = self.gmaps()
        a = gmaps.geocode('서울종암경찰서', language='ko')
        print(a)
        '''
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
        station_lng = []
        for i, name in enumerate(station_names):
            if name != '서울종암경찰서':
                temp = gmaps.geocode(name, language= 'ko')
            else:
                temp = [{'address_components': [{'long_name': '2 3', 'short_name': '2 ３', 'types': ['premise']},
                                                {'long_name': '서울', 'short_name': '종암로', 'types': ['political', 'sublocality', 'sublocality_level_4']},
                                                {'long_name': '성북구', 'short_name': '성북구', 'types': ['political', 'sublocality', 'sublocality_level_1']},
                                                {'long_name': '서울특별시', 'short_name': '서울특별시', 'types': ['administrative_area_level_1', 'political']},
                                                {'long_name': '대한민국', 'short_name': 'KR', 'types': ['country', 'political']},
                                                {'long_name': '139-230', 'short_name': '139-230', 'types': ['postal_code']}],
                         'formatted_address': '서울 성북구 종암로23길 52',
                         'geometry': {'location': {'lat': 37.60388169879458, 'lng': 127.04001571848704},
                                      'location_type': 'ROOFTOP',
                                      'viewport': {'northeast': {'lat': 37.60388169879458, 'lng': 127.04001571848704},
                                                   'southwest': {'lat': 37.60388169879458, 'lng': 127.04001571848704}}},
                         'partial_match': True, 'place_id': 'ChIJQ9zARmW5fDURgrNe_TNJWP4',
                         'plus_code': {'compound_code': 'J3RC+VC 대한민국 서울특별시', 'global_code': '8Q99J3RC+VC'},
                         'types': ['establishment', 'point_of_interest', 'police']}]

            print(f'name {i} = {temp[0].get("formatted_address")}')

    def save_cctv_pos(self):
        self.file.fname = 'cctv_in_seoul'
        print(self.csv(self.file))
        # 헤더는 2행, 사용하는 컬럼은 B, D, G, J, N 을 사용한다.
        self.file.fname = 'pop_in_seoul'
        cols = 'B, D, G, J, N'
        pop = self.xls(self.file, header=1, cols=cols, skiprows=[2])
        print(pop)

    def save_police_norm(self):
        pass

    def folium_test(self):
        self.file.fname = 'us-states'
        states = self.json(self.file)
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
        self.file.fname = 'geo_simple'
        self.myprint(self.json(self.file))

if __name__ == '__main__':
    #Solution().save_police_pos()
    #Solution().save_police_pos3()
    #Solution().save_cctv_pos()
    Solution().folium_test()
    #Solution().draw_crime_map()