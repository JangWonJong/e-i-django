import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model

# 1. Raw Data Loading
df = pd.read_csv('./data/ozone.csv')

# 2. Data Preprocessing
training_data = df[['Temp', 'Ozone']]

training_data = training_data.dropna(how='any')

# 3. Training Data Set
x_data = training_data['Temp'].values.reshape(-1,1)
t_data = training_data['Ozone'].values.reshape(-1,1)

# 4. sklearn을 이용해서 linear regression model 객체를 생성
# 아직 완성되지 않은(학습되지 않은) 모델을 일단 생성
model = linear_model.LinearRegression()

# 5. Training Data Set을 이용해서 학습 진행
# fit() 함수를 이용
model.fit(x_data, t_data)

# 6. W와 b값을 알아내보자
# model.coef_ : W / model.intercept_ : b
print('W : {}, b : {}'.format(model.coef_, model.intercept_))
# W : [[2.4287033]], b : [-146.99549097]

# 7. 예측 수행
predict_val = model.predict([[62]])   # 온도를 이용해서 오존량 예측
print(predict_val)   # [[3.58411393]]

# 8. 그래프로 확인해보자
plt.scatter(x_data, t_data)
plt.plot(x_data, np.dot(x_data, model.coef_) + model.intercept_, color='r')
plt.show()

if __name__ == '__main__':
    pass