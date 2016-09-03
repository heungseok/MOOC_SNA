# -*- coding: utf-8 -*-
import load_data2 as data_import
import myGraph as mGraph
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
    return graph

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
    return graph


def one_mode_projection(origin_graph):

    vertex_type_list = origin_graph.get_vertex_typeList()
    edge_tuple_list = origin_graph.get_edge_tupleList()
    # print vertex_type_list
    # print edge_tuple_list
    g = Graph.Bipartite(vertex_type_list, edge_tuple_list)
    g.vs["url"] = origin_graph.get_vertex_urlList()
    g.vs["label"] = origin_graph.get_vertex_titleList()
    projected_course_graph = g.bipartite_projection(which=0)

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

for time in timeList:
    course_review_graph = extract_course_review_connection(time)
    coreview_graph = one_mode_projection(course_review_graph)
    print coreview_graph
    course_keyword_graph = extract_course_keyword_connection(time)
    cokeyword_graph = one_mode_projection(course_keyword_graph)
    print cokeyword_graph

    assign_centrality_to_origin_data(coreview_graph, cokeyword_graph, time)

print "end of calculation for network attr"

