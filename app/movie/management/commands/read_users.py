# -*- coding: utf_8 -*-
from django.core.management.base import BaseCommand, CommandError
from sqlalchemy import create_engine
from django.conf import settings
import pandas as pd
import numpy as np


class Command(BaseCommand):
    args = "<file>"
    help = "Add Users from a text file"

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('No input file given')
        if len(args) == 0:
            raise CommandError('No input file given')
        db_name = settings.DATABASES['default']['NAME']
        engine = create_engine('mysql+mysqldb://xju:1234@localhost/'+db_name+'?charset=utf8')
        input_name = args[0]
        df = pd.read_table(input_name, names=['id', 'name'],
                           dtype={'id': np.uint32, 'name': str}, skiprows=1)
        df['watched_movies'] = 0
        df.drop('name', axis=1).to_sql("movie_phantomuser", engine, flavor='mysql', if_exists='append',
                                       index=False, chunksize=1000)
        self.stdout.write('Successfully added %d users' % (df.shape[0]))
