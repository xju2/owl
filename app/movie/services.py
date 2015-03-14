__author__ = 'xju'
import pandas as pd
from sqlalchemy import create_engine
from mlalgs.matrix.matrix_completion import SVDThreshold
from mlalgs.matrix.utils.pandas_utils import unpivot, add_row
from django.conf import settings


def train_user(current_user):

    movie_cut = 1000
    user_cut = 50
    db_name = settings.DATABASES['default']['NAME']
    engine = create_engine('mysql+mysqldb://xju:1234@localhost/'+db_name+'?charset=utf8')
    good_movie = pd.read_sql_query('select id from movie_movie where rated_users > ' +
                                   str(movie_cut), engine)
    good_user = pd.read_sql_query('select id from movie_phantomuser where watched_movies > ' +
                                  str(user_cut), engine)
    # add current user to the matrix
    add_row(good_user, [current_user.id])

    user_id_list = ""
    for ids in good_user['id'].values.tolist():
        user_id_list += str(ids) + ","
    movie_id_list = ""
    for ids in good_movie['id'].values.tolist():
        movie_id_list += str(ids) + ','

    good_rate = pd.read_sql_query('select user_id, movie_id, rate from movie_phantomrate where user_id in ('
                                  + user_id_list[:-1]+') and movie_id in ('+movie_id_list[:-1]+');', engine)
    # add current user's rate to the matrix
    for rate in current_user.movie_realrate_related.all():
        add_row(good_rate, [rate.user_id, rate.movie_id, rate.rate])

    matrix = good_rate.pivot(index='movie_id', columns='user_id', values='rate')
    svd_threshold = SVDThreshold()
    trained = svd_threshold.train(matrix)
    final_df = unpivot(trained, 'movie_id', 'user_id', 'rate')
    recommend_matrix = (final_df[final_df['user_id'] == current_user.id]).sort_index(by='rate')[-10:-1]
    return recommend_matrix['movie_id'].tolist()
