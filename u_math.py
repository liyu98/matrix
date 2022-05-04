import numpy as np

import numpy as np
from scipy.linalg import svd
import scipy.io as scio
import pandas as pd
#
# # 2-D array: 2 x 3
# two_dim_matrix_one = np.array([[3, 3, 2], [2, 3, -2]])
# # 2-D array: 3 x 2
# two_dim_matrix_two = np.array([[3, 2], [3, 3], [2, -2]])
#
# two_multi_res = np.dot(two_dim_matrix_one, two_dim_matrix_two)
# print('two_multi_res: %s' % (two_multi_res))
#
# # 1-D array
# one_dim_vec_one = np.array([1, 2, 3])
# one_dim_vec_two = np.array([4, 5, 6])
# one_result_res = np.dot(one_dim_vec_one, one_dim_vec_two)
# print('one_result_res: %s' % (one_result_res))
#
# # 矩阵转置
# A = np.mat([[3, 3, 2], [2, 3, -2]])
# print(A.T)
#
#
# two_multi_res = np.dot(two_dim_matrix_one, A.T)
# print('two_multi_res-2: %s' % (two_multi_res))
#
# """
# Singular Value Decomposition
# """
# # define a matrix
# X = np.array([[3, 3, 2], [2, 3, -2]])
# print(X)
# # perform SVD
# U, singular, V_transpose = svd(X)
# # print different components
# print("U:\n ", U)
# print("Singular array: \n", singular)
# print("V^{T}: \n",V_transpose)
#
# """
# Calculate Pseudo inverse
# """
# # inverse of singular matrix is just the reciprocal of each element
# singular_inv = 1.0 / singular
# # create m x n matrix of zeroes and put singular values in it
# s_inv = np.zeros(A.shape)
# s_inv[0][0] = singular_inv[0]
# s_inv[1][1] = singular_inv[1]
# # calculate pseudoinverse
# M = np.dot(np.dot(V_transpose.T, s_inv.T), U.T)
# print("M:\n", M)
#



dataFile = './face.mat'
data = scio.loadmat(dataFile)
print(type(data))
print(data)

print(data.keys())
print(data['id'])

#
# df = pd.DataFrame(data['Y'])
# print(df.head())
#
# df1 = pd.DataFrame(data['id'])
# print(df1.head())

