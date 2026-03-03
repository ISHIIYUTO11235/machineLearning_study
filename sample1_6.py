import numpy as np
from sklearn.linear_model import LinearRegression

# データの準備
D = np.array([[1, 3], [3, 6], [6, 5], [8, 7]])
X = D[:,0]
Y = D[:,1]

# ==========================================
# 方法1: scikit-learnを使用するアプローチ
# ==========================================
# scikit-learnは入力Xが2次元配列である必要があるため変換
X_sklearn = X.reshape(-1, 1)

model = LinearRegression()
model.fit(X_sklearn, Y)
a_sklearn = model.coef_[0]
b_sklearn = model.intercept_

print("--- 方法1: scikit-learn ---")
print(f"傾き: {a_sklearn:.4f}, 切片: {b_sklearn:.4f}")