from sqlalchemy import create_engine
import pymysql
import pandas as pd
import numpy as np

def getTransformsList():
    engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/transform', echo=False)
    df = pd.read_sql("SELECT * FROM transforms", con=engine, index_col='id')
    return df


def getTransforms(id):
    engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/transform', echo=False)
    df = pd.read_sql("SELECT * FROM data WHERE transform_id=" + str(id) +
                     " ORDER BY id DESC LIMIT 300", con=engine, index_col='id')
    return df.sort_index()


def updateTransform(id, status, time_end):
    engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/transform', echo=False)
    engine.execute("UPDATE transforms SET status="+str(status)+", time_end="+str(time_end)+" WHERE id=" + str(id))


def updateAllTransform(df):
    engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/transform', echo=False)
    df.to_sql('transforms', con=engine, if_exists='append')


def getAllTransform():
    engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/transform', echo=False)
    return pd.read_sql('SELECT * FROM data', con=engine)


def getTestData(id):
    df = getTransforms(id)
    return np.hstack((df.iloc[-1].values,
           df.iloc[-100].values, df.iloc[-1].values - df.iloc[-100].values, df.iloc[-100:].mean(), df.iloc[-100:].std(),
           df.iloc[-200].values, df.iloc[-1].values - df.iloc[-200].values, df.iloc[-200:].mean(), df.iloc[-200:].std(),
           df.iloc[-300].values, df.iloc[-1].values - df.iloc[-300].values, df.iloc[-300:].mean(), df.iloc[-300:].std()))


def getTestDataAll():
    df = getAllTransform()
    result = []
    for rows in df.groupby('transform_id'):
        result.append(np.hstack((rows[1].iloc[-1].values,
           rows[1].iloc[-100].values, rows[1].iloc[-1].values - rows[1].iloc[-100].values, rows[1].iloc[-100:].mean(), rows[1].iloc[-100:].std(),
           rows[1].iloc[-200].values, rows[1].iloc[-1].values - rows[1].iloc[-200].values, rows[1].iloc[-200:].mean(), rows[1].iloc[-200:].std(),
           rows[1].iloc[-300].values, rows[1].iloc[-1].values - rows[1].iloc[-300].values, rows[1].iloc[-300:].mean(), rows[1].iloc[-300:].std())))
    return np.array(result)
