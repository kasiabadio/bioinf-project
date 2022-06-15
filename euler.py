from math import gamma
from xml.dom import minidom
import time


def read_answer(k_list):
    sequence = ''
    for i in k_list:
        sequence += i[0]
    sequence += i[1:]
    return sequence


def create_debrujin_graph(olis, visited_with_counter):
    kmers = []
    k_dict = {}
    for oli in olis:   
        if(oli[:-1] not in kmers):
            kmers.append(oli[:-1])
        if(oli[1:] not in kmers):
            kmers.append(oli[1:])  

    for kmer in kmers:
        k_dict[kmer] = []

    for i in olis:
        # add counter to solution
        #print("i: ", i, " visited_with_counter[i]: ", visited_with_counter[i])
        for _ in range(visited_with_counter[i]):
            k_dict[str(i[0:-1])].append(str(i[1:]))
    
    return k_dict


def eulerian_path(k_dict, start):
    global N, K
    stack = []
    path = []
    temp_start = start[:K-1]
    temp_stack = {key: val for key, val in k_dict.items() if key.startswith(temp_start)}
   
    temp_key = list(temp_stack.keys())
    temp_value = list(temp_stack.values())
    
    stack.append(temp_key[0])
    stack.append(temp_value[0][0])
    k_dict[temp_start].remove(temp_value[0][0])

    while len(stack)>0 and len(path) < N: 
        top = stack[-1]
        if(k_dict[top] != []):
            vertex = k_dict[top][0] 
            stack.append(vertex)
            k_dict[top].remove(vertex)
        else:
            path.append(stack[-1])
            stack.pop()
    path.reverse()
    
    return path




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

    g = create_debrujin_graph(olis, visited_with_counter)
    path = eulerian_path(g, S0)
    
    if len(path) > 0:
        answer = read_answer(path)
        print(answer)
        print("Soultion length: ", len(answer))

    end_time = time.time()
    
    elapsed = round(end_time - start_time, 6)
    print("Elapsed time euler: ", elapsed, " s")