# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   introduction_to_ml_with_python
@File       :   C0402_binning.py
@Version    :   v0.1
@Time       :   2019-10-10 09:52
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《Python机器学习基础教程》, Sec0402，P168
@Desc       :   数据表示与特征工程。分箱（离散化）、线性模型和树
"""
import matplotlib.pyplot as plt
import mglearn
import numpy as np
import pandas as pd

# 设置数据显示的精确度为小数点后3位
np.set_printoptions(precision = 3, suppress = True, threshold = np.inf, linewidth = 150)


# 4.2. 分箱（binning）、离散化（discretization）、线性模型 与 树
# 这是个回归预测问题。
# 线性模型只能对线性关系建模，对于单个特征的情况预测的结果就是直线。
#   - 使用特征分箱技术（离散化）可以将单个特征划分为多个特征，使线性模型也能够表示更加复杂的数据模型。
# 决策树可以构建更加复杂的数据模型，依赖于具体的数据表示。
# 决策树使用的是CART算法，也是个支持回归问题的算法，采用的也是分箱计算的方式。
# 所以计算的结果并不跟训练数据点完全重合。
# 回归问题的评价指标：
# R^2=(1-u/v), u=((y_true-y_pred)**2).sum(), v=((y_true-y_true.mean())**2).sum()
# R^2的最佳得分是（1.0），最差得分可以为负数。
def compare_linear_model_decision_tree():
    # 仔细观察数据之间的相关性带来的影响。
    # 有噪声数据训练数据和测试数据只有完全相同的样本数才存在完全相关，否则数据不相关。
    # 以下结论只适合训练数据与测试数据存在相关性时有用。（即无噪声数据）
    # 结论1：训练数据的数量增加，会提高决策树模型预测的精度；
    # 测试数据的数量增加，可能会降低决策树模型预测的精度。（这个对模型没有帮助，只是帮助理解评价指标）
    # 结论2：训练数据的数量增加，会降低线性回归模型预测的精度；
    # 测试数据的数量增加，可能会提高线性回归模型预测的精度。（这个对模型没有帮助，只是帮助理解评价指标）

    for train_number in [30, 60, 100]:
        # 准备训练数据，有噪声的正弦波
        from mglearn.datasets import make_wave
        X_train, y_train = make_wave(n_samples = train_number)

        # # 准备训练数据，无噪声的正弦波
        # X_train = np.linspace(-3, 3, train_number).reshape(-1, 1)
        # y_train = np.sin(X_train)

        print('=' * 40)
        for test_number in [30, 60, 100]:
            # 准备测试数据，有噪声的正弦波
            from mglearn.datasets import make_wave
            X_test, y_test = make_wave(n_samples = test_number)
            X_test, y_test = (np.array(t) for t in zip(*sorted(zip(X_test, y_test))))

            # # 准备测试数据，无噪声的正弦波
            # X_test = np.linspace(-3, 3, test_number).reshape(-1, 1)
            # y_test = np.sin(X_test)

            number_title = "{}个训练数据；{}个测试数据".format(train_number, test_number)
            print('-' * 5, number_title, '-' * 5)
            # 决策树预测
            from sklearn.tree import DecisionTreeRegressor
            reg_dtr = DecisionTreeRegressor(min_samples_split = 3)
            reg_dtr.fit(X_train, y_train)
            print("使用决策树预测的结果R^2评价 = {}".format(reg_dtr.score(X_test, y_test)))

            # 线性回归预测
            from sklearn.linear_model import LinearRegression
            reg_lr = LinearRegression().fit(X_train, y_train)
            print("使用线性回归预测的结果R^2评价 = {}".format(reg_lr.score(X_test, y_test)))

            # 画图
            plt.figure()
            plt.plot(X_test, reg_dtr.predict(X_test), label = '决策树')
            plt.plot(X_test, reg_lr.predict(X_test), label = '线性回归')
            plt.plot(X_train[:, 0], y_train, 'o', c = 'b')
            plt.plot(X_test[:, 0], y_test, '^', c = 'r')
            plt.xlabel('输入的特征')
            plt.ylabel('输出的回归')
            plt.legend(loc = 'best')
            plt.suptitle("图4-1：比较线性回归和决策树的预测效果\n"
                         "{}个训练数据；{}个测试数据".format(train_number, test_number))

            print()
            pass
        pass


# 使用特征分箱（binning，也叫离散化，discretization）可以让线性模型在连续数据上更强大
# 分箱的宽度，不同的宽度代表分类的数目，也是线性回归模型分类的精度，分类数目过高会造成过拟合
# 对于特定的数据集，如果数据集大、维度高，则可以使用线性模型，
# 但是某些特征与输出的关系是非线性的，就可以使用分箱提高建模能力
# 增加训练数据集的数目，可以提高模型的精度
def data_binning():
    for train_number in [100, 150, 200]:
        # 准备训练数据，有噪声的正弦波
        from mglearn.datasets import make_wave
        X_train, y_train = make_wave(n_samples = train_number)

        # # 准备训练数据，无噪声的正弦波
        # X_train = np.linspace(-3, 3, train_number).reshape(-1, 1)
        # y_train = np.sin(X_train)

        print('=' * 40)
        for test_number in [100, 150, 200]:
            # 准备测试数据，有噪声的正弦波
            from mglearn.datasets import make_wave
            X_test, y_test = make_wave(n_samples = test_number)
            X_test, y_test = (np.array(t) for t in zip(*sorted(zip(X_test, y_test))))

            # # 准备测试数据，无噪声的正弦波
            # X_test = np.linspace(-3, 3, test_number).reshape(-1, 1)
            # y_test = np.sin(X_test)

            for bin_number in [5, 10, 15]:
                print('=' * 40)
                number_title = "{}个训练数据；{}个测试数据；{}个箱子".format(train_number, test_number, bin_number)
                print('-' * 5, number_title, '-' * 5)
                print()
                # 将X_train的值与箱子的值对应，即将连续值离散化
                bins = np.linspace(-3, 3, bin_number)
                X_train_bin = np.digitize(X_train, bins = bins)

                print('-' * 5, "训练数据", '-' * 5)
                import random
                rand_train_number_list = random.sample(range(0, train_number), 10)
                print('十个原始的训练数据:', X_train[rand_train_number_list].T)
                print('十个分箱后的训练数据:', X_train_bin[rand_train_number_list].T)

                # 将离散化的训练数据使用 OneHotEncoder 进行编码
                from sklearn.preprocessing import OneHotEncoder
                encoder = OneHotEncoder(sparse = False, categories = 'auto')
                encoder.fit(X_train_bin)
                X_train_one_hot = encoder.transform(X_train_bin)
                print('-' * 5, "分箱后的训练数据使用OneHot编码", '-' * 5)
                print('使用OneHot编码的分箱后的训练数据的形状= {}'.format(X_train_one_hot.shape))
                # print('十个使用OneHot编码的分箱后的训练数据: \n', X_train_one_hot[rand_train_number_list])

                # 将X_test的值与箱子的值对应，即将连续值离散化
                X_test_bin = np.digitize(X_test, bins = bins)
                print('-' * 5, "测试数据", '-' * 5)
                import random
                rand_train_number_list = random.sample(range(0, test_number), 10)
                print('十个原始的测试数据:', X_test[rand_train_number_list].T)
                print('十个分箱后的测试数据:', X_test_bin[rand_train_number_list].T)

                # 将离散化的测试数据使用 OneHotEncoder 进行编码
                # 必须使用训练数据集的编码器来编码，不能再训练一次
                X_test_one_hot = encoder.transform(X_test_bin)
                print('-' * 5, "分箱后的训练数据使用OneHot编码", '-' * 5)
                print('使用OneHot编码的分箱后的训练数据的形状= {}'.format(X_test_one_hot.shape))
                # print('十个使用OneHot编码的分箱后的训练数据: \n', X_test_one_hot[rand_train_number_list].T)

                print('-' * 40)
                # 决策树预测
                from sklearn.tree import DecisionTreeRegressor
                reg_dtr = DecisionTreeRegressor(min_samples_split = 3)
                reg_dtr.fit(X_train_one_hot, y_train)
                print("使用决策树预测的结果R^2评价 = {}".format(reg_dtr.score(X_test_one_hot, y_test)))

                # 线性回归预测
                from sklearn.linear_model import LinearRegression
                reg_lr = LinearRegression().fit(X_train_one_hot, y_train)
                print("使用线性回归预测的结果R^2评价 = {}".format(reg_lr.score(X_test_one_hot, y_test)))

                # 绘制数据点
                plt.figure()
                plt.plot(X_test, reg_dtr.predict(X_test_one_hot), label = '决策树')
                plt.plot(X_test, reg_lr.predict(X_test_one_hot), label = '线性回归')
                plt.plot(X_train[:, 0], y_train, 'o', c = 'b')
                plt.plot(X_test[:, 0], y_test, '^', c = 'r')
                plt.xlabel('输入的特征')
                plt.ylabel('输出的回归')
                plt.legend(loc = 'best')
                plt.suptitle("图4-2：在分箱特征上比较线性回归和决策树回归\n" + number_title)

                print()
                pass
            pass


if __name__ == "__main__":
    # 图4-1：比较线性回归和决策树
    # compare_linear_model_decision_tree()

    # 使用特征分箱（binning，也叫离散化，discretization）可以让线性模型在连续数据上更强大
    data_binning()
    import winsound

    # 运行结束的提醒
    winsound.Beep(600, 500)
    if len(plt.get_fignums()) != 0:
        plt.show()
    pass