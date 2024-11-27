from WorkflowData import *

class LowestCostLast(Graph):
    
    workflow_graph: Graph
    due_dates: list[int]
    processing_times: list[int]
    total_processing_time: int = 0
    leaf_nodes: set = set()
    schedule: list = []

    def __init__(self, due_dates, processing_times):
        self.workflow_graph = None
        self.due_dates = due_dates
        self.processing_times = processing_times
        self.leaf_node = set()
        self.schedule = []
        self.total_processing_time = 0

    def add_graph(self, graph):
        self.workflow_graph = graph

    def add_graph_matrix(self, adj_matrix):
        self.workflow_graph = Graph()
        self.workflow_graph.add_matrix_edges(adj_matrix)

    def find_optimum(self):
        self.find_total_processing_time()
        self.find_leaf_nodes()
        while len(self.leaf_nodes) > 0:
            self.iterate_schedule()
            self.find_leaf_nodes()

    def find_leaf_nodes(self):
        self.leaf_nodes = set()
        for node, edges in self.workflow_graph.forward_dict.items():
            if len(edges) == 0:
                self.leaf_nodes.add(node)

    def find_total_processing_time(self):
        total = 0
        for time in self.processing_times:
            total += time
        self.total_processing_time = total

    def iterate_schedule(self):
        lowest_cost = None
        lowest_cost_leaf = None

        for leaf_node in self.leaf_nodes:
            cost = self.compute_cost(leaf_node)
            if lowest_cost == None or lowest_cost > cost:
                lowest_cost = cost
                lowest_cost_leaf = leaf_node

        self.schedule.insert(0, lowest_cost_leaf)
        self.workflow_graph.remove_node(lowest_cost_leaf)
        self.total_processing_time -= self.processing_times[lowest_cost_leaf]

    def compute_cost(self, node) -> int:
        due_date = self.due_dates[node]
        return max(0, self.total_processing_time - due_date)

if __name__ == '__main__':
    lowest_cost_last = LowestCostLast(d, p)
    graph = Graph()
    graph.add_matrix_edges(G)
    lowest_cost_last.add_graph(graph)
    lowest_cost_last.find_optimum()

    print([x+1 for x in lowest_cost_last.schedule])
