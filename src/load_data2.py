import json
import csv
import pandas as pd
import numpy as np
import time
import datetime

courseList = []
reviewList = []
instructorList = []

class Keyword():
    def __init__(self, name):
        self.name = name
        self.degree = 0.0
        self.bet = 0.0
        self.closeness = 0.0
        self.eigen = 0.0

    def assign_network_attr(self, degree, bet, close, eigen):
        self.degree = degree
        self.bet = bet
        self.closeness = close
        self.eigen = eigen

class Subject():
    def __init__(self, name):
        self.name = name
        self.degree = 0.0
        self.bet = 0.0
        self.closeness = 0.0
        self.eigen = 0.0

        # sum of network attributes of connected keywords at same time by subject, and the number of connected keywords
        self.keywords = []
        self.sum_of_keywords_centrality = 0.0
        self.keywords_num = 0

    def assign_network_attr(self, degree, bet, close, eigen):
        self.degree = degree
        self.bet = bet
        self.closeness = close
        self.eigen = eigen

    def set_keywords(self, keywords):
        self.keywords = keywords
        self.keywords_num = len(keywords)

    def set_sum_of_keywords(self, sum):
        self.sum_of_keywords_centrality += sum


class Course():

    def __init__(self, url, title, platform, institution, subject, language, keywords,
                 totalReviewCount, totalReviewValue, avgEffortHours, courseLength, price, level, time, reviewCount,
                 reviewValue, time_from, time_to):

        self.url = url
        self.title = title
        self.platform = platform

        self.subject = Subject(subject)
        self.language = language
        self.keywords = []
        for k in keywords:
            keyword = Keyword(k)
            self.keywords.append(keyword)

        self.avgEffortHours = avgEffortHours
        self.courseLength = courseLength
        self.price = price
        self.level = level

        self.totalReviewCount = totalReviewCount
        self.totalReviewValue = totalReviewValue
        self.time = time
        self.timeReviewCount = reviewCount
        self.timeReviewValue = reviewValue
        self.time_from = time_from
        self.time_to = time_to

        self.degree = 0.0
        self.bet = 0.0
        self.closeness = 0.0
        self.eigen = 0.0

        self.instructors = []

        self.institutions = []
        self.set_institutions(institution)


    def assign_network_attr(self, degree, bet, close, eigen):
        self.degree = degree
        self.bet = bet
        self.closeness = close
        self.eigen = eigen

    def set_instructors(self, name, bio, age, gender):
        instructor = {'Name': name, 'Bio': bio, 'Age': age, 'Gender': gender}
        self.instructors.append(instructor)

    def set_institutions(self, name, overall_ranking=0, subject_ranking=0, region='null', year=0):
        flag = False
        for index, inst in enumerate(self.institutions):
            if inst['Name'] == name:
                self.institutions[index]['Ranking'] = overall_ranking
                self.institutions[index]['SubjectRanking'] = subject_ranking
                self.institutions[index]['Region'] = region
                self.institutions[index]['Year'] = year
                flag = True

        if flag is False:
            institution = {'Name': name, 'Region': region, 'Ranking': overall_ranking,
                           'SubjectRanking': subject_ranking, 'Year':year}
            self.institutions.append(institution)


def load_courseData():

    with open("../data/CourseXTdata_addTime.csv", "rb") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'url':
                continue
            url = row[0]
            title = row[1]
            platform = row[2]
            institution = row[3]
            subject = row[4]
            language = row[5]
            keywords = row[6].split(',')
            totalReviewCount = row[7]
            totalReviewValue = row[8]
            avgEffortHours = row[9]
            courseLength = row[10]
            price = row[11]
            level = row[12]
            time = row[13]
            timeReviewCount = row[14]
            timeReviewValue = row[15]

            time_from = datetime.datetime.strptime(row[16], "%Y-%m-%d")
            time_to = datetime.datetime.strptime(row[17], "%Y-%m-%d")


            temp_course = Course(url, title, platform, institution, subject, language, keywords, totalReviewCount,
                        totalReviewValue, avgEffortHours, courseLength, price, level, time, timeReviewCount, timeReviewValue, time_from, time_to)

            courseList.append(temp_course)

# "course_url","title","course_platform","review_platform","time","reviewr_id","review_date","review_value"
class Review():
    def __init__(self, course_url, course_title, course_platform, time, reviewer_id, review_date, review_value):
        self.course_url = course_url
        self.course_title = course_title
        self.course_platform = course_platform
        self.time = time
        self.reviewer_id = reviewer_id
        self.review_date = review_date
        self.review_value = review_value


def load_reviewData():
    with open("reviewXTdata.csv", "rb") as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if row[0] == 'course_url':
                continue
            course_url = row[0]
            course_title = row[1]
            course_platform = row[2]
            time = row[4]
            reviewer_id = row[5]
            review_date = row[6]
            review_value = row[7]
            review = Review(course_url, course_title, course_platform, time, reviewer_id, review_date, review_value)
            reviewList.append(review)


class Instructor():
    def __init__(self, name, bio, age, gender):
        self.name = name
        self.bio = bio
        self.age = age
        self.gender = gender
        self.course_list = []

    def add_course(self, course_title):
        self.course_list.append(course_title)


def load_instructorData():
    with open("instructor_classified.csv", "rb") as csvfile:
        reader = csv.reader(csvfile)
        # course_id,course_title,img_url,instructor_name,instructor_bio,gender,age
        for row in reader:
            if row[0] == 'course_id':
                continue
            course_id = row[0]
            course_title = row[1]
            img_url = row[2]
            instructor_name = row[3]
            instructor_bio = row[4]
            gender = row[5]
            age = row[6]
            flag = True
            for index, inst in enumerate(instructorList):
                if inst.name == instructor_name:
                    instructorList[index].add_course(course_title)
                    flag = False

            if flag:
                instructor = Instructor(instructor_name, instructor_bio, age, gender)
                instructor.add_course(course_title)
                instructorList.append(instructor)

        # for inst in instructorList:
        #     print inst.name
        #     print inst.course_list

def set_instructorsData_toXTData():
    for inst in instructorList:
        for index, course in enumerate(courseList):
            if course.title in inst.course_list:
                courseList[index].set_instructors(inst.name, inst.bio, inst.age, inst.gender)


def adjust_courseData(coursera, edx):
    # need to adjust variables (price, subject, level, num_school, school_set)
    # print coursera.head(10)
    for i, course in enumerate(courseList):
        row = coursera.loc[coursera['title'] == course.title]
        if row.empty:
            pass
        else:
            price = row.iloc[0]['price']
            subject = row.iloc[0]['subject']
            level = row.iloc[0]['level']
            num_school = row.iloc[0]['num_school']

            courseList[i].price = price
            courseList[i].level = level
            courseList[i].subject.name = subject
            for j in range(int(num_school)):
                school_index = 'school_' + str(j + 1)
                school = row.iloc[0][school_index]
                courseList[i].set_institutions(school)

            continue

        row = edx.loc[edx['title'] == edx.title]
        if row.empty:
            pass
        else:
            price = row.iloc[0]['price']
            subject = row.iloc[0]['subject']
            level = row.iloc[0]['level']
            num_school = row.iloc[0]['num_school']

            courseList[i].price = price
            courseList[i].level = level
            courseList[i].subject.name = subject
            for j in range(int(num_school)):
                school_index = 'school_' + str(j + 1)
                school = row.iloc[0][school_index]
                courseList[i].set_institutions(school)


def assign_rankingsData(overall_rankings, subject_rankings):
    for i, course in enumerate(courseList):
        for j, institution in enumerate(course.institutions):
            school_name = institution["Name"]
            course_year = course.time_from.year
            subject_name = course.subject.name

            row_overall = overall_rankings.loc[(overall_rankings['year'] == course_year) & (overall_rankings['univ_title'] == school_name)]
            row_subject = subject_rankings.loc[(subject_rankings['year'] == course_year) & (subject_rankings['univ_title'] == school_name) & (subject_rankings['subject'] == subject_name)]
            # institution = {'Name': name, 'Region': region, 'Ranking': overall_ranking, 'SubjectRanking': subject_ranking}
            if row_overall.empty:
                pass
            else:
                ranking = row_overall.iloc[0]['ranking']
                year = row_overall.iloc[0]['year']
                region = row_overall.iloc[0]['country']
                if row_subject.empty:
                    ranking_bySubject = 0
                else:
                    ranking_bySubject = row_subject.iloc[0]['ranking']

                courseList[i].set_institutions(school_name, ranking, ranking_bySubject, region, year)
