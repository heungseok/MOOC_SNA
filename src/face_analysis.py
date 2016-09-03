import time
import requests
import operator
import numpy as np
import json
import csv

instructor_list = []

class Instructor():
    def __init__(self, course_id, course_title, name, bio, img_url):
        self.course_id = course_id
        self.course_title = course_title
        self.name = name
        self.bio = bio
        self.img_url = img_url
        self.gender = ""
        self.age = 0

    def set_gender(self, gender):
        self.gender = gender

    def set_age(self, age):
        self.age = age


with open("coursera_edx_course_20160822.csv", "rb") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] == 'course_id':
            continue
        course_id = row[0]
        title = row[2]
        instructor_name = row[10]
        instructor_bio = row[11]
        img_url = row[12]

        if instructor_name != "":
            instructor = Instructor(course_id, title, instructor_name, instructor_bio, img_url)
            instructor_list.append(instructor)
    print len(instructor_list)

_url = 'https://api.projectoxford.ai/face/v1.0/detect?returnFaceAttributes=age,gender'
_key = '9d4a02e7c88d40e08e5ab502ade75d34'
_maxNumRetries = 10

def processRequest(json, data, headers, params):
    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request('post', _url, json=json, data=data, headers=headers, params=params)

        if response.status_code == 429:

            print("Message: %s" % (response.json()['error']['message']))

            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content
        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()['error']['message']))

        break

    return result

# Face detection parameters
params = { 'returnFaceAttributes': 'age,gender',
           'returnFaceLandmarks': 'true'}

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/json'

# call face recognition API and, set instructors' age and gender
for index, inst in enumerate(instructor_list):

    json = { 'url': inst.img_url }
    print inst.img_url
    data = None
    result = processRequest( json, data, headers, params )
    if result is not None and len(result) > 0:
        gender = result[0]['faceAttributes']['gender']
        age = result[0]['faceAttributes']['age']
        print inst.name, gender, age

    else:
        gender = "none"
        age = 0

    instructor_list[index].set_gender(gender)
    instructor_list[index].set_age(float(age))
    time.sleep(5)

with open('instructor_classified.csv', 'wb') as csvfile:
    fieldnames = ['course_id','course_title', 'img_url', 'instructor_name', 'instructor_bio', 'gender','age']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for inst in instructor_list:
        writer.writerow({'course_id': inst.course_id, 'course_title': inst.course_title, 'img_url': inst.img_url,
                         'instructor_name': inst.name, 'instructor_bio': inst.bio,
                         'gender': inst.gender, 'age': str(inst.age)})