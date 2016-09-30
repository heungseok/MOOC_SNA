# -*- coding: utf-8 -*-
import load_data2 as data_import
import myGraph as mGraph
import pandas as pd
# import keywordGraph as keyword_graph
# from courseGraph import *
from igraph import *



# load and assign data
data_import.load_courseData()
data_import.load_reviewData()
data_import.load_instructorData()
data_import.set_instructorsData_toXTData()

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

# time series list
timeList = []

# This for-loop is for load_data2
for course in courseList:
    # for time in course.time:
    if course.time in timeList:
        pass
    else:
        timeList.append(course.time)

print timeList

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
    g.vs["1_label"] = graph.get_vertex_title_by_type(1)
    g.vs["0_label"] = graph.get_vertex_title_by_type(0)

    plot(g)
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
    g.vs["1_label"] = graph.get_vertex_title_by_type(1)
    g.vs["0_label"] = graph.get_vertex_title_by_type(0)

    plot(g)
    print "get incidence matrix from bipartite network"
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


    for subject in dic_subject_keywords.keys():
        keyword_num = len(dic_subject_keywords.get(subject))
        print subject, keyword_num

        for index, course in enumerate(courseList):
            if str(course.time) == str(time) and course.subject == subject:
                courseList[index].set_keyword_count(keyword_num)

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

    plot(g)
    print "get incidence matrix from bipartite network"
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

def assign_centrality_to_origin_data(coreview_graph, cokeyword_graph, time):
    for index, course in enumerate(courseList):
        if str(course.time) == str(time):
            for v1 in coreview_graph.vs:
                if str(v1['url']) == str(course.url):
                    courseList[index].assign_network_attr(v1['degree'], v1['betweenness'],
                                                          v1['closeness'], v1['eigen'])
            for v2 in cokeyword_graph.vs:
                for k_index, keyword in enumerate(course.keywords):
                    if str(v2['url']) == str(keyword.name):
                        courseList[index].keywords[k_index].assign_network_attr(
                            v2['degree'], v2['betweenness'], v2['closeness'], v2['eigen'])


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


# subject_keyword_graph = extract_subject_keyword_connection(5)
# write_incidence_matrix(subject_keyword_graph)

# cosubject_graph = one_mode_projection(subject_keyword_graph, 1)
# layout = cosubject_graph.layout("kk")
# write_adjacency_matrix(cosubject_graph)

# cokeyword_graph = one_mode_projection(subject_keyword_graph, 0)
# layout = cosubject_graph.layout("kk")
# write_adjacency_matrix(cokeyword_graph)



for time in timeList:

    # make subject-keyword bipartite network.
    subject_keyword_graph = extract_subject_keyword_connection(time)
    cosubject_graph = one_mode_projection(subject_keyword_graph, 0)
    cokeyword_graph_by_subject = one_mode_projection(subject_keyword_graph, 1)
    print cosubject_graph
    print cokeyword_graph_by_subject

    course_review_graph = extract_course_review_connection(time)
    coreview_graph = one_mode_projection(course_review_graph, 0)
    print coreview_graph
    course_keyword_graph = extract_course_keyword_connection(time)
    cokeyword_graph_by_course = one_mode_projection(course_keyword_graph, 0)
    print cokeyword_graph_by_course

    assign_centrality_to_origin_data(coreview_graph, cokeyword_graph_by_course, time)

print "end of calculation for network attr"

