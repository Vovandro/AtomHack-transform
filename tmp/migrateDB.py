import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pymysql
import os

files_test = []
for _, _, filenames in os.walk('./data_test'):
    for filename in filenames:
        if filename[-4:] == '.csv':
            files_test.append(filename)

engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/transform', echo=False)


for file in files_test:
    engine.execute("INSERT INTO transforms (name_transfomr,serial,status,time_end) VALUES ('" +
                   file[2:-4] + "', '-', 1, 1)")
    id = engine.execute("SELECT LAST_INSERT_ID()").fetchall()[0][0]

    df = pd.read_csv('./data_test/' + file)
    df['transform_id'] = id

    df.to_sql('data', con=engine, if_exists='append', index=False)