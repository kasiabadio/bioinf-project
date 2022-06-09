from email.policy import default
from xml.dom import minidom
import time
from collections import defaultdict


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

        # TODO: potencjalnie tutaj można zmniejszyć czas wyszukiwania, przez nie przechodzenie po wszystkich ścieżkach 
        #for _ in range(len(self.graph[u])):

        # wybierz wierzchołek, który występuje najwięcej razy w grafie
        chosen_j = -1
        for j in self.graph[u]:
            max_value = -1
            if j == 0:
                max_value = visited[0]
            if visited[j] > 0 and visited[j] > max_value:
                max_value = visited[j]
                chosen_j = j
        
        # jeżeli nie ma następnika, to dodaj ścieżkę
        if chosen_j == -1:
            all.append(self.read_answer(path))
        # jeżeli są następnicy, to wybierz wierzchołek o największej liczności
        else:
            self.print_all_paths_util(chosen_j, visited, path, all)

        # usuń wierzchołek ze ścieżki i zaznacz jako niezaznaczony
        path.pop()
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
    g.print_all_paths(path, all)
    

    end_time = time.time()

    elapsed = round(end_time - start_time, 6)

    for e in all:
        if (len(e) <= N):
            print(len(e))

    print(len(all))
    