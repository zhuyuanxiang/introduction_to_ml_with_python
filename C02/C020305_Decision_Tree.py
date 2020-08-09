# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   introduction_to_ml_with_python
@File       :   C020305_Decision_Tree.py
@Version    :   v0.1
@Time       :   2019-09-29 11:45
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《Python机器学习基础教程》, Sec020305，P54
@Desc       :   监督学习算法。决策树。使用CART算法实现。
"""

# Chap2 监督学习
import config
import matplotlib.pyplot as plt
import mglearn
import sklearn
import numpy as np
import pandas as pd


# 2.3.5. 决策树

def plot_feature_importance_cancer(model, dataset):
    n_features = dataset.data.shape[1]
    plt.barh(range(n_features), model.feature_importances_, align = 'center')
    plt.yticks(np.arange(n_features), dataset.feature_names)
    plt.xlabel('Feature importance')
    plt.ylabel('Feature')
    pass


# 分类和回归树(Classification and Regression Tree, CART)是一种通用的树生长算法。
def draw_decision_tree():
    mglearn.plots.plot_animal_tree()
    plt.suptitle("图2-22：区分几种动物的决策树")


# 使用决策树算法处理 iris 数据集
# 对树预剪枝，从而控制树的深度，可以防止过拟合，增加测试集的精度
# Scikit-Learn只实现了“预剪枝”，没有实现“后剪枝”。
# random_state表示决策树学习过程的随机性。
#   - 因为寻找最优决策树是NP-完全问题，因此无法保证选择的结果是最优决策树，
#   只能根据随机条件决策随机的选择过程，得出一个当前条件下最优的决策树。
#   - 设置这个值，是为了保证每次选择的结果相同。
#   - 具体说明可以参考下面的网址：
#       https://stackoverflow.com/questions/43321394/what-is-random-state-parameter-in-scikit-learn-tsne
#       https://scikit-learn.org/stable/modules/tree.html#tree
def train_decision_tree_with_iris():
    import graphviz
    from sklearn.model_selection import train_test_split
    iris = sklearn.datasets.load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
            iris.data, iris.target, stratify = iris.target, random_state = config.seed)
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.tree import export_graphviz
    # max_depth=2，4 时，测试集的精度最高，但是max_depth=4时训练集的精度过高（有过拟合的危险），因此建议选择2。
    for max_depth in [1, 2, 3, 4, 9]:
        tree = DecisionTreeClassifier(random_state = config.seed, max_depth = max_depth)
        tree.fit(X_train, y_train)

        print('=' * 20)
        print("-- Decision Tree max_depth = {} --".format(max_depth))
        print('Training set score: {:.3f}'.format(tree.score(X_train, y_train)))
        print('Test set score: {:.3f}'.format(tree.score(X_test, y_test)))

        print('Feature importance:\n{}'.format(tree.feature_importances_))
        plt.figure()
        plot_feature_importance_cancer(tree, iris)
        plt.suptitle("-- Decision Tree max_depth = {} --".format(max_depth))

        # 输出决策树到文件中，用于后期分析
        out_file = 'tree_{}.dot'.format(max_depth)
        export_graphviz(tree, out_file = out_file, impurity = False, filled = True,
                        feature_names = iris.feature_names, class_names = list(iris.target_names))

        # 打开文件中保存的决策树，并且显示为图形用于分析
        with open(out_file) as f:
            dot_graph = f.read()
        graph = graphviz.Source(dot_graph)
        graph.render('tree_{}'.format(max_depth))
        graph.view()
        pass
    pass


# 使用决策树算法处理 cancer 数据集
# 对树预剪枝，从而控制树的深度，可以防止过拟合，增加测试集的精度
# Scikit-Learn只实现了“预剪枝”，没有实现“后剪枝”。
def train_decision_tree_with_cancer():
    import graphviz
    # 完美地记住训练数据的所有标签，但是测试精度比线性模型要低，说明过拟合了。
    from sklearn.model_selection import train_test_split
    cancer = sklearn.datasets.load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
            cancer.data, cancer.target, stratify = cancer.target, random_state = config.seed)

    from sklearn.tree import DecisionTreeClassifier
    from sklearn.tree import export_graphviz
    # max_depth=4,5 时，测试集的精度最高，但是max_depth=5时训练集的精度过高（有过拟合的危险），因此建议选择4。
    for max_depth in [1, 3, 4, 5, 6, 9]:
        tree = DecisionTreeClassifier(random_state = config.seed, max_depth = max_depth)
        tree.fit(X_train, y_train)

        print('=' * 20)
        print("-- Decision Tree max_depth = {} --".format(max_depth))
        print('Training set score: {:.3f}'.format(tree.score(X_train, y_train)))
        print('Test set score: {:.3f}'.format(tree.score(X_test, y_test)))

        print('Feature importance:\n{}'.format(tree.feature_importances_))
        plt.figure()
        plot_feature_importance_cancer(tree, cancer)
        plt.suptitle("-- Decision Tree max_depth = {} --".format(max_depth))

        # 输出决策树到文件中，用于后期分析
        out_file = 'tree_{}.dot'.format(max_depth)
        export_graphviz(tree, out_file = out_file, impurity = False, filled = True,
                        feature_names = cancer.feature_names,
                        class_names = list(cancer.target_names))

        # 打开文件中保存的决策树，并且显示为图形用于分析
        with open(out_file) as f:
            dot_graph = f.read()
        graph = graphviz.Source(dot_graph)
        graph.render('tree_{}'.format(max_depth))
        graph.view()
        pass
    pass


# 4) 树的特征重要性
def plot_decision_tree_important_feature():
    # 将特征的重要性进行可视化，了解哪个特征最重要，哪些特征非常重要，哪些特征没有被考虑。
    from sklearn.model_selection import train_test_split
    cancer = sklearn.datasets.load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
            cancer.data, cancer.target, stratify = cancer.target, random_state = config.seed)

    from sklearn.tree import DecisionTreeClassifier
    tree = DecisionTreeClassifier(max_depth = 4, random_state = config.seed)
    tree.fit(X_train, y_train)
    print('Feature importance:\n{}'.format(tree.feature_importances_))
    plot_feature_importance_cancer(tree, cancer)
    plt.suptitle("图2-28：在 cancer 数据集上学到的决策树的特征重要性")


# 决策树学习非单调关系的数据集
def plot_tree_not_monotone():
    graph = mglearn.plots.plot_tree_not_monotone()
    graph.render('tree')
    graph.view()
    plt.suptitle("图2-29：在二维数据集上学到的决策树的决策边界\n"
                 "二维数据集（y轴上的特征与类别标签是非单调的关系）")
    # from IPython.display import display
    # display(graph)     # 无法显示出图形，只能输出类的名称


def show_ram_prices_log_scale():
    ram_prices = pd.read_csv('../data/ram_price.csv')
    # 使用对数坐标绘图时，x轴与y轴的线性关系很明显
    plt.semilogy(ram_prices.date, ram_prices.price)  # y轴是对数刻度
    plt.xlabel('Year')
    plt.ylabel('Price in $/MByte')
    plt.suptitle("图2-31：用对数坐标绘制RAM价格的历史发展")
    pass


def fit_decision_tree_regression():
    # 树模型完美的拟合了训练数据，但是无法预测测试数据；
    # 所有的树模型都有这个缺点：即树不能在训练数据的范围之外生成“新的”预测。
    # 线性模型无论对训练数据还是测试数据都给予了相对较好的预测结果。

    # 运行代码文件时，当前路径为代码文件当前位置
    ram_prices = pd.read_csv('../data/ram_price.csv')
    # 在Console中执行代码时，当前路径为项目的根目录
    # ram_prices = pd.read_csv('data/ram_price.csv')
    data_train = ram_prices[ram_prices.date < 2000]
    data_test = ram_prices[ram_prices.date >= 2000]

    X_train = data_train.date[:, np.newaxis]
    y_train = np.log(data_train.price)  # 对价格对对数

    from sklearn.tree import DecisionTreeRegressor
    from sklearn.linear_model import LinearRegression
    tree_regressor = DecisionTreeRegressor()
    tree_regressor.fit(X_train, y_train)
    linear_regression = LinearRegression().fit(X_train, y_train)

    # 为ram_prices.date增加一维数据，即如果是一维的数据，就变成了二维的数据
    X_all = ram_prices.date[:, np.newaxis]

    # 预测数据
    pred_tree_regressor = tree_regressor.predict(X_all)
    pred_linear_regression = linear_regression.predict(X_all)

    # 通过指数运算，将数据恢复原始尺度
    price_tree_regressor = np.exp(pred_tree_regressor)
    price_linear_regression = np.exp(pred_linear_regression)

    plt.semilogy(data_train.date, data_train.price, label = 'Training data')
    plt.semilogy(data_test.date, data_test.price, label = 'Test data')
    plt.semilogy(ram_prices.date, price_tree_regressor, label = 'Tree prediction')
    plt.semilogy(ram_prices.date, price_linear_regression, label = 'Linear prediction')
    plt.legend()
    plt.suptitle("图2-32：线性模型和回归树对RAM价格数据的预测结果对比")


if __name__ == "__main__":
    # 图2-22：区分几种动物的决策树
    # draw_decision_tree()

    # 使用决策树算法处理 iris 数据集
    # train_decision_tree_with_iris()

    # 使用决策树算法处理 cancer 数据集
    # train_decision_tree_with_cancer()

    # 4) 树的特征重要性
    # 前面已经实现了。这里只显示了 max_depth = 4 的情况，也是最优的特征选择系数。
    # plot_decision_tree_important_feature()

    # 决策树学习非单调关系的数据集
    # plot_tree_not_monotone()

    # 图2-31：用对数坐标绘制RAM价格的历史发展
    # show_ram_prices_log_scale()

    # 图2-32：线性模型和回归树对RAM价格数据的预测结果对比
    # fit_decision_tree_regression()

    import tools
    tools.beep_end()
    tools.show_figures()