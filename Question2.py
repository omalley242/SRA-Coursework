import random
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

def valid_interchange(precedences, idx1, idx2):
    for i, j in precedences:
        if (i == idx1 and j == idx2) or (i == idx2 and j == idx1):
            return False
    return True

def compute_tardiness(processing_times, due_dates, schedule):
    cumulative_time, tardiness_sum = 0, 0
    
    for job_index in schedule:
        cumulative_time += processing_times[job_index]
        job_tardiness = max(0, cumulative_time - due_dates[job_index])
        tardiness_sum += job_tardiness
    return tardiness_sum

def tabu_search(processing_times, due_dates, precedences, K, L, tolerance, f_initial):
    curr_schedule = generate_initial_solution(precedences, len(processing_times), f_initial)
    best_schedule = curr_schedule[:]
    best_tardiness = compute_tardiness(processing_times, due_dates, best_schedule)

    tabu_list = []
    idx = 0

    for _ in range(K):
        neighbors = []
        size = len(curr_schedule)
        for i in range(idx, size-1):
            if valid_interchange(precedences, curr_schedule[i], curr_schedule[i+1]):
                neighbor = curr_schedule[:]
                temp = neighbor[i]
                neighbor[i] = neighbor[i+1]
                neighbor[i+1] = temp

                to_append = (neighbor, (neighbor[i+1], neighbor[i]))
                neighbors.append(to_append)
        for i in range(idx):
            if valid_interchange(precedences, curr_schedule[i], curr_schedule[i+1]):
                neighbor = curr_schedule[:]
                temp = neighbor[i]
                neighbor[i] = neighbor[i+1]
                neighbor[i+1] = temp

                to_append = (neighbor, (neighbor[i+1], neighbor[i]))
                neighbors.append(to_append)

        for neighbor, neighbor_change in neighbors:
            neighbor_cost = compute_tardiness(processing_times, due_dates, neighbor)

            if not sorted(neighbor_change) in tabu_list and neighbor_cost - best_tardiness <= tolerance:
                curr_schedule = neighbor
                current_cost = neighbor_cost

                if len(tabu_list) >= L:
                    tabu_list.pop()
                
                sorted_neighbor_change = sorted(neighbor_change)
                tabu_list.insert(0, sorted_neighbor_change)

                idx = max(curr_schedule.index(sorted_neighbor_change[0]), curr_schedule.index(sorted_neighbor_change[1]))

                if current_cost < best_tardiness:
                    best_schedule = curr_schedule[:]
                    best_tardiness = current_cost
                
                break

    return best_schedule, best_tardiness

processing_times = [3, 10, 2, 2, 5, 2, 14, 5, 6, 5, 5, 2, 3, 3, 5, 6, 6, 6, 2, 3, 2, 3, 14, 5, 18, 10, 2, 3, 6, 2, 10]
due_dates = [172, 82, 18, 61, 93, 71, 217, 295, 290, 287, 253, 307, 279, 73, 355, 34, 233, 77, 88, 122, 71, 181, 340, 141, 209, 217, 256, 144, 307, 329, 269]
precedences = [(0, 30), (1, 0), (2, 7), (3, 2), (4, 1), (5, 15), (6, 5), (7, 6), (8, 7), (9, 8),
    (10, 0), (11, 4), (12, 11), (13, 12), (16, 14), (14, 10), (15, 4), (16, 15), (17, 16),
    (18, 17), (19, 18), (20, 17), (21, 20), (22, 21), (23, 4), (24, 23), (25, 24), (26, 25),
    (27, 25), (28, 26), (28, 27), (29, 3), (29, 9), (29, 13), (29, 19), (29, 22), (29, 28)]

initial_solution = [29, 28, 22, 9, 8, 13, 12, 11, 3, 19, 21, 2, 26, 27, 7, 6, 
                    18, 20, 25, 17, 24, 16, 14, 5, 23, 15, 4, 10, 1, 0, 30]

best_schedule, best_tardiness = tabu_search(
    processing_times, due_dates, precedences, L=20, K=1000, tolerance=5, f_initial=initial_solution
)
print(best_schedule)
print(best_tardiness
