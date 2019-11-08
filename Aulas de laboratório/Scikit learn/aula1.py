# 2017100230@[~]: /opt/anaconda3/bin/python3.7
# Python 3.7.3 (default, Mar 27 2019, 22:11:17) 
# [GCC 7.3.0] :: Anaconda, Inc. on linux
# Type "help", "copyright", "credits" or "license" for more information.
# >>> import numpy as np
# >>> from sklearn import datasets
# >>> iris = datasets.load_iris()
# >>> iris.data
# >>> iris.target
# >>> iris.data.shape
# >>> np.random.seed(0)
# >>> idx = np.random.permutation(len(iris_X))
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# NameError: name 'iris_X' is not defined
# >>> idx = np.random.permutation(len(iris.data))
# >>> idx
# array([114,  62,  33, 107,   7, 100,  40,  86,  76,  71, 134,  51,  73,
#         54,  63,  37,  78,  90,  45,  16, 121,  66,  24,   8, 126,  22,
#         44,  97,  93,  26, 137,  84,  27, 127, 132,  59,  18,  83,  61,
#         92, 112,   2, 141,  43,  10,  60, 116, 144, 119, 108,  69, 135,
#         56,  80, 123, 133, 106, 146,  50, 147,  85,  30, 101,  94,  64,
#         89,  91, 125,  48,  13, 111,  95,  20,  15,  52,   3, 149,  98,
#          6,  68, 109,  96,  12, 102, 120, 104, 128,  46,  11, 110, 124,
#         41, 148,   1, 113, 139,  42,   4, 129,  17,  38,   5,  53, 143,
#        105,   0,  34,  28,  55,  75,  35,  23,  74,  31, 118,  57, 131,
#         65,  32, 138,  14, 122,  19,  29, 130,  49, 136,  99,  82,  79,
#        115, 145,  72,  77,  25,  81, 140, 142,  39,  58,  88,  70,  87,
#         36,  21,   9, 103,  67, 117,  47])
# >>> iris_x = iris.data
# >>> iris_y = iris.target
# >>> idx = np.random.permutation(len(iris_x))
# >>> np.unique(iris_y)
# array([0, 1, 2])
# >>> 
# >>> iris_x_train = iris_x[idx[:-10]]
# >>> iris_y_train = iris_y[idx[:-10]]
# >>> iris_x_test = iris_x[idx[-10]]
# >>> iris_y_test = iris_y[idx[-10]]
# >>> from sklearn.neighbors import KNeighborsClassifier

# https://scikit-learn.org/stable/user_guide.html