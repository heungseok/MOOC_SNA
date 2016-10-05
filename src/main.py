# -*- coding: utf-8 -*-
import load_data2 as data_import
import load_currentCourseData as origin_platform
import load_QSRankingData as qs_rankings
import myGraph as mGraph
import pandas as pd
# import keywordGraph as keyword_graph
# from courseGraph import *
from igraph import *



# load and init data
data_import.load_courseData()
data_import.load_reviewData()

data_import.load_instructorData()
data_import.set_instructorsData_toXTData()

print "finished load data"
# load courses' data from origin platform(edX, Coursera),
# and adjust variables(price, subject, level, num_school, school_set)
coursera = origin_platform.load_coursera_course()
edx = origin_platform.load_edX_course()
data_import.adjust_courseData(coursera, edx)
print "finished adjust all data"

# load QS-world univ ranking data(overall, by subject),
# and set ranking values to school's variable according to time
overall_rankings = qs_rankings.load_qsRankingData()
subject_rankings = qs_rankings.load_qsRankingData_bySubject()

data_import.assign_rankingsData(overall_rankings, subject_rankings)

print "finished load ranking data, and also assign the data to origin data"

# assign global list from the load_data module
courseList = data_import.courseList
reviewList = data_import.reviewList
instructorList = data_import.instructorList

# clean previous lists
data_import.courseList = []
data_import.reviewList = []
data_import.instructorList = []

print "size of courseList " + str(len(courseList))
print "size of reviewList " + str(len(reviewList))

# for course in courseList:
#     print course.title, course.subject.name, course.time_from, course.institutions[0]['Name'], course.institutions[0]['Ranking'],  course.institutions[0]['SubjectRanking'], course.institutions[0]['Region'], course.institutions[0]['Year']
#

# time series list
timeList = []

# This for-loop is for load_data2
for course in courseList:
    # for time in course.time:
    if course.time in timeList:
        pass
    else:
        timeList.append(course.time)
#
# print timeList
#
def extract_course_review_connection(time):
    graph = mGraph.Graph()
    vertex_id = 0
    for course in courseList:
        # print time, course.time
        if str(course.time) == str(time):
            course_vertex = mGraph.Vertex(0, course.url, course.title, vertex_id)
            if graph.add_vertex(course_vertex):
                vertex_id += 1

            for review in reviewList:# 분석 대상이 course이므로 time과 edge가 형성이 되는 조건이 들어 맞을 경우에만 review vertex 생성.
                if str(review.time) == str(time):
                    if review.course_title == course.title and review.course_platform == course.platform:
                        reviewer_vertex = mGraph.Vertex(1, review.reviewer_id, review.reviewer_id, vertex_id)
                        if graph.add_vertex(reviewer_vertex):
                            vertex_id += 1

                        graph.add_edge(mGraph.Edge(graph.get_vertex_by_url(course.url),
                                              graph.get_vertex_by_url(review.reviewer_id)))

    vertex_type_list = graph.get_vertex_typeList()
    edge_tuple_list = graph.get_edge_tupleList()
    # print vertex_type_list
    # print edge_tuple_list
    g = Graph.Bipartite(vertex_type_list, edge_tuple_list)
    g.vs["url"] = graph.get_vertex_urlList()
    g.vs["label"] = graph.get_vertex_titleList()

    # vertex attribute add, 1_label is type1's label(subject-side) and 0_label is type0's label(keyword-side)
    # g.vs["1_label"] = graph.get_vertex_title_by_type(1)
    # g.vs["0_label"] = graph.get_vertex_title_by_type(0)

    # plot(g)
    print "get incidence matrix from bipartite network"
    # will print matrix (list of rows)
    # print g.get_incidence()[0]
    # will print column indices (list of rows)
    # print g.get_incidence()[1]
    # print g.vs['1_label']
    # print g.vs['0_label']

    return g


def extract_course_keyword_connection(time):
    graph = mGraph.Graph()
    vertex_id = 0
    for course in courseList:
        if str(course.time) == str(time):
            course_vertex = mGraph.Vertex(1, course.url, course.title, vertex_id)
            if graph.add_vertex(course_vertex):
                vertex_id += 1

            for keyword in course.keywords:
                keyword_vertex = mGraph.Vertex(0, keyword.name, keyword.name, vertex_id)
                if graph.add_vertex(keyword_vertex):
                    vertex_id += 1

                graph.add_edge(mGraph.Edge(graph.get_vertex_by_url(course.url),
                                          graph.get_vertex_by_url(keyword.name)))

    vertex_type_list = graph.get_vertex_typeList()
    edge_tuple_list = graph.get_edge_tupleList()
    # print vertex_type_list
    # print edge_tuple_list
    g = Graph.Bipartite(vertex_type_list, edge_tuple_list)
    g.vs["url"] = graph.get_vertex_urlList()
    g.vs["label"] = graph.get_vertex_titleList()

    # vertex attribute add, 1_label is type1's label(subject-side) and 0_label is type0's label(keyword-side)
    # g.vs["1_label"] = graph.get_vertex_title_by_type(1)
    # g.vs["0_label"] = graph.get_vertex_title_by_type(0)

    # plot(g)
    # print "get incidence matrix from bipartite network"
    # will print matrix (list of rows)
    # print g.get_incidence()[0]
    # will print column indices (list of rows)
    # print g.get_incidence()[1]
    # print g.vs['1_label']
    # print g.vs['0_label']

    return g



# extract subject keyword connection and bipartite network composed with subject-side and keyword-side
def extract_subject_keyword_connection(time):
    graph = mGraph.Graph()
    vertex_id = 0
    dic_subject_keywords = {}
    for index, course in enumerate(courseList):
        if str(course.time) == str(time):

            # for adding subject in graph type '1' (subject-side)
            subject_vertex = mGraph.Vertex(1, course.subject.name, course.subject.name, vertex_id)
            if graph.add_vertex(subject_vertex):
                vertex_id += 1

            # for adding subject in dictionary
            if course.subject.name not in dic_subject_keywords.keys():
                dic_subject_keywords[course.subject.name] = []

            for keyword in course.keywords:
                # for adding keyword in graph (bipartite) type 0 (keyword-side)
                keyword_vertex = mGraph.Vertex(0, keyword.name, keyword.name, vertex_id)
                if graph.add_vertex(keyword_vertex):
                    vertex_id += 1

                # for adding keyword in subject-keyword dictionary
                if keyword.name not in dic_subject_keywords[course.subject.name]:
                    dic_subject_keywords[course.subject.name].append(keyword.name)

                graph.add_edge(mGraph.Edge(graph.get_vertex_by_url(course.subject.name),
                                           graph.get_vertex_by_url(keyword.name)))


    # set keyword num of the subject of origin course data
    for subject in dic_subject_keywords.keys():
        # keyword_num = len(dic_subject_keywords.get(subject))
        # print subject, keyword_num
        for index, course in enumerate(courseList):
            if str(course.time) == str(time) and str(course.subject.name) == str(subject):
                courseList[index].subject.set_keywords(dic_subject_keywords.get(subject))
                print courseList[index].subject.keywords

    vertex_type_list = graph.get_vertex_typeList()
    edge_tuple_list = graph.get_edge_tupleList()
    # print vertex_type_list
    # print edge_tuple_list
    g = Graph.Bipartite(vertex_type_list, edge_tuple_list)
    g.vs["url"] = graph.get_vertex_urlList()
    g.vs["label"] = graph.get_vertex_titleList()

    # vertex attribute add, 1_label is type1's label(subject-side) and 0_label is type0's label(keyword-side)
    g.vs["1_label"] = graph.get_vertex_title_by_type(1)
    g.vs["0_label"] = graph.get_vertex_title_by_type(0)

    # plot(g)
    # print "get incidence matrix from bipartite network"
    # will print matrix (list of rows)
    # print g.get_incidence()[0]
    # will print column indices (list of rows)
    # print g.get_incidence()[1]
    # print g.vs['1_label']
    # print g.vs['0_label']

    return g



def one_mode_projection(origin_graph, type):

    projected_course_graph = origin_graph.bipartite_projection(which=type)

    # print "size of the projected graph's nodes - " + str(len(projected_course_graph.vs))
    # print "size of the projected graph's edges - " + str(len(projected_course_graph.es))

    projected_course_graph.vs["degree"] = projected_course_graph.degree()
    projected_course_graph.vs["betweenness"] = projected_course_graph.betweenness()
    projected_course_graph.vs["closeness"] = projected_course_graph.closeness()
    projected_course_graph.vs["eigen"] = projected_course_graph.evcent(directed=False)

    return projected_course_graph


# assign network attributes to courseList data.
def assign_centrality_to_origin_data(coreview_graph, cokeyword_graph, cosubject_graph, cokeyword_graph_by_subject, time):
    for index, course in enumerate(courseList):
        if str(course.time) == str(time):
            # set the attributes to each network
            # to coreview network
            for v1 in coreview_graph.vs:
                if str(v1['url']) == str(course.url):
                    courseList[index].assign_network_attr(v1['degree'], v1['betweenness'],
                                                          v1['closeness'], v1['eigen'])
            # to cokeyword network
            for v2 in cokeyword_graph.vs:
                for k_index, keyword in enumerate(course.keywords):
                    if str(v2['url']) == str(keyword.name):
                        courseList[index].keywords[k_index].assign_network_attr(
                            v2['degree'], v2['betweenness'], v2['closeness'], v2['eigen'])

            # to cosubject network
            for v3 in cosubject_graph.vs:
                if str(v3['url']) == str(course.subject.name):
                    courseList[index].subject.assign_network_attr(
                        v3['degree'], v3['betweenness'], v3['closeness'], v3['eigen'])

            # to cokeyword network by subject
            # especially, assign sum of the connected keywords' attributes to each subject of the course at the time
            for v4 in cokeyword_graph_by_subject.vs:
                if str(v4['url']) in course.subject.keywords:
                    degree_sum = float(v4['degree'])
                    bet_sum = float(v4['betweenness'])
                    close_sum = float(v4['closeness'])
                    eigen_sum = float(v4['eigen'])
                    total = degree_sum + bet_sum + close_sum + eigen_sum
                    course.subject.set_sum_of_keywords(total)


def write_adjacency_matrix(network):
    print "get adjacency matrix from bipartite network"
    file_name = "adjacency_matrix.csv"
    print network.get_adjacency(attribute="weight")
    print "test"
    print network.get_adjacency(attribute="weight").data

    df_from_network = pd.DataFrame(network.get_adjacency(attribute='weight').data,
                                   columns=network.vs['label'], index=network.vs['label'])
    # df_from_network.to_csv(file_name, sep='\t', encoding='utf-8')


# Need to adjust array of labels in network object.. DON'T USE now
def write_incidence_matrix(network):
    print "get incidence matrix from bipartite network"
    file_name = "incidence_matrix.csv"

    # the incidence matrix and two lists in a triplet.
    # The first list defines the mapping between row indices of the matrix and the original vertex IDs.
    # The second list is the same for the column indices.
    # Thus, when accesing the return values to get incidence matrix only, we need to access to the first list. such as network.get_incidence()[0]
    df_from_network = pd.DataFrame(network.get_incidence()[0],
                                   columns=list(set(network.vs['1_label'])), index=list(set(network.vs['0_label'])))
    df_from_network.to_csv(file_name, sep='\t', encoding='utf-8')


# TESTING CODE
# course_review_graph = extract_course_review_connection(9)
# coreview_graph = one_mode_projection(course_review_graph)
# print coreview_graph
# layout = coreview_graph.layout("kk")
# plot(coreview_graph, layout = layout)
#
# course_keyword_graph = extract_course_keyword_connection(9)
# cokeyword_graph = one_mode_projection(course_keyword_graph)
#
# print cokeyword_graph
# layout = cokeyword_graph.layout("kk")
# plot(cokeyword_graph, layout = layout)
#
# course_review_graph = extract_course_review_connection(8)
# coreview_graph = one_mode_projection(course_review_graph)
# print coreview_graph
# layout = coreview_graph.layout("kk")
# plot(coreview_graph, layout = layout)
#
# course_keyword_graph = extract_course_keyword_connection(8)
# cokeyword_graph = one_mode_projection(course_keyword_graph)
#
# print cokeyword_graph
# layout = cokeyword_graph.layout("kk")
# plot(cokeyword_graph, layout = layout)


# subject_keyword_graph = extract_subject_keyword_connection(8)
# # write_incidence_matrix(subject_keyword_graph)
# # vertex attribute add, 1_label is type1's label(subject-side) and 0_label is type0's label(keyword-side)
#
#
# cosubject_graph = one_mode_projection(subject_keyword_graph, 1)
#
# print "################# subjectNode list in co_subject_graph #################"
# print cosubject_graph.vs["1_label"]
# print "################# keyword list in co_subject_graph #################"
# print cosubject_graph.vs["0_label"]
#


# write_adjacency_matrix(cosubject_graph)

# cokeyword_graph = one_mode_projection(subject_keyword_graph, 0)
# print "################# subjectNode list in cokeyword_graph #################"
# print cosubject_graph.vs["1_label"]
# print "################# keyword list in cokeyword_graph #################"
# print cosubject_graph.vs["0_label"]

# write_adjacency_matrix(cokeyword_graph)


# make subject-keyword bipartite network,
# do projection to each side(subject-side, keyword-side)
print "################# start network construction #################"
subject_keyword_graph = extract_subject_keyword_connection(15)

cosubject_graph = one_mode_projection(subject_keyword_graph, 0)
cokeyword_graph_by_subject = one_mode_projection(subject_keyword_graph, 1)
print "################# co_subject_graph #################"
print cosubject_graph
print "################# co_keyword_graph (BY Subject) #################"
print cokeyword_graph_by_subject


# make course-review bipartite network, and course-keyword bipartite network.
# do projection to course side(at co-review network) and to keyword side(at co-keyword network)
course_review_graph = extract_course_review_connection(15)
coreview_graph = one_mode_projection(course_review_graph, 0)
print "################# co_subject_graph #################"
print coreview_graph
course_keyword_graph = extract_course_keyword_connection(15)
cokeyword_graph_by_course = one_mode_projection(course_keyword_graph, 0)
print "################# co_keyword_graph (BY Course) #################"
print cokeyword_graph_by_course

# need to assign keyword size of each subject according to time
# and assign sum of all keywords' centrality to subject according to time
assign_centrality_to_origin_data(coreview_graph, cokeyword_graph_by_course
                                 , cosubject_graph, cokeyword_graph_by_subject, 15)






#
# for time in timeList:
# for time in range(5):
#
#     # make subject-keyword bipartite network,
#     # do projection to each side(subject-side, keyword-side)
#     subject_keyword_graph = extract_subject_keyword_connection(time)
#
#     cosubject_graph = one_mode_projection(subject_keyword_graph, 0)
#     cokeyword_graph_by_subject = one_mode_projection(subject_keyword_graph, 1)
#     print "################# co_subject_graph #################"
#     print cosubject_graph
#     print "################# co_keyword_graph (BY Subject) #################"
#     print cokeyword_graph_by_subject
#
#
#     # make course-review bipartite network, and course-keyword bipartite network.
#     # do projection to course side(at co-review network) and to keyword side(at co-keyword network)
#     course_review_graph = extract_course_review_connection(time)
#     coreview_graph = one_mode_projection(course_review_graph, 0)
#     print "################# co_subject_graph #################"
#     print coreview_graph
#     course_keyword_graph = extract_course_keyword_connection(time)
#     cokeyword_graph_by_course = one_mode_projection(course_keyword_graph, 0)
#     print "################# co_keyword_graph (BY Course) #################"
#     print cokeyword_graph_by_course
#
#     # need to assign keyword size of each subject according to time
#     # and assign sum of all keywords' centrality to subject according to time
#     assign_centrality_to_origin_data(coreview_graph, cokeyword_graph_by_course
#                                      , cosubject_graph, cokeyword_graph_by_subject, time)
#
# print "end of calculation for network attr"
#
