# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   introduction_to_ml_with_python
@File       :   C0104.py
@Version    :   v0.1
@Time       :   2019-09-17 17:21
@License    :   (C)Copyright 2019-2020, zYx.Tom
@Reference  :   《Python机器学习基础教程》, Ch0104，P05
@Desc       :   引言。必要的库和工具
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# 1.4.2. NumPy
# 创建一个ndarray类的对象，是一个二维NumPy数组，也叫数组。
# NumPy 的学习可以参考 《利用Python进行数据分析》
def numpy_train():
    x = np.array([[1, 2, 3], [4, 5, 6]])
    print("x:\n{}".format(x))


# 1.4.3. SciPy
# SciPy 的学习可以参考 《Scipy Lecture Notes》(http://scipy-lectures.org/)
def scipy_train():
    # 创建一个二维NumPy数组，对角线为1，其余为0，稀疏矩阵（Sparse Matrix）的稠密表示（Dense Representation）
    eye = np.eye(4)
    print('NumPy array:\n{}'.format(eye))

    from scipy import sparse  # SciPy的稀疏矩阵有好几种形式
    # CSR格式比COO格式保存要多30%的内存占用率。COO格式一经定义后shape就不可再修改，但是data, row, col还可以修改。
    # 转换稀疏数组的表示方式为SciPy的CSR格式
    sparse_csr_matrix = sparse.csr_matrix(eye)
    print(('\nSciPy sparse CSR matrix:\n{}'.format(sparse_csr_matrix)))
    # 转换稀疏数组的表示方式为SciPy的COO格式
    sparse_coo_matrix = sparse.coo_matrix(eye)
    print(('\nSciPy sparse COO matrix:\n{}'.format(sparse_coo_matrix)))

    # 输出一个全1的4*4矩阵
    print('\n--------')
    data = np.ones((4, 4))
    print('NumPy array:\n{}'.format(data))

    # 输出一个全1的4*1向量，将之转化为COO格式的稀疏矩阵
    print('\n--------')
    data = np.ones(4)
    print('NumPy array:\n{}'.format(data))

    # 将之转化为COO格式的稀疏矩阵
    row_indices = np.arange(4)
    col_indices = np.arange(4)
    eye_coo = sparse.coo_matrix((data, (row_indices, col_indices)))
    print('\nCOO representation:\n{}'.format(eye_coo))


# 1.4.4. matplotlib
def matplotlib_train():
    # 生成一个序列，序列范围是-10到10，总共100个数
    x = np.linspace(-10, 10, 100)
    # 使用 sin 函数 生成第二个序列
    y = np.sin(x)
    plt.plot(x, y, marker='x')
    # plot 函数生成一个曲线图表
    plt.show()


# 1.4.5. pandas
def pandas_train():
    # 生成一个简单的人群数据集
    data = {
            'Name': ['John', 'Anna', 'Peter', 'Linda'],
            'Location': ['New York', 'Paris', 'Berlin', 'London'],
            'Age': [24, 13, 53, 33]
    }
    data_pandas = pd.DataFrame(data)
    print(data_pandas[data_pandas.Age > 30])
    # pandas.DataFrame对于数据分析很重要。


if __name__ == "__main__":
    # 1.4.2. NumPy
    # 创建一个ndarray类的对象，是一个二维NumPy数组，也叫数组。
    # numpy_train()

    # 1.4.3. SciPy
    # scipy_train()

    # 1.4.4. matplotlib
    # matplotlib_train()

    # 1.4.5. pandas
    pandas_train()

    import tools

    tools.beep_end()
    tools.show_figures()
