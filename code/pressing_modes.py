import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pressing_scales_common_tones import scale_dict

def is_brighter(a, b):
    assert(len(a) == len(b))
    a_only = set(a).difference(set(b))
    b_only = set(b).difference(set(a))
    assert(len(a_only) == len(b_only) == 1)
    if ((list(a_only)[0] - list(b_only)[0]) % 12) < 6:
        return 1
    else:
        return 0

def get_modes(scale_type):
    # do everything in D.  
    modes = []
    for s, ns in scale_dict.items():
        if s[1] == scale_type:
            if 2 in ns:
                modes.append(ns)
    return modes
 
def get_max_intersection(modes):
    max_intersection = 0
    for x in modes:
        for y in modes:
            if set(x) == set(y):
                continue
            mode_intersection = set(x).intersection(set(y)) 
            if len(mode_intersection) > max_intersection:
                max_intersection = len(mode_intersection)
    return max_intersection

def test_int_altered():
    a = get_modes('melodic_minor')
    print(a)
    mi = get_max_intersection(a)
    print(mi)


def order_dark_bright(scale_type):
    modes = get_modes(scale_type)

#test_int_altered()
#print(get_modes('major'))

#
four_7scale_colors = ['#94A0B2', '#2D2828', '#D2C8BC', '#35608D']

def color_node_list(row_names, colors):
    node_colors = []
    for r in row_names:
        if r[1] == 'major':
            node_colors.append(colors[0])
        elif r[1] == 'melodic_minor':
            node_colors.append(colors[1])
        elif r[1] == 'harmonic_minor':
            node_colors.append(colors[2])
        elif r[1] == 'harmonic_major':
            node_colors.append(colors[3])
    return node_colors

def build_seven_note_mode_subnetwork():
    # first, we only care about 7 diatonic modes and the neighboring pressing scales 
    seven_diatonic_modes = {k : v for k,v in scale_dict.items() if k[1] == 'major' if 2 in v }
    #print(seven_diatonic_modes)
    seven_note_nondiatonic = {k : v for k,v in scale_dict.items() if len(v) == 7 if k[1] != 'major'}
    #print(seven_note_nondiatonic)
    rel_scale_dict = {**seven_diatonic_modes, **seven_note_nondiatonic}
    n_row = len(rel_scale_dict.keys())
    common_tone_mat = np.zeros((n_row, n_row))
    bd_mat = np.zeros((n_row, n_row))
    row_names = []
    col_names = []
    for i, (k_i, v_i) in enumerate(rel_scale_dict.items()):
        #row_names.append("_".join([k_i[0], k_i[1] ])
        row_names.append(k_i)
        for j, (k_j, v_j) in enumerate(rel_scale_dict.items()):
            if len(col_names) < n_row:
                col_names.append(k_j)
            int_size = len(set(v_i).intersection(set(v_j)))
            common_tone_mat[i, j] = int_size
            # if scale a darker than b
            if int_size == 6:
                bd_mat[i,j] = is_brighter(v_i, v_j) 
    ct_df = pd.DataFrame(common_tone_mat, columns=col_names, index=pd.MultiIndex.from_tuples(row_names))
    bd_df = pd.DataFrame(bd_mat, columns=col_names, index=pd.MultiIndex.from_tuples(row_names))
    return ct_df, bd_df

ct_df, bd_df = build_seven_note_mode_subnetwork()

ct_df.to_csv('common_tone_matrix.csv')


def prune_non_major_adjacent_nodes(df):
    bad_columns = []
    bad_rows = []
    for col in df.columns:
        is_good = False
        for row in df.index:
            if row[1] == 'major':
                if df[col].loc[row] != 0:
                    is_good = True
        # Because 'Eb_harmonic_minor', 'F#_harmonic_major' are missing via distance but contain D.
        if (not is_good) and (2 not in scale_dict[col]) :
        #if not is_good:
            bad_columns.append(col)
    for row in df.index:
        is_good = False
        for col in df.columns:
            if col[1] == 'major':
                if df[col].loc[row] != 0:
                    is_good = True
        if (not is_good) and (2 not in scale_dict[row]) :
        #if not is_good:
            bad_rows.append(row)
    #print(bad_columns)
    #print(bad_rows)
    bad_int = set(bad_columns).intersection(set(bad_rows))
    #print(f'pruning the following nodes: {bad_int}')
    return df.drop(columns = bad_int, index = bad_int)


def plot_ct_df():
    six_df = ct_df[ct_df == 6].fillna(0)
    #print(ct_df[ct_df == 6])
    plot_graph(six_df)

def validate_pruned_selection(pruned_df):
    """
    Checks to make sure the note D (2) is in all modes, except for two odd melodic minor scales.
    """
    scales_missing_D = []
    for c in pruned_df.columns:
        if 2 not in scale_dict[c]:
            scales_missing_D.append(c)
    print(f'scales missing D in pruned matrix are:  {scales_missing_D}.')

def find_missing_scales(pruned_df):
    with_d = {k : v for k,v in scale_dict.items() if (2 in v)}
    with_d_list = set([k[0] + '_' + k[1] for k in with_d.keys()])
    pruned_col_list = set([sn[0] + '_' + sn[1] for sn in pruned_df.columns])
    missing_scales = with_d_list.difference(pruned_col_list)
    print(f'scales in scale_dict with D missing from pruned graph:  {missing_scales}')


def plot_bd_df(scale_types_drop = None):
    #print(ct_df[ct_df == 6])
    pruned_bd = prune_non_major_adjacent_nodes(bd_df)
    validate_pruned_selection(pruned_bd)
    find_missing_scales(pruned_bd)
    if scale_types_drop is not None:
        drop_cols = [c for c in pruned_bd.columns if c[1] in scale_types_drop]
        pruned_bd.drop(columns = drop_cols, index = drop_cols, inplace = True)
    #print(pruned_bd)
    plot_graph(pruned_bd, digraph = True)


def plot_graph(df, digraph = False):
    node_colors = color_node_list(df.columns, four_7scale_colors)
    if digraph:
        G = nx.from_pandas_adjacency(df, create_using=nx.DiGraph)
        #sorted_modes = list(nx.topological_sort(G))
        #print(len(sorted_modes))
        #print(sorted_modes)
    else:
        G = nx.from_pandas_adjacency(df)
    nx.draw_kamada_kawai(G, node_color = node_colors, node_size = 500,  with_labels = True )
    #major_nodes = [k for k in df.columns if (k[1] == 'major' )]
    #major_notes = ['Eb','Bb', 'F','C','G','D','A']
    #pos_dict = { (n,'major') : (i *1000, i*1000) for i, n in enumerate(major_notes)} 
    #nx.draw(G, node_color = node_colors,  with_labels = True, pos=nx.spring_layout(G, pos = pos_dict, fixed = major_nodes))
    #nx.draw(G, node_color = node_colors,  with_labels = True)
    plt.show()

# useful for constructing the bright dark plot
pruned_bd = prune_non_major_adjacent_nodes(bd_df)
pruned_bd.to_csv('pruned_bd_digraph.csv')

#plot_ct_df()
#plot_bd_df(['melodic_minor'])
#plot_bd_df(['major'])
#plot_bd_df(['harmonic_major'])
#plot_bd_df(['harmonic_major', 'harmonic_minor'])
if __name__ == '__main__':
    plot_bd_df()
