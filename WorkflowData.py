# 31 x 31 Adjacency Matrix
M = 31
N = 31

G = [[0 for i in range(0, M)] for j in range(0, N)]

G[0][30]=1
G[1][0]=1
G[2][7]=1
G[3][2]=1
G[4][1]=1
G[5][15]=1
G[6][5]=1
G[7][6]=1
G[8][7]=1
G[9][8]=1
G[10][0]=1
G[11][4]=1
G[12][11]=1
G[13][12]=1
G[16][14]=1
G[14][10]=1
G[15][4]=1
G[16][15]=1
G[17][16]=1
G[18][17]=1
G[19][18]=1
G[20][17]=1
G[21][20]=1
G[22][21]=1
G[23][4]=1
G[24][23]=1
G[25][24]=1
G[26][25]=1
G[27][25]=1
G[28][26]=1
G[28][27]=1
G[29][3]=1
G[29][9]=1
G[29][13]=1
G[29][19]=1
G[29][22]=1
G[29][28]=1


# Processing Times Array
p = [3, 10, 2, 2, 5, 2, 14, 5,
     6, 5, 5, 2, 3, 3, 5, 6, 6,
     6, 2, 3, 2, 3, 14, 5, 18,
     10, 2, 3, 6, 2, 10]


# Due Times Array
d = [172, 82, 18, 61, 93, 71, 217, 295, 290,
     287, 253, 307, 279, 73, 355, 34,
     233, 77, 88, 122, 71, 181, 340, 141,
     209, 217, 256, 144, 307, 329, 269]


# Graph Implementation
class Graph():

    forward_dict = {}
    backward_dict = {}

    # take an input adj matrix and convert to inner format
    def __init__(self, adj_matrix: list[list[any]]):
        for i in range(len(adj_matrix)):
            self.add_node(i)
            for j in range(len(adj_matrix[i])):
                if adj_matrix[i][j] == 1:
                    self.add_directed_edge(i, j)

    # create data structure for forward and backwards tree traversal
    def add_directed_edge(self, entry_node: any, exit_node: any):
        result = self.forward_dict.get(entry_node)

        if result == None:
            self.forward_dict[entry_node] = set()
        self.forward_dict[entry_node].add(exit_node)

        result = self.backward_dict.get(exit_node)
        if result == None:
            self.backward_dict[exit_node] = set()
        self.backward_dict[exit_node].add(entry_node)

    def add_node(self, node):
        result = self.forward_dict.get(node)
        if result == None: 
            self.forward_dict[node] = set()

        result = self.backward_dict.get(node)
        if result == None:      
            self.backward_dict[node] = set()

    # remove a node and returns the list of nodes that pointed to it
    def remove_node(self, node):
        result = self.forward_dict.get(node)
        points_to = set()
        pointed_by = set()

        if result != None:
            points_to = self.forward_dict[node]    
            del self.forward_dict[node]

        result = self.backward_dict.get(node)
        if result != None:
            pointed_by = self.backward_dict[node]    
            del self.backward_dict[node]

        for child in points_to:
            self.backward_dict[child].remove(node)

        for parent in pointed_by:
            self.forward_dict[parent].remove(node)


    # method for printing the tree
    def __str__(self):
        output_str = ""
        for key, value in self.forward_dict.items():
            output_str += ((str(key) + ":" + str(value)) + "\n")
        return output_str.removesuffix("\n")


