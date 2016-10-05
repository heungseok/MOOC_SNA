import csv
import load_data2
import main

with open('../data/XT_results.csv', 'wb') as csvfile:
    # url,title,platform,institution,subject,language,keywords,totalReviewCount,totalReviewValue,time,timeReviewCount,timeReviewValue
    fieldnames = ['index', 'course_url', 'course_title', 'platform', 'institution_size']

    max_school_len = 0
    for course in main.courseList:
        temp_length = len(course.institutions)
        if temp_length > max_school_len:
            max_school_len = temp_length

    for i in range(max_school_len):
        fieldnames.extend(['institution' + str(i+1) + '_name', 'institution' + str(i+1) + '_region',
                           'institution' + str(i+1) + '_ranking', 'institution' + str(i+1) + '_ranking_bySubject'])

    fieldnames.extend(['subject', 'num_of_connected_keywords', 'sum_of_attr_of_connected_keywords', 'language',
                  'avgEffortHours(perWeeks)', 'course_length', 'price', 'level',
                  'totalReviewCount', 'totalReviewValue', 'time', 'time_from', 'time_to', 'reviewCount', 'reviewValue',
                  'degree', 'closeness', 'betweenness', 'eigen',
                  'keyword1', 'k1_degree', 'k1_close', 'k1_bet', 'k1_eigen',
                  'keyword2', 'k2_degree', 'k2_close', 'k2_bet', 'k2_eigen',
                  'keyword3', 'k3_degree', 'k3_close', 'k3_bet', 'k3_eigen',
                  'keyword4', 'k4_degree', 'k4_close', 'k4_bet', 'k4_eigen',
                  'keyword5', 'k5_degree', 'k5_close', 'k5_bet', 'k5_eigen'])

    max_instructor_len = 0

    for course in main.courseList:
        temp_length = len(course.instructors)
        if temp_length > max_instructor_len:
            max_instructor_len = temp_length

    for i in range(max_instructor_len):
        fieldnames.extend(['instructor' + str(i+1) + '_name', 'instructor' + str(i+1) + '_bio',
                           'instructor' + str(i+1) + '_age', 'instructor' + str(i+1) + '_gender'])

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for index, course in enumerate(main.courseList):
        dict = {
            'index': index, 'course_url': course.url, 'course_title': course.title, 'platform': course.platform,
            'institution_size': len(course.institutions),
            'subject': course.subject.name, 'num_of_connected_keywords': course.subject.keywords_num,
            'sum_of_attr_of_connected_keywords': course.subject.sum_of_keywords_centrality, 'language': course.language,
            'avgEffortHours(perWeeks)': course.avgEffortHours, 'course_length': course.courseLength,
            'price': course.price, 'level': course.level,
            'totalReviewCount': course.totalReviewCount, 'totalReviewValue': course.totalReviewValue,
            'time': course.time, 'time_from': course.time_from.strftime("%Y-%m-%d"), 'time_to': course.time_to.strftime("%Y-%m-%d"),
            'reviewCount': course.timeReviewCount, 'reviewValue': course.timeReviewValue,
            'degree': course.degree, 'betweenness': course.bet, 'closeness': course.closeness, 'eigen': course.eigen
        }
        for i, institution in enumerate(course.institutions):
            dict.update({
                'institution' + str(i + 1) + "_name": institution['Name'],
                'institution' + str(i + 1) + "_region": institution['Region'],
                'institution' + str(i + 1) + "_ranking": institution['Ranking'],
                'institution' + str(i + 1) + "_ranking_bySubject": institution['SubjectRanking'],

            })

        for i, key in enumerate(course.keywords):
            dict.update({
                'keyword' + str(i + 1): key.name,
                'k' + str(i + 1) + '_degree': key.degree,
                'k' + str(i + 1) + '_bet': key.bet,
                'k' + str(i + 1) + '_close': key.closeness,
                'k' + str(i + 1) + '_eigen': key.eigen
            })

        # max_instructor_len
        for i, inst in enumerate(course.instructors):
            dict.update({
                'instructor' + str(i+1) + '_name': inst['Name'],
                'instructor' + str(i+1) + '_bio': inst['Bio'],
                'instructor' + str(i+1) + '_age': inst['Age'],
                'instructor' + str(i+1) + '_gender': inst['Gender']
            })

        writer.writerow(dict)
