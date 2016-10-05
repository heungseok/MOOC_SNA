# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

def load_edX_course():
    df = pd.read_csv('../data/edx_fill_null_with_price.csv', index_col="course_id")
    # df = pd.read_csv('CourseXTdata.csv')
    # for i, row in df.iterrows():
    #     print 'title: ', row['title'], '/ subject: ', row['subject'], '/ price: ', row['price']

    return df

def load_coursera_course():
    df = pd.read_csv("../data/coursera_fill_price_20160926_withoutDescription.csv", index_col="course_id")
    # for i, row in df.iterrows():
    #     if 'english' in str(row['language']).lower():
    #         print 'title: ', row['title'], '/ subject: ', row['subject'], '/ price: ', row['price_adjusted']
    return df

