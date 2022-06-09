from xml.dom import minidom

# funkcja do zamiany tablicy z fragmentami w graf
def create_debrujin_graph(olis):
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

if __name__ == '__main__':
    print("INFORMACJA O POWTORZENIACH, BLEDY POZYTYWNE")

    # parsuj xml
    file = minidom.parse('bio.php.xml')
    dna = file.firstChild
    N = int(dna.getAttribute('length')) #długość badanej sekwencji
    S0 = dna.getAttribute('start') # początkowy fragment długości k
    probe = dna.getElementsByTagName('probe')[0]
    K = len(probe.getAttribute('pattern')) # długość sond oligonukleotydowych
    print("Długość sekwencji: ", N, " Fragment początkowy: ", S0, " Długość sond: ", K)
   
    olis = []
    for oli in probe.getElementsByTagName('cell'):
        olis.append(oli.firstChild.nodeValue)
    
    k_mers = create_debrujin_graph(olis)
    