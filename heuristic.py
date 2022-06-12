
from xml.dom import minidom
import time
from collections import defaultdict
import random

class Graph:

    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)

    def read_answer(self, k_list):
        sequence = ''
        for i in k_list:
            sequence += i[0]
        sequence += i[1:]
        return sequence


    def print_all_paths_util(self, u, visited, path, all):
        global N, S0
        
        visited[u] -= 1
        path.append(u)

        # wybierz wierzchołek
        to_choose_from = []
        for j in self.graph[u]:
            if visited[j] > 0:
                to_choose_from.append(j)
        
        if len(to_choose_from) > 0: 
            # wybierz losowy wierzchołek
            chosen_j = random.choice(to_choose_from)
            self.print_all_paths_util(chosen_j, visited, path, all)
        else :
            # jeżeli nie ma następnika, to dodaj ścieżkę
            answer = self.read_answer(path)
            if answer not in all:
                all.append(answer)
        
        visited[u] += 1

    
    def print_all_paths(self, path, all):
        global S0, visited_with_counter
        self.print_all_paths_util(S0, visited_with_counter, path, all)
        
    def create_graph(self, olis):
        global K
        for oli in olis:
            self.graph[oli] = []
        
        # dodaj każdy oli gdzie wszedzie jest następnikiem
        for oli in olis:
            for key in self.graph.keys():
                if oli[0:(K-1)] == key[1:K] and oli != key:
                    # dodaj krawędź
                    self.graph[key].append(oli)

    def print_graph(self):
        for key, value in self.graph.items():
            print("-->", key, ":  ", value, end="\n")
        
    # --------------- HEURISTIC -----------------

    def return_mer_with_lowest_and_highest_frequency(self):
        global lmers
        lowest = float('inf')
        highest = float('-inf')
        mers = ['','']
        for key, value in lmers.items():
            if value < lowest:
                mers[0] = key
            if value > highest:
                mers[1] = key
        return mers


    def count_mer_frequency(self, mer):
        global solutions
        counter = 0
        for solution in solutions:
            if mer in solution:
                counter += 1
        return counter


    def extend_move_insert(self, mer):
        global best_solution, tabu
        
        #TODO: check if can be improved
        #TODO: return false if no improvement
        #TODO: how to insert it in solution
        tabu.append(mer)
        return True
        

    def extend_move_delete(self, mer):
        global best_solution, tabu
            
        #TODO: how to delete it from solution
        #TODO: return false if not deleted succesfully

        tabu.append(mer)
        return True


    def extend_move(self):
        mers = self.return_mer_with_lowest_and_highest_frequency()
        if mers[0] != '':
            return 'INSERT ' + str(self.extend_move_insert(mers[0]))
        elif mers[1] != '':
            return 'DELETE ' + str(self.extend_move_delete(mers[1]))


    def restart(self, reference_set):
        global solutions
        if len(reference_set > 1) and len(solutions) > 0:
            # replace worst solution in reference set by greedy heuristic
            min_length_solution = float('inf')
            to_swap = -1
            for i, solution in enumerate(reference_set):
                if len(solution) < min_length_solution:
                    to_swap = i
                    min_length_solution = len(solution)
            reference_set[to_swap] = solutions.pop(0)

        return reference_set
    

    def main_tabu(self):
        global best_solution, solutions
        #TODO: how should it be initialized?
        reference_set = [best_solution, best_solution]

        #TODO: while not all restarts done -> how to do this?
        reference_set = self.restart(reference_set)

        #TODO: while not all extend moves without improvement done -> how to do this?
        extend_move = self.extend_move()
        if extend_move =='INSERT True':
            pass
        elif extend_move == 'INSERT False':
            pass
        elif extend_move == 'DELETE True':
            pass
        elif extend_move == 'DELETE False':
            pass

        
        
        

def read_instance():
    global file, dna, N, S0, probe, K, olis, visited_with_counter
    # parsuj xml
    file = minidom.parse(input())
    dna = file.firstChild
    N = int(dna.getAttribute('length')) #długość badanej sekwencji
    S0 = dna.getAttribute('start') # początkowy fragment długości k
    probe = dna.getElementsByTagName('probe')[0]
    K = len(probe.getAttribute('pattern')) # długość sond oligonukleotydowych
   
    for oli in probe.getElementsByTagName('cell'):
        olis.append(oli.firstChild.nodeValue)
        for _ in range(int(oli.getAttribute('intensity'))):
            if oli.firstChild.nodeValue not in visited_with_counter:
                visited_with_counter[oli.firstChild.nodeValue] = int(oli.getAttribute('intensity'))
            

if __name__ == '__main__':
    
    file = -1
    dna = -1
    N = -1
    S0 = ''
    probe = ''
    K = -1
    olis = []
    visited_with_counter = {}
    read_instance()
    
    # GREEDY
    start_time = time.time()

    path = []
    all = []
    g = Graph(N)
    g.create_graph(olis)
    g.print_graph()
    for i in range(5):
        path = []
        g.print_all_paths(path, all)
    
    end_time = time.time()
    elapsed = round(end_time - start_time, 6)

    #print(all)
    print("Elapsed time greedy: ", elapsed, " s")


    # HEURISTIC
    solutions = all.copy()
    best_solution = solutions[0]
    lmers = {}
    for solution in solutions:
        lmers[solution] = 1
    tabu = []
    # moves - add / delete / shift of nucleotide
    # tabu tab - list of inserted / deleted / shifted nucleotides remebered for certain amount of iterations
    
    # global evaluation -> length of sequence (for making the sequence longer)

    # (when algorithm is stuck) 
    # count number of times oligonucleotide is included in solutions, 
    # add l-mer with lowest value to solution 
    # else if no feasable insertion then deletion is applied
    # e.g. frequency value of l-mer = number of iterations
