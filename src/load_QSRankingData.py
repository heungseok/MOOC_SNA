import pandas as pd
import numpy as np


def load_qsRankingData():
    df = pd.read_csv('../data/QS_world_university_rankings_2012-2016.csv')
    # df = pd.read_csv('CourseXTdata.csv')
    # for i, row in df.iterrows():
    #     print 'title: ', row['title'], '/ subject: ', row['subject'], '/ price: ', row['price']

    return df

def load_qsRankingData_bySubject():
    df = pd.read_csv('../data/QS_world_university_rankings_By_Subjects_2013-2016.csv')
    # df = pd.read_csv('CourseXTdata.csv')
    # for i, row in df.iterrows():
    #     print 'title: ', row['title'], '/ subject: ', row['subject'], '/ price: ', row['price']

    return df

# df = load_qsRankingData()
# print df.head(10)
# df = load_qsRankingData_bySubject()
# print df.head(10)