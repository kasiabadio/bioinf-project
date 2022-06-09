import random
import math
import sys
import re
import os
from collections import OrderedDict

#--------------Explanation of the graph solution: https://www.youtube.com/watch?v=TNYZZKrjCSk

if __name__ == '__main__':
    input_first = input().rstrip().split()
    length = int(input_first[1])
    input_second = input().rstrip().split()
    start = input_second[1]
    input_third = input().rstrip().split()
    probe = int(input_third[1])
#--------------read olinucleotides-----------------------------
    olis = []
    for i in range(length - probe + 1):
        ol = input()
        olis.append(ol)
        
#--------------define functions-----------------------------

    def create_debrujin_graph(olis):
        kmers = []
        k_dict = {}
        for oli in olis:   #oli in olis
            if(oli[:-1] not in kmers):
                kmers.append(oli[:-1])
            if(oli[1:] not in kmers):
                kmers.append(oli[1:])  
        for kmer in kmers:
            k_dict[kmer] = []
        for i in olis:
            k_dict[str(i[0:-1])].append(str(i[1:]))
        #print("dict", dict)
        return k_dict

    def eulerian_path(k_dict):
        stack = []
        path = []
        temp_start = start[:probe-1]
        temp_stack = {key: val for key, val in k_dict.items()
               if key.startswith(temp_start)}
        #print("temp_stack", temp_stack)
        temp_key = list(temp_stack.keys())
        temp_value = list(temp_stack.values())
        stack.append(temp_key[0])
        stack.append(temp_value[0][0])
        k_dict[temp_start].remove(temp_value[0][0])
        #print("k_dict", k_dict)
        while len(stack)>0: 
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

    def read_answer(k_list):
        sequence = ''
        for i in k_list:
            sequence += i[0]
        sequence += i[1:]
        return sequence

#--------------use functions-----------------------------

    graph = create_debrujin_graph(olis)
    path = eulerian_path(graph)
    answer = read_answer(path)
    print(answer)
