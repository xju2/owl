# -*- coding: utf_8 -*-
from django.core.management.base import BaseCommand, CommandError
from sqlalchemy import create_engine
from django.conf import settings

import time
import pandas as pd


class Command(BaseCommand):
    args = "<file>"
    help = "Add Users from a text file"

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('No input file given')

        start_time = time.time()
        db_name = settings.DATABASES['default']['NAME']
        engine = create_engine('mysql+mysqldb://xju:1234@localhost/'+db_name+'?charset=utf8')
        input_name = args[0]

        df = pd.read_table(input_name, names=["user_id", "movie_id", "rate"])
        df.to_sql("movie_phantomrate", engine, flavor='mysql', if_exists='append',
                  index=False, chunksize=1000)
        self.stdout.write('time takes: %s seconds' % (time.time()-start_time))
