# -*- coding: utf_8 -*-

from django.core.management.base import BaseCommand, CommandError
from sqlalchemy import create_engine
from django.conf import settings
import pandas as pd
import numpy as np


class Command(BaseCommand):
    args = '<file>'
    help = 'Add movies from a text file'

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('No input file given')
        db_name = settings.DATABASES['default']['NAME']
        engine = create_engine('mysql+mysqldb://xju:1234@localhost/'+db_name+'?charset=utf8')
        input_name = args[0]
        df = pd.read_table(input_name,
                           names=['id', 'name', 'avg_rate_site', 'publish_date', 'types',
                                  'publish_country', 'language', 'length', 'directors', 'actors'],
                           dtype={'id': np.int, 'name': str, 'avg_rate_site': np.float, 'publish_date': str})
        df['avg_rate_site'] *= 100
        df.index.name = 'id'
        df['rated_users'] = 0
        df.to_sql("movie_movie", engine, flavor='mysql', if_exists='append', index=False,
                  chunksize=1000)
        self.stdout.write('Successfully added %d movies' % (df.shape[0]))
