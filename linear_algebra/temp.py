import numpy as np
import pandas as pd


import matplotlib.pyplot as plt

class Temp(object):
    def __init__(self):
        url = "https://raw.githubusercontent.com/reisanar/datasets/master/ozone.data.csv"
        self.df = pd.read_csv(url)
        self.training_data = self.df[['temp', 'ozone']]
        self.x_data = self.training_data['temp'].values.reshape(-1, 1)
        self.t_data = self.training_data['ozone'].values.reshape(-1, 1)
        self.W = np.random.rand(1, 1)
        self.b = np.random.rand(1)


    def loss_func(self, x, t):
        y = np.dot(x, self.W) + self.b
        return np.mean(np.power((t - y), 2))  # 최소제곱법

    @staticmethod
    def numerical_derivative(f, x):
        delta_x = 1e-4
        derivative_x = np.zeros_like(x)
        it = np.nditer(x, flags=['multi_index'])

        while not it.finished:
            idx = it.multi_index  # iterator의 현재 index를 tuple 형태로 추출
            tmp = x[idx]
            x[idx] = tmp + delta_x
            fx_plus_delta = f(x)  # f(x + delta_x)
            x[idx] = tmp - delta_x
            fx_minus_delta = f(x)  # f(x - delta_x)
            derivative_x[idx] = (fx_plus_delta - fx_minus_delta) / (2 * delta_x)
            x[idx] = tmp
            it.iternext()

        return derivative_x

    def predict(self, x):
        return np.dot(x, self.W) + self.b

    def solution(self):
        learning_rate = 1e-5
        f = lambda x: self.loss_func(self.x_data, self.t_data)

        for step in range(90000):
            self.W -= learning_rate * self.numerical_derivative(f, self.W)
            self.b -= learning_rate * self.numerical_derivative(f, self.b)

            if step % 9000 == 0:
                print('W : {}, b : {}, loss : {}'.format(self.W, self.b, self.loss_func(self.x_data, self.t_data)))

        result = self.predict(62)
        print(result)  # [[34.56270003]]
        plt.scatter(self.x_data, self.t_data)
        plt.plot(self.x_data, np.dot(self.x_data, self.W) + self.b, color='r')
        plt.show()

if __name__ == '__main__':
    Temp().solution()