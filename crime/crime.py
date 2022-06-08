

from context.domains import Reader, Printer, File


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

    def save_cctv_pos(self):
        self.file.fname = 'cctv_in_seoul'
        self.myprint(self.csv(self.file))


    def save_police_norm(self):
        pass

    def folium_test(self):
        pass

    def draw_crime_map(self):
        self.file.fname = 'geo_simple'
        self.myprint(self.json(self.file))

if __name__ == '__main__':
    Solution().save_police_pos()
    #Solution().save_police_pos2('crime_in_seoul')
    Solution().save_cctv_pos()
    Solution().draw_crime_map()