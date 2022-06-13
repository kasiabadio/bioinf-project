
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
        
        #visited[u] += 1

    
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
        

def greedy_algorithm():
    global N, olis
    path = []
    all = []
    g = Graph(N)
    g.create_graph(olis)
    g.print_all_paths(path, all) # create answer
    return all[0]

# --------------- HEURISTIC -----------------

# increase lmer count (after inserting a solution or deleting it)
def count_lmers(olis_set):
    global lmers
    for oli in olis_set:
        if oli in lmers:
            lmers[oli] += 1
        else:
            lmers[oli] = 1


def extend_move_insert(mer):
    global best_solution, tabu, K, S0
    
    # check if can be improved
    if best_solution[(len(best_solution)-K+1):] != mer[:-1]:
        #print("Comparison insertion: ", best_solution[(len(best_solution)-K+1):], mer[:-1])
        # return false if no improvement
        return False
    
    # insert it in solution
    best_solution += mer[-1]
    if mer != S0:
        tabu.append(mer)
    return True
    

def restart(reference_set, greedy_solution):
    global lmers

    # swap solutions
    min_length_solution = float('inf')
    to_swap = -1
    for i, solution in enumerate(reference_set):
        if len(solution) < min_length_solution:
            to_swap = i
            min_length_solution = len(solution)

    # delete olis from lmers from to swap
    for i in range(len(reference_set[to_swap])-1):
        to_delete = reference_set[to_swap][i:(i+K)]
        if to_delete in lmers:
            lmers[to_delete] -= 1

    # add olis to lmers from greedy_solution
    for i in range(len(greedy_solution)-1):
        to_add = greedy_solution[i:(i+K)]
        if to_add in lmers:
            lmers[to_add] += 1

    reference_set[to_swap] = greedy_solution
    return reference_set


def main_tabu():
    global best_solution, olis, K, S0, visited_with_counter, final_solutions
    
    visited_with_counter_copy = visited_with_counter.copy()
    # add olis to lmers from first greedy solution
    for j in range(4):
        greedy_solution = greedy_algorithm()
        reference_set.append(greedy_solution)

    visited_with_counter = visited_with_counter_copy

    for i in range(len(greedy_solution)-1):
        to_add = greedy_solution[i:(i+K)]
        if to_add in lmers:
            lmers[to_add] += 1
    
    reference_set = sorted(reference_set, key=lambda x: len(x), reverse=True)
    best_solution = greedy_solution
    #reference_set = [best_solution, '']
 
    # 3) while not all restarts done
    loop_count = 0
    loop_count_outer = 0

    lenghts_tab = []
    del_insert_tab = [[],[]]
    temporary_best = ["", 0]
    while loop_count_outer < 10:
            
        greedy_solution = greedy_algorithm()
        reference_set.append(greedy_solution)
        # replace the worst solution from reference_set by greedy solution
        if len(reference_set) > 1:
            greedy_solution = greedy_algorithm()
            visited_with_counter = visited_with_counter_copy
            reference_set = restart(reference_set, greedy_solution)

        reference_set = sorted(reference_set, key=lambda x: len(x), reverse=True)
        best_solution = reference_set[0]

        first_sol = best_solution
        print("\nbest_solution before extending/deleting: \n", best_solution)
        print("\nREFERENCE SET SIZE:", len(reference_set))

        while loop_count < 8:  
           
            #print("reference_set after sorting ", reference_set)

            # 4) while not all cycles of restarts do 12, 13
            deletion_count = 0
            insertion_count = 0

            for i in range(400):
                #save full length solutions
                if(len(best_solution) == N and best_solution not in final_solutions):
                    final_solutions.append(best_solution)
                    reference_set.pop(0)
                    greedy_solution = greedy_algorithm()
                    reference_set.append( greedy_solution )
                    visited_with_counter = visited_with_counter_copy

            
                #print("TABU len ", len(tabu))
                #print("VISITED WITH COUNTER: ", visited_with_counter)
                # 12, 13) insertion or deletion of an lmer
                if(len(olis)>=10):
                    if len(tabu) >= len(olis)//10:      #tabu_size
                        tabu.pop(0)
                else:
                    if len(tabu) >= 3:      #tabu_size
                        tabu.pop(0)

                is_inserted = False
                #sortujemy olis wg częstotliwości w rozwiązaniach


                #CO TU SIe BeDZIE DZIAlO :OOOOO

                olis = sorted(lmers, key=lambda lmer: lmers[lmer])
                #print("\nbest_solution before extending/deleting: ", best_solution)
                for oli in olis:
                    if oli not in tabu:
                        # check counter in visited_with_counter && add fragment to lmers because it is useful
                        if visited_with_counter[oli] > 0:
                            is_inserted = extend_move_insert(oli)
                            #print("I checked addition for ", oli, " and it is ", is_inserted)
                            if is_inserted:
                                lmers[oli] += 1
                                visited_with_counter[oli] -= 1
                                #print("counter + ", oli)
                                insertion_count+=1
                                #print("best_solution after adding: ", best_solution)
                                break

                if not is_inserted:
                    fragment = best_solution[len(best_solution)-K:]
                    if fragment in lmers: #and fragment not in tabu:
                        if lmers[fragment] > 0:
                            # increase counter in visited_with_counter
                            if fragment in visited_with_counter:
                                visited_with_counter[fragment] += 1
                            else:
                                visited_with_counter[fragment] = 1

                            # delete fragment from lmers because it is not useful
                            lmers[fragment] -= 1
                            #print("counter - ", fragment)
                            deletion_count+=1
                            best_solution = best_solution[:-1]
                            if fragment != S0:
                                tabu.append(fragment)
                    #else:
                        #tabu.pop(-1)
                        #tabu.pop(-1)
                        #print("tabu", tabu)
                        #final_solutions.append(best_solution)
                        #break
                            #print("best_solution after delete: ", best_solution)

            #print("LMERS: ", lmers)
            reference_set[0] = best_solution
            #print("reference_set[0] ", reference_set[0])
            olis = sorted(lmers, key=lambda lmer: lmers[lmer])
            temp_length = len(best_solution)
        
            loop_count += 1
            #print("\n\nbest_solution after changes: ", best_solution)
            #print("Wydluzylismy o:", temp_length - len(first_sol))
            lenghts_tab.append(temp_length)
            #print("\ndeleted: ", deletion_count, " inserted", insertion_count)
            #print("Szukana dlugosc lancucha: ", N, " dlugosc znalezionego lancucha: ", temp_length)
            del_insert_tab[0].append(deletion_count)
            del_insert_tab[1].append(insertion_count)
            #zapisz najlepsze rozwiązanie z iteracji while
            if(temporary_best[1]<temp_length):
                temporary_best = [best_solution, temp_length]
        loop_count_outer+=1
    print("\n\n------FINAL: \n searching for length: ", N, "\nour lengths: \n", lenghts_tab, "\n deletion count: \n", del_insert_tab[0], "\ninsertion count: \n", del_insert_tab[1])
    print("Best solution len: ", temporary_best[1])
    final_solutions.append(temporary_best[1])
    print("final", final_solutions)
    reference_set.pop(0)


       
# --------------------------- UTIL ----------------------------------
        
def read_instance():
    global file, dna, N, S0, probe, K, olis, visited_with_counter, lmers
    # parsuj xml
    file = minidom.parse(input())
    dna = file.firstChild
    N = int(dna.getAttribute('length')) #długość badanej sekwencji
    S0 = dna.getAttribute('start') # początkowy fragment długości k
    probe = dna.getElementsByTagName('probe')[0]
    K = len(probe.getAttribute('pattern')) # długość sond oligonukleotydowych
   
    for oli in probe.getElementsByTagName('cell'):
        olis.append(oli.firstChild.nodeValue)

        # add to lmers set
        lmers[oli.firstChild.nodeValue] = 0

        for _ in range(int(oli.getAttribute('intensity'))):
            if oli.firstChild.nodeValue not in visited_with_counter:
                visited_with_counter[oli.firstChild.nodeValue] = int(oli.getAttribute('intensity'))
        

# ------------------------ MAIN --------------------------------

if __name__ == '__main__':
    
    file = -1
    dna = -1
    N = -1
    S0 = ''
    probe = ''
    K = -1
    olis = []
    visited_with_counter = {}
    lmers = {}
    final_solutions = []

    read_instance()
    #print("MAIN VISITED WITH COUNTER ", visited_with_counter)
    #best_solution = greedy_algorithm()
    best_solution = []
    #print("greedy: ", best_solution)

    # HEURISTIC
    tabu = []
    main_tabu()
    # moves - add / delete / shift of nucleotide
    # tabu tab - list of inserted / deleted / shifted nucleotides remebered for certain amount of iterations
    
    # global evaluation -> length of sequence (for making the sequence longer)

    # (when algorithm is stuck) 
    # count number of times oligonucleotide is included in solutions, 
    # add l-mer with lowest value to solution 
    # else if no feasable insertion then deletion is applied
    # e.g. frequency value of l-mer = number of iterations
