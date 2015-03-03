__author__ = 'xju'
from django.core.management.base import BaseCommand

import pandas as pd
from sqlalchemy import create_engine
from mlalgs.matrix.matrix_completion import SVDThreshold
from mlalgs.matrix.utils.pandas_utils import unpivot


class Command(BaseCommand):
    args = ""
    help = "Machine learning.."

    def handle(self, *args, **options):
        engine = create_engine('mysql+mysqldb://xju:1234@localhost/movies?charset=utf8')
        movie_cut = 100
        user_cut = 20
        print("movie cut: ", movie_cut)
        print("user cut: ", user_cut)
        good_movie = pd.read_sql_query('select id, name from recosys_movie where rated_users > ' +
                                       str(movie_cut), engine)
        good_user = pd.read_sql_query('select id, name from recosys_user where watched_movies > ' +
                                      str(user_cut), engine)
        user_id_list = ""
        for ids in good_user['id'].values.tolist():
            user_id_list += str(ids) + ","
        movie_id_list = ""
        for ids in good_movie['id'].values.tolist():
            movie_id_list += str(ids) + ','
        good_rate = pd.read_sql_query('select user_id, movie_id, rate from recosys_realrate where user_id in ('
                                      + user_id_list[:-1]+') and movie_id in ('+movie_id_list[:-1]+');', engine)
        matrix = good_rate.pivot(index='movie_id', columns='user_id', values='rate')
        svd_threshold = SVDThreshold()
        trained = svd_threshold.train(matrix)
        final_df = unpivot(trained)
        final_df.index.name = 'id'
        final_df.to_sql("recosys_suggestrate", engine, flavor="mysql",
                        if_exists='replace', index=True, chunksize=1000)
        self.stdout.write('Successfully updated suggested movies')
