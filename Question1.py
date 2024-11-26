from WorkflowData import *

class LowestCostLast(Graph):
    
    workflow_graph: Graph
    due_dates: list[int]
    processing_times: list[int]
    total_processing_time: int = 0
    leaf_nodes: set = set()
    schedule: list = []

    def __init__(self, adj_matrix, due_dates, processing_times):
        self.workflow_graph = Graph(adj_matrix)
        self.due_dates = due_dates
        self.processing_times = processing_times
        self.find_total_processing_time()
        self.find_leaf_nodes()

    #
    def find_optimum(self):
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

        self.schedule.append(lowest_cost_leaf)
        self.workflow_graph.remove_node(lowest_cost_leaf)
        self.total_processing_time -= self.processing_times[lowest_cost_leaf]

    def compute_cost(self, node) -> int:
        due_date = self.due_dates[node]
        return max(0, self.total_processing_time - due_date)

lowest_cost_last = LowestCostLast(G, d, p)
lowest_cost_last.find_optimum()
