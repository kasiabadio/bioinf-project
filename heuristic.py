from xml.dom import minidom
import time

# funkcja do przejścia przez wierzchołki
def eulerian_path(k_dict, start, path_length):
        global file, dna, N, S0, probe, K, olis
        stack = []
        path = []
        temp_start = start[:K-1]
        temp_stack = {key: val for key, val in k_dict.items()
               if key.startswith(temp_start)}
        #print("temp_stack", temp_stack)

        temp_key = list(temp_stack.keys())
        temp_value = list(temp_stack.values())
        stack.append(temp_key[0])
        stack.append(temp_value[0][0])
        k_dict[temp_start].remove(temp_value[0][0])
        #print("k_dict", k_dict)

        while len(stack)>0 and len(path) <= path_length: 
            top = stack[-1]
            if(k_dict[top] != []):
                vertex = k_dict[top][0] 
                stack.append(vertex)
                k_dict[top].remove(vertex)
            else:
                path.append(stack[-1])
                stack.pop()
        path.reverse()
        #print(path)
        return path

# funkcja do zamiany tablicy z fragmentami w graf
def create_debrujin_graph():
    global file, dna, N, S0, probe, K, olis
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
        k_dict[str(i[0:-1])].append(str(i[1:]))

    return k_dict

def read_answer(k_list):
        sequence = ''
        for i in k_list:
            sequence += i[0]
        sequence += i[1:]
        return sequence


def read_instance():
    global file, dna, N, S0, probe, K, olis
    # parsuj xml
    file = minidom.parse(input())
    dna = file.firstChild
    N = int(dna.getAttribute('length')) #długość badanej sekwencji
    S0 = dna.getAttribute('start') # początkowy fragment długości k
    probe = dna.getElementsByTagName('probe')[0]
    K = len(probe.getAttribute('pattern')) # długość sond oligonukleotydowych
   
    for oli in probe.getElementsByTagName('cell'):
        for _ in range(int(oli.getAttribute('intensity'))):
            olis.append(oli.firstChild.nodeValue)


if __name__ == '__main__':
    
    file = -1
    dna = -1
    N = -1
    S0 = ''
    probe = ''
    K = -1
    olis = []

    read_instance()

    start_time = time.time()
    k_dict = create_debrujin_graph()
    path = eulerian_path(k_dict, S0, N)
    end_time = time.time()
    elapsed = round(end_time - start_time, 6)
    print(elapsed)
    print(read_answer(path))