import json
import csv

courseList = []
reviewList = []
instructorList = []

class Course():

    def __init__(self, url, title, platform, institution, subject, language, keywords, totalReviewCount, totalReviewValue):
        self.url = url
        self.title = title
        self.platform = platform
        self.institution = institution
        self.subject = subject
        self.language = language
        self.keywords = keywords
        self.totalReviewCount = totalReviewCount
        self.totalReviewValue = totalReviewValue
        self.time = []
        self.timeReviewCount = []
        self.timeReviewValue = []

    def appendTime(self, time, review_count, review_value):
        self.time.append(time)
        self.timeReviewCount.append(review_count)
        self.timeReviewValue.append(review_value)

def load_courseData():

    with open("CourseXTdata.csv", "rb") as csvfile:
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
            time = row[9]
            timeReviewCount = row[10]
            timeReviewValue = row[11]

            flag = False
            for index, course in enumerate(courseList):
                if course.url == url:
                    courseList[index].appendTime(time, timeReviewCount, timeReviewValue)
                    flag = True
                    break

            if flag:
                continue
            else:
                temp_course = Course(url, title, platform, institution, subject, language, keywords, totalReviewCount,
                        totalReviewValue)
                temp_course.appendTime(time, timeReviewCount, timeReviewValue)
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
    with open("reviewXTdata.csv","rb") as csvfile:
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



def load_instrutorData():
    with open("instructor_classfied.csv", "rb") as csvfile:
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

        for inst in instructorList:
            print inst.name
            print inst.course_list




# igraph code
# g = Graph()
# g.add_vertex(3)
# print(g)
