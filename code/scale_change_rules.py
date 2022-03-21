from pressing_scales_common_tones import major, melodic_minor, harmonic_major, harmonic_minor
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class JazzScale():
    def __init__(self, root_number, scale_type):
        self.root = root_number % 12
        self.scale_type = scale_type 
        assert scale_type in ['major', 'melodic_minor', 'harmonic_minor', 'harmonic_major' ]
        # transpose pitch classes
        self.update_scale_notes()
    
    def __eq__(self, other):
        if self.notes == other.notes: 
            return True
        else:
            return False

    def update_scale_notes(self):
        if self.scale_type == 'major':
            self.notes = major
        elif self.scale_type == 'melodic_minor':
            self.notes = melodic_minor
        elif self.scale_type == 'harmonic_major':
            self.notes = harmonic_major
        elif self.scale_type == 'harmonic_minor':
            self.notes = harmonic_minor
        else:
            raise ValueError('scale type note ')

        self.notes = sorted([(x + self.root) % 12 for x in self.notes])

    def modulate(self, transp, new_scale_type):
        self.root = (self.root + transp) % 12
        self.scale_type = new_scale_type
        self.update_scale_notes()


# (scale type, type of change), : [ allowable transitions.]

scale_rules = {('major', 'dark') : [(5, 'major'), (0, 'harmonic_major'), (0, 'melodic_minor')],
        ('melodic_minor', 'dark') : [(-2,'major'), (0, 'harmonic_minor') ],
        ('harmonic_major', 'dark') : [(5,'melodic_minor'), (0, 'harmonic_minor') ],
        ('harmonic_minor', 'dark') : [(3,'major'), (3, 'harmonic_major') ],
        ('major', 'bright') : [(-5, 'major'), (2, 'melodic_minor'), (-3, 'harmonic_minor')],
        ('melodic_minor', 'bright') : [(0, 'major'), (-5, 'harmonic_major')],
        ('harmonic_major', 'bright') : [(0, 'major'), (-3, 'harmonic_minor')],
        ('harmonic_minor', 'bright') : [(0, 'melodic_minor'), (0, 'harmonic_major')]
        }


def build_dark_adjacency():
    colnames = []
    for scale in ['major', 'melodic_minor', 'harmonic_major', 'harmonic_minor']:
        for root in range(12):
            colnames.append((root, scale))
    A = np.zeros((len(colnames), len(colnames)), dtype = int)
    for i, x in enumerate(colnames):
        possible_maps = scale_rules[(x[1], 'dark')] 
        for j, y in enumerate(colnames):
            root_diff = (y[0] - x[0]) % 12
            if (root_diff, y[1]) in possible_maps:
                A[i,j] = 1
    
    A = pd.DataFrame(A, index = colnames, columns = colnames)
    return A


def cycle_multiples():
    A = build_dark_adjacency()             
    powers = [A]
    An = A
    plt.matshow(An)
    plt.savefig(f'An_{0}.png')
    #plt.matshow(An)
    for c in range(36):
        An = A.dot(An)
        plt.matshow(An)
        plt.savefig(f'An_{c + 1}.png')
        powers.append(An)
        if An.to_numpy().trace() != 0:
            print(f'cycle detected for length {c}')
            print(An)
            diag = np.diagonal(An)
            print(diag.nonzero())


def dot_adj_vector(scale_index, max_dots = 12):
    vs = []
    A = build_dark_adjacency()
    source_vec = np.zeros(A.shape[0])
    # one-hot encode
    source_vec[scale_index] = 1
    new_vec = source_vec
    vs.append(new_vec)
    for d in range(max_dots + 1):
        new_vec = A.T.dot(new_vec)
        vs.append(new_vec)
    return vs
    

def get_cycles(max_cycles):
    A = build_dark_adjacency()
    G = nx.from_pandas_adjacency(A, create_using = nx.DiGraph)
    basis = nx.cycle_basis(G, root = (0, 'major'))
    #edges = nx.find_cycle(G, source = (0, 'major'), orientation = 'original')
    return basis
    #cycles = nx.simple_cycles(G)
    #n_cycles_found = 0
    #for i, x in enumerate(cycles):
    #    if x[0] == (0, 'major'):
    #        print(f'cycle number {i}:')
    #        print(f'{x}')
    #        n_cycles_found += 1
    #    if n_cycles_found > max_cycles: 
    #        return cycles
    #return cycles

#A = build_dark_adjacency()             



# the scale matrices wee built before were subset to those neighboring the 7 modes starting on C.
# these rules or a proper adjacency matrix would allow one to look for cycles without using the notes.

# go from major to major via dark paths only.
def find_cycles(start_scale, current_scale = None, history = []): 
    """
    start and current are a list of root and scale_type. 
    """
    if len(history) > 40:
        print('depth of 40 exceeded')
        return
    if current_scale is None:
        current_scale = start_scale
    # a list of allowable transitions
    eligible_rules = scale_rules[(start_scale.scale_type, 'dark')]
    for rule in eligible_rules:
        new_root = current_scale.root + rule[0]
        new_scale_type = rule[1]
        proposed_new_scale = JazzScale(new_root, new_scale_type) 
        print(proposed_new_scale.scale_type)
        if proposed_new_scale == start_scale:
            print(f'{len(history)} cycle found with history: {history}')
        else:
            history.append((proposed_new_scale.root, proposed_new_scale.scale_type))
            find_cycles(start_scale, proposed_new_scale, history)

#if __name__ == "__main__":
#    A = build_dark_adjacency()
#    G = nx.from_pandas_adjacency(A, create_using = nx.DiGraph)
#    find_all_cycles(G, source=(0, 'major'), cycle_length_limit = 12)
    #x = JazzScale(0, 'major')
    #find_cycles(x)
