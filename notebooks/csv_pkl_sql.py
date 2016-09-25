from api_keys import POSTGRES_PWD
import dill
import pandas as pd
from sqlalchemy import create_engine

def csv_it(dataframe, filebase):
    dataframe.to_csv('../csv/'+filebase+'.csv', sep=',', index=False, encoding='utf-8')
    return

def pkl_it(dataframe, filebase):
    with open('../pkl/'+filebase+'.pkl', 'w') as fh:
        dill.dump(dataframe, fh)

    return

def sql_it(dataframe, filebase, dbname='zika'):
    postgres_str = 'postgresql://mlgill:{}@127.0.0.1:5432/{}'.format(POSTGRES_PWD, dbname)
    engine = create_engine(postgres_str)
    dataframe.to_sql(filebase, engine, if_exists='replace')
    return

def save_it(dataframe, filebase, dbname='zika'):
    csv_it(dataframe, filebase)
    pkl_it(dataframe, filebase)
    sql_it(dataframe, 'sql_' + filebase, dbname=dbname)
    return
