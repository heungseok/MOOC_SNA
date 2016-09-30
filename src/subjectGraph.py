
class Vertex():
    def __init__(self, type, url, label, id):
        self.type = type
        self.url = url
        self.label = label
        self.id = id

class Edge():
    def __init__(self, source, target):
        self.source = source
        self.target = target

class Graph():
    def __init__(self):
        self.vertexList = []
        self.edgeList = []

    def check_vertex_exist(self, node):
        for v in self.vertexList:
            if v.url == node.url:
                return True
        return False

    def add_vertex(self, node):
        if self.check_vertex_exist(node):
            return False
        else:
            self.vertexList.append(node)
            return True

    def add_edge(self, edge):
        self.edgeList.append(edge)

    def get_vertex_by_url(self, url):
        for v in self.vertexList:
            if v.url == url:
                return v
        return False

    def get_vertex_typeList(self):
        type_list = []
        for v in self.vertexList:
            type_list.append(v.type)
        return type_list

    def get_vertex_urlList(self):
        url_list = []
        for v in self.vertexList:
            url_list.append(v.url)
        return url_list

    def get_vertex_titleList(self):
        title_list = []
        for v in self.vertexList:
            title_list.append(v.label)
        return title_list

    def get_edge_tupleList(self):
        tuple_list = []
        for e in self.edgeList:
            t = (e.source.id, e.target.id)
            tuple_list.append(t)
        return tuple_list

