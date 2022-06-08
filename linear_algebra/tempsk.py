import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model

from context.domains import Reader


class Tempsk():
    def __init__(self):
        url = "https://raw.githubusercontent.com/reisanar/datasets/master/ozone.data.csv"
        self.df = Reader().csv(url)
        #self.df = pd.read_csv(url)
        self.training_data = self.df[['temp', 'ozone']]
        self.training_data = self.training_data.dropna(how='any')
        self.x_data = self.training_data['temp'].values.reshape(-1, 1)
        self.t_data = self.training_data['ozone'].values.reshape(-1, 1)


    def solution(self):
        model = linear_model.LinearRegression()
        model.fit(self.x_data, self.t_data)
        print('W : {}, b : {}'.format(model.coef_, model.intercept_))
        predict_val = model.predict([[62]])  # 온도를 이용해서 오존량 예측
        print(predict_val)  # [[3.58411393]]
        plt.scatter(self.x_data, self.t_data)
        plt.plot(self.x_data, np.dot(self.x_data, model.coef_) + model.intercept_, color='r')
        plt.show()


if __name__ == '__main__':
    Tempsk().solution()