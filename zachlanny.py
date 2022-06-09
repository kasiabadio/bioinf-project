from email.policy import default
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

    # for e in all:
    #     if (len(e) <= N):
    #         print(len(e))

    print(len(all))