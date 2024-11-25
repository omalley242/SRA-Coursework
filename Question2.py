import random
import numpy as np
import networkx as nx

def generate_precedence_graph(precedences):
    graph = nx.DiGraph()
    graph.add_edges_from(precedences)
    return graph

def generate_initial_solution(precedences, num_jobs, f_initial=None):
    if f_initial:
        return f_initial
    
    if not precedences:
        return random.shuffle(list(range(1, num_jobs + 1)))
    
    graph = generate_precedence_graph(precedences)
    initial_solution = list(nx.topological_sort(graph))
    return initial_solution

def compute_tardiness(processing_times, due_dates, schedule):
    completion_times = np.zeros(len(schedule))
    for i, job in enumerate(schedule):
        if i > 0:
            completion_times[i] = completion_times[i - 1] + processing_times[job - 1]
        else:
            completion_times[i] = processing_times[job - 1]

    tardiness = sum(
        max(0, completion_times[i] - due_dates[job - 1]) 
        for i, job in enumerate(schedule)
    )
    return tardiness

def is_schedule_valid(schedule, precedences):
    job_indices = {job: i for i, job in enumerate(schedule)}
    for job1, job2 in precedences:
        if job_indices.get(job1, float('inf')) >= job_indices.get(job2, float('-inf')):
            return False
    return True

def tabu_search(processing_times, due_dates, precedences, K, L, tolerance):
    curr_schedule = generate_initial_solution(precedences, len(processing_times))
    best_schedule = curr_schedule
    best_tardiness = compute_tardiness(processing_times, due_dates, best_schedule)
    
    tabu_list = []
    for _ in range(K):
        neighbors = []
        for i in range(len(curr_schedule) - 1):
            neighbor = curr_schedule[:]
            
            neighbor[i], neighbor[i + 1] = neighbor[i + 1], neighbor[i]
            if is_schedule_valid(neighbor, precedences) and neighbor not in tabu_list:
                neighbors.append(neighbor)
        
        if neighbors:
            neighbors.sort(key=lambda n: compute_tardiness(processing_times, due_dates, n))
            best_neighbor = neighbors[0]
            best_neighbor_tardiness = compute_tardiness(processing_times, due_dates, best_neighbor)

            if best_neighbor_tardiness - best_tardiness <= tolerance:
                best_schedule = best_neighbor
                best_tardiness = best_neighbor_tardiness
            
            tabu_list.append(best_neighbor)
            if len(tabu_list) > L:
                tabu_list.pop(0)
            curr_schedule = best_neighbor
    
    return best_schedule, best_tardiness

processing_times = [3, 10, 2, 2, 5, 2, 14, 5, 6, 5, 5, 2, 3, 3, 5, 6, 6, 6, 2, 3, 2, 3, 14, 5, 18, 10, 2, 3, 6, 2, 10]
due_dates = [172, 82, 18, 61, 93, 71, 217, 295, 290, 287, 253, 307, 279, 73, 355, 34,
             233, 77, 88, 122, 71, 181, 340, 141, 209, 217, 256, 144, 307, 329, 269]
precedences = [(1, 31), (2, 1), (3, 8), (4, 3), (5, 2), (6, 16), (7, 6), (8, 7), (9, 8), (10, 9),
    (11, 1), (12, 5), (13, 12), (14, 13), (17, 15), (15, 11), (16, 5), (17, 16), (18, 17),
    (19, 18), (20, 19), (21, 18), (22, 21), (23, 22), (24, 5), (25, 24), (26, 25), (27, 26),
    (28, 26), (29, 27), (29, 28), (30, 4), (30, 10), (30, 14), (30, 20), (30, 23), (30, 29)]

#problem sheet example 5
# processing_times = [10, 7, 3]
# due_dates = [15,2,13]
# precedences = []

best_schedule, best_tardiness = tabu_search(processing_times, due_dates, precedences, K=1000, L=20, tolerance=10)
print(f"Best Schedule: {best_schedule}")
print(f"Best Total Tardiness: {best_tardiness}")
