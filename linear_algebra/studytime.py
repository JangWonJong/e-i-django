
import numpy as np
import matplotlib.pyplot as plt

class Studytime(object):
    def __init__(self):
        self.x_data = np.array([1, 2, 3, 4, 5, 7, 8, 10, 12, 13, 14, 15, 18, 20, 25, 28, 30]).reshape(-1, 1)
        self.t_data = np.array([5, 7, 20, 31, 40, 44, 46, 49, 60, 62, 70, 80, 85, 91, 92, 97, 98]).reshape(-1, 1)
        self.W = np.random.rand(1,1)
        self.b = np.random.rand(1)

    def loss_func(self,x,t):
        y = np.dot(x, self.W) + self.b
        return np.mean(np.power((t - y), 2))  # 최소 제곱법

    # 4. 미분함수
    @staticmethod
    def numerical_derivative(f, x):
        # f : 미분하려고 하는 다변수 함수
        # x : 모든 변수를 포함하고 있는 ndarray
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
        return np.dot(x, self.W) + self.b  # Hypothesis, Linear Regression Model

    def solution(self):
        learning_rate = 0.0001
        f = lambda x: self.loss_func(self.x_data, self.t_data)

        for step in range(90000):
            self.W = self.W - learning_rate * self.numerical_derivative(f, self.W)  # W의 편미분
            self.b = self.b - learning_rate * self.numerical_derivative(f, self.b)  # b의 편미분

            if step % 9000 == 0:
                print('W : {}, b : {}, loss : {}'.format(self.W, self.b, self.loss_func(self.x_data, self.t_data)))

        print(self.predict(19))  # [[77.86823633]]
        plt.scatter(self.x_data.ravel(), self.t_data.ravel())
        plt.plot(self.x_data.ravel(), np.dot(self.x_data, self.W) + self.b)  # 직선
        plt.show()

if __name__ == '__main__':
    Studytime().solution()
