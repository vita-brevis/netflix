class CException(Exception):
    message = ''
    err_no = -1

    def __init__(self, err_no, message=''):
        self.err_no = err_no
        self.message = message

    def __str__(self):
        if self.message == '':
            return ('An Unknown C exception occurred! Error: {}'
                    .format(self.err_no))
        else:
            return '{}. (Error {})'.format(self.message, self.err_no)


def c_svd_update_feature(train_points, users, user_offsets, movies, residuals,
                         movie_averages, feature, num_features, learn_rate, k_factor):
    import ctypes
    from ctypes import c_void_p, c_int32, c_float
    import os
    from utils.data_paths import LIBRARY_DIR_PATH
    num_train_points = train_points.shape[0]
    num_users = users.shape[0]
    num_movies = movies.shape[0]
    library_file_name = 'svd.so'
    library_file_path = os.path.join(LIBRARY_DIR_PATH, library_file_name)
    svd_lib = ctypes.cdll.LoadLibrary(library_file_path)
#    svd_lib.c_update_feature.argtypes = [c_void_p, c_int32, c_void_p, c_void_p, c_int32, c_void_p,
#                                         c_void_p, c_int32, c_void_p, c_float, c_int32, c_int32]
#    svd_lib.c_update_feature.restype = c_int32
    c_update_feature = svd_lib.c_update_feature
    returned_value = c_update_feature(
        c_void_p(train_points.ctypes.data),    # (void*) train_points
        c_int32(num_train_points),             # (int)   num_train_points
        c_void_p(users.ctypes.data),           # (void*) users
        c_void_p(user_offsets.ctypes.data),    # (void*) user_offsets
        c_int32(num_users),                    # (int)   num_users
        c_void_p(movies.ctypes.data),          # (void*) movies
        c_void_p(movie_averages.ctypes.data),  # (void*) movie_averages
        c_int32(num_movies),                   # (int)   num_movies
        c_void_p(residuals.ctypes.data),       # (void*) residuals
        c_float(learn_rate),                   # (float) learn_rate
        c_int32(feature),                      # (int)   feature
        c_int32(num_features),                 # (int)   num_features
        c_float(k_factor)                      # (float) k_factor
    )
    if returned_value != 0:
        raise CException(returned_value)

def c_run_svd_plus_epoch(train_points, users, user_offsets, user_rating_count, movies, movie_averages,
                         movie_rating_count, similarity_matrix_rated, num_neighbors, nearest_neighbors_matrix,
                         implicit_preference, implicit_preference_sums, explicit_feedback, implicit_feedback,
                         num_features, offset_learn_rate, feature_learn_rate, feedback_learn_rate, offset_k_factor,
                         feature_k_factor, feedback_k_factor):
    import ctypes
    from ctypes import c_void_p, c_int32, c_float
    import os
    from utils.data_paths import LIBRARY_DIR_PATH
    num_train_points = train_points.shape[0]
    num_users = users.shape[0]
    num_movies = movies.shape[0]
    library_file_name = 'svd_plus.so'
    library_file_path = os.path.join(LIBRARY_DIR_PATH, library_file_name)
    svd_lib = ctypes.cdll.LoadLibrary(library_file_path)
#    svd_lib.c_update_feature.argtypes = [c_void_p, c_int32, c_void_p, c_void_p, c_int32, c_void_p,
#                                         c_void_p, c_int32, c_void_p, c_float, c_int32, c_int32]
#    svd_lib.c_update_feature.restype = c_int32
    c_svd_plus = svd_lib.c_svd_plus
    returned_value = c_svd_plus(
        c_void_p(train_points.ctypes.data),    # (void*) train_points
        c_int32(num_train_points),             # (int)   num_train_points
        c_void_p(users.ctypes.data),           # (void*) users
        c_void_p(user_offsets.ctypes.data),    # (void*) user_offsets
        c_void_p(user_rating_count.ctypes.data), # (void*) user_rating_count[]
        c_int32(num_users),                    # (int)   num_users
        c_void_p(movies.ctypes.data),          # (void*) movies
        c_void_p(movie_averages.ctypes.data),  # (void*) movie_averages
        c_void_p(movie_rating_count.ctypes.data), # (void*) movie_rating_count[]
        c_int32(num_movies),                   # (int)   num_movies
        c_void_p(similarity_matrix_rated.ctypes.data),    # (void*) similarity_matrix_rated
        c_int32(num_neighbors),
        c_void_p(nearest_neighbors_matrix.ctypes.data),
        c_void_p(implicit_preference.ctypes.data),
        c_void_p(implicit_preference_sums.ctypes.data),
        c_void_p(explicit_feedback.ctypes.data),
        c_void_p(implicit_feedback.ctypes.data),
        c_int32(num_features),
        c_float(offset_learn_rate),
        c_float(feature_learn_rate),
        c_float(feedback_learn_rate),
        c_float(offset_k_factor),
        c_float(feature_k_factor),
        c_float(feedback_k_factor)
    )
    if returned_value != 0:
        raise CException(returned_value)