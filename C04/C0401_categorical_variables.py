# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   introduction_to_ml_with_python
@File       :   C0401_categorical_variables.py
@Version    :   v0.1
@Time       :   2019-10-10 09:33
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《Python机器学习基础教程》, Sec0401，P161
@Desc       :   数据表示与特征工程。分类变量。
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 设置数据显示的精确度为小数点后3位
np.set_printoptions(precision = 3, suppress = True, threshold = np.inf)
# -------
# 显示所有列，默认为5
pd.set_option('display.max_columns', None)
# -------
# deprecated，使用display_max_rows代替
# pd.set_option('display.height',1000)
# 显示所有行，默认为5
pd.set_option('display.max_rows', None)
# -------
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 500)
# -------
# 设置显示的宽度，默认为80
pd.set_option('display.width', 1000)


# 4.1.1 One-Hot编码（虚拟变量）
def one_hot_encode():
    read_data = pd.read_csv('../data/adult.data', header = None, index_col = False,
                            names = ['age', 'workclass', 'fnlwgt', 'education', 'education-num',
                                     'marital-status', 'occupation', 'relationship', 'race', 'gender',
                                     'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income'])
    data = read_data[['age', 'workclass', 'education', 'gender', 'hours-per-week', 'occupation', 'income']]
    print("-- data的前五个数据内容 --")
    print('=' * 20)
    print(data.head())

    # 1. 检查字符串编码的分类数据
    # 使用pandas的Series数据类型（Series是DataFrame中单列对应的数据类型）的value_counts()函数
    print('-' * 20)
    print("显示gender字段的唯一值及其出现的次数：")
    print(data.gender.value_counts())

    # 使用get_dummies()自动变换所有具有对象类型（比如字符串）的列或者所有分类的列。
    # 分类特征的每个可能取值都被扩展为一个新的特征。
    print('-' * 20)
    print('原始特征的名称:\n', list(data.columns), '\n')
    data_dummies = pd.get_dummies(data)
    print('扩展后的所有特征名称:\n', list(data_dummies.columns))

    # 组合的特征太多，只显示其中的5个
    pd.set_option('display.max_columns', 5)
    print('-' * 20)
    print("data_dummies的前五个数据内容：")
    print(data_dummies.head())

    # .ix is deprecated. Please use .loc for label based indexing or .iloc for positional indexing
    # features = data_dummies.ix[:, 'age':'occupation_Transport-moving']
    print('-' * 20)
    print("-- 提取包含特征的列 --")
    print("从age到occupation_ Transport-moving的所有列")
    features = data_dummies.loc[:, 'age':'occupation_ Transport-moving']
    X = features.values  # 转化为Numpy数组
    y = data_dummies['income_ >50K'].values
    print('X.shape(): {}, y.shape(): {}'.format(X.shape, y.shape))
    print('X=', X[:5])
    print('y=', y[:5])
    bincount = np.bincount(y)
    print('np.bincount(y) = 0的个数 {} 和 1的个数 {}', bincount[0], bincount[1])

    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 0)
    log_reg = LogisticRegression(solver = 'lbfgs', max_iter = 10000)
    log_reg.fit(X_train, y_train)
    print('=' * 20)
    print('基于LogisticRegression学习的测试集评价: {:.2f}'.format(log_reg.score(X_test, y_test)))

    pass


# 4.1.2. 数字可以编码分类变量
def demo_dataframe():
    demo_df = pd.DataFrame({'Integer Feature': [0, 1, 2, 1], 'Categorical Feature': ['socks', 'fox', 'socks', 'box']})
    demo_df_str = demo_df.copy()
    demo_df_str['Integer Feature'] = demo_df['Integer Feature'].astype(str)  # 转换成str类型
    demo_df_dummies = pd.get_dummies(demo_df)
    demo_df_str_dummies = pd.get_dummies(demo_df_str)
    print("表4-4：包含分类字符串特征和整数特征的数据框")
    print(demo_df)
    print('-' * 40)
    print("表4-4-str：包含分类字符串特征和整数字符串特征的数据框")
    print(demo_df_str)
    print('-' * 40)
    print("表4-5：表4-4中数据的One-Hot编码版本，整数特征不变")
    print(demo_df_dummies)
    print('-' * 40)
    print("表4-5：表4-4-str中数据的One-Hot编码版本，整数字符串特征也同时编码")
    print(demo_df_str_dummies)
    from tabulate import tabulate
    print(tabulate(demo_df_str_dummies))


if __name__ == "__main__":
    # 4.1.1 One-Hot编码（虚拟变量）
    # one_hot_encode()
    demo_dataframe()

    import winsound

    # 运行结束的提醒
    winsound.Beep(600, 500)
    if len(plt.get_fignums()) != 0:
        plt.show()
    pass
