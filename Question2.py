import random
import numpy as np
import networkx as nx

def generate_precedence_graph(precedences):
    graph = nx.DiGraph()
    graph.add_edges_from(precedences)
    return graph

def generate_initial_solution(precedences, num_jobs, f_initial):
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

def tabu_search_enhanced(processing_times, due_dates, precedences, K, L, tolerance, f_initial):
    curr_schedule = generate_initial_solution(precedences, len(processing_times), f_initial)
    best_schedule = curr_schedule[:]
    best_tardiness = compute_tardiness(processing_times, due_dates, best_schedule)

    tabu_list = []
    for _ in range(K):
        neighbors = []
        for i in range(len(curr_schedule)):
            for j in range(i + 1, len(curr_schedule)):  
                neighbor = curr_schedule[:]
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                
                if is_schedule_valid(neighbor, precedences) and neighbor not in tabu_list:
                    neighbors.append((neighbor, compute_tardiness(processing_times, due_dates, neighbor)))

        if neighbors:
            neighbors.sort(key=lambda x: x[1])
            best_neighbor, best_neighbor_tardiness = neighbors[0]

            if best_neighbor_tardiness <= best_tardiness:
                best_schedule = best_neighbor
                best_tardiness = best_neighbor_tardiness

            tabu_list.append(best_neighbor)
            if len(tabu_list) > L:
                tabu_list.pop(0)
                
            if best_neighbor_tardiness - best_tardiness < tolerance:
                curr_schedule = best_neighbor

    incremented_best_schedule = [x + 1 for x in best_schedule]

    return incremented_best_schedule, best_tardiness

processing_times = [3, 10, 2, 2, 5, 2, 14, 5, 6, 5, 5, 2, 3, 3, 5, 6, 6, 6, 2, 3, 2, 3, 14, 5, 18, 10, 2, 3, 6, 2, 10]
due_dates = [172, 82, 18, 61, 93, 71, 217, 295, 290, 287, 253, 307, 279, 73, 355, 34, 233, 77, 88, 122, 71, 181, 340, 141, 209, 217, 256, 144, 307, 329, 269]
precedences = [(0, 30), (1, 0), (2, 7), (3, 2), (4, 1), (5, 15), (6, 5), (7, 6), (8, 7), (9, 8),
    (10, 0), (11, 4), (12, 11), (13, 12), (16, 14), (14, 10), (15, 4), (16, 15), (17, 16),
    (18, 17), (19, 18), (20, 17), (21, 20), (22, 21), (23, 4), (24, 23), (25, 24), (26, 25),
    (27, 25), (28, 26), (28, 27), (29, 3), (29, 9), (29, 13), (29, 19), (29, 22), (29, 28)]

initial_solution = [29, 28, 22, 9, 8, 13, 12, 11, 3, 19, 21, 2, 26, 27, 7, 6, 
                    18, 20, 25, 17, 24, 16, 14, 5, 23, 15, 4, 10, 1, 0, 30]

Ls = [20]
tolerances = [15, 10, 5, 0]

best_sol = 400
for tolerance in tolerances:
    best_schedule, best_tardiness = tabu_search_enhanced(processing_times, due_dates, precedences, 1000, L=20, tolerance=tolerance, f_initial=None)
    if best_tardiness < best_sol:
        best_sol = best_tardiness
        print("tolerance: ", tolerance)
        print(best_sol)

# best_schedule, best_tardiness = tabu_search_enhanced(processing_times, due_dates, precedences, 10, L=10, tolerance=0, f_initial=initial_solution)
# print(f"Best Schedule: {best_schedule}")
# print(f"Total Tardiness: {best_tardiness}")
# print("")

#problem sheet example 5
# processing_times = [10, 7, 3]
# due_dates = [15,2,13]
# precedences = []

# best_schedule, best_tardiness = tabu_search(processing_times, due_dates, precedences, K=10, L=20, tolerance=10)
# print(f"Best Schedule: {best_schedule}")
# print(f"Best Total Tardiness: {best_tardiness}")
