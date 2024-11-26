from WorkflowData import *

# G = Adj Matrix for DAG

lowest_cost_last = LowestCostLast(G, d, p)

print(lowest_cost_last.workflow_graph)

lowest_cost_last.find_optimum()

print(lowest_cost_last.workflow_graph)
print(lowest_cost_last.schedule)