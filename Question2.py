import random
import networkx as nx
from WorkflowData import *
from Question1 import *
import copy

class TabuSearch(Graph):

    workflow_graph: Graph
    processing_times: list[int]
    due_dates: list[int]
    schedule: list[int]

    def __init__(self, processing_times, due_dates):
        self.workflow_graph = None
        self.due_dates = due_dates
        self.processing_times = processing_times
        self.best_schedule = []

    def add_precendences(self, adj_matrix):
        self.workflow_graph = Graph()
        self.workflow_graph.add_matrix_edges(adj_matrix)

    def generate_initial_solution(self, num_jobs, f_initial):
        if f_initial:
            return f_initial
        
        if not self.workflow_graph: #if no precendences are supplied
            return random.shuffle(list(range(1, num_jobs + 1)))
        
        LCL = LowestCostLast(self.due_dates,self.processing_times)
        graph_copy = Graph()
        graph_copy.forward_dict = copy.deepcopy(self.workflow_graph.forward_dict)
        graph_copy.backward_dict = copy.deepcopy(self.workflow_graph.backward_dict)
        LCL.add_graph(graph_copy)
        LCL.find_optimum()

        return LCL.schedule

    def valid_interchange(self, idx1, idx2):
        if ((self.workflow_graph.get_children(idx1) and idx2 in self.workflow_graph.get_children(idx1)) or
            (self.workflow_graph.get_children(idx2) and idx1 in self.workflow_graph.get_children(idx2))):
            return False
        return True

    def compute_tardiness(self, schedule):
        cumulative_time, tardiness_sum = 0, 0
        
        for job_index in schedule:
            cumulative_time += self.processing_times[job_index]
            job_tardiness = max(0, cumulative_time - self.due_dates[job_index])
            tardiness_sum += job_tardiness

        return tardiness_sum

    def tabu_search(self, K, L, tolerance, f_initial):
        curr_schedule = self.generate_initial_solution(len(self.processing_times), f_initial)
        self.best_schedule = curr_schedule[:]
        best_tardiness = self.compute_tardiness(self.best_schedule)

        tabu_list = []
        idx = 0

        for _ in range(K):
            neighbors = []
            size = len(curr_schedule)

            for i in range(idx, size-1):
                if self.valid_interchange(curr_schedule[i], curr_schedule[i+1]):
                    neighbor = curr_schedule[:]
                    temp = neighbor[i]
                    neighbor[i] = neighbor[i+1]
                    neighbor[i+1] = temp

                    to_append = (neighbor, (neighbor[i+1], neighbor[i]))
                    neighbors.append(to_append)
            for i in range(idx):
                if self.valid_interchange(curr_schedule[i], curr_schedule[i+1]):
                    neighbor = curr_schedule[:]
                    temp = neighbor[i]
                    neighbor[i] = neighbor[i+1]
                    neighbor[i+1] = temp

                    to_append = (neighbor, (neighbor[i+1], neighbor[i]))
                    neighbors.append(to_append)

            for neighbor, neighbor_change in neighbors:
                neighbor_cost = self.compute_tardiness(neighbor)

                if not sorted(neighbor_change) in tabu_list and neighbor_cost - best_tardiness <= tolerance:
                    curr_schedule = neighbor
                    current_cost = neighbor_cost

                    if len(tabu_list) >= L:
                        tabu_list.pop()
                    
                    sorted_neighbor_change = sorted(neighbor_change)
                    tabu_list.insert(0, sorted_neighbor_change)

                    idx = max(curr_schedule.index(sorted_neighbor_change[0]), curr_schedule.index(sorted_neighbor_change[1]))

                    if current_cost < best_tardiness:
                        self.best_schedule = curr_schedule[:]
                        best_tardiness = current_cost
                        #print(f"Iteration {iteration + 1}: Current Cost = {curr_schedule}, Current Solution = {best_tardiness}")

                    break
        updated_best_schedule = [x+1 for x in self.best_schedule]     
        return updated_best_schedule, best_tardiness


initial_solution = [29, 28, 22, 9, 8, 13, 12, 11, 3, 19, 21, 2, 26, 27, 7, 6, 
                    18, 20, 25, 17, 24, 16, 14, 5, 23, 15, 4, 10, 1, 0, 30]

length = [10, 20, 30]
gammas = [5, 10, 20, 30]

for l in length:
    tabu_search_class = TabuSearch(p, d)
    tabu_search_class.add_precendences(G)
    best_schedule, best_tardiness = tabu_search_class.tabu_search(
        K=1000, L=l, tolerance=5, f_initial=None
    )
    print(best_schedule)
    print(best_tardiness)
