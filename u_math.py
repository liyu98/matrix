import numpy as np

# 2-D array: 2 x 3
two_dim_matrix_one = np.array([[3, 3, 2], [2, 3, -2]])
# 2-D array: 3 x 2
two_dim_matrix_two = np.array([[3, 2], [3, 3], [2, -2]])

two_multi_res = np.dot(two_dim_matrix_one, two_dim_matrix_two)
print('two_multi_res: %s' % (two_multi_res))

# 1-D array
one_dim_vec_one = np.array([1, 2, 3])
one_dim_vec_two = np.array([4, 5, 6])
one_result_res = np.dot(one_dim_vec_one, one_dim_vec_two)
print('one_result_res: %s' % (one_result_res))