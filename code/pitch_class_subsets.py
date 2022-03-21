import os
import numpy as np
import pandas as pd
from itertools import chain, combinations

pd.set_option('display.max_rows', 1000)

bright_dark_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_seven_note_modes_sorted_dark_to_bright.csv')
bd = pd.read_csv(bright_dark_csv)

# keep things simple for now and only include scales containing D.
bd = bd[bd.contains_root == True]
bd['notes'] = bd['notes'].apply(eval)

atoms = {'min7' : [0, 3, 7, 10],  'maj7' : [0, 4, 7, 11], 'dom7' : [0, 4, 7, 10 ], 'min7b5' : [0, 3, 6, 10], \
        'augMaj7' : [0, 4, 8, 11], 'minMaj7' : [0, 3, 7, 11], 'fabe' : [0, 4, 6, 11], \
        'min9' : [0, 3, 7, 10, 2], '9' : [0, 2, 4, 7, 10] , 'maj9' : [0, 2, 4, 7, 11]}

def get_brightness(atom_name, notes):
    notes_rooted = [(n + 2) % 12 for n in notes] 
    df_list = []
    for t in range(12):
        transposed = [(n + t) % 12 for n in notes_rooted]
        if t > 6:
           t_printable = '- ' + str(12 - t)
        else:
            t_printable = '+ ' + str(t)
        t_set = set(transposed)
        for index, row in bd.iterrows():  
            m_set = set(row['notes'])
            if t_set.issubset(m_set): 
                brightness = row['brightness'] 
                mode_name = row['common_name'] 
                scale_type = row['scale_type'] 
                #print(f'{t_printable} {atom_name}: {brightness}, {scale}')
                df_list.append({'offset' : t_printable, 'atom_name' : atom_name, 'brightness' : brightness, 'parent_scale_type' : scale_type, 'mode' : mode_name })
    return df_list

def atoms_to_brightness(atoms):
    dfs = []
    for a, ns in atoms.items():
        df_list = get_brightness(a, ns)
        dfs.extend(df_list)
    out = pd.DataFrame(dfs)

    out.brightness = out.brightness.astype(int)
    return out


def build_standard_4note_chord_brightness(atoms):
    out = atoms_to_brightness(atoms)
    out.sort_values(by = ['brightness', 'parent_scale_type'], inplace = True  )
    print(out)
    out.to_csv('final_sorted_pitch_class_brightness.csv')
    

def get_dom7_exts_deprecated():
    # this is incomplete because it's too tedious!  use powerset instead
    dom7_atoms = {'7' : [], '7b5' : [6], '75' : [7],  '7#5' : [8],
            '75#11' : [6,7], '7#11b13' : [6,8], '75b13' : [7,8], 
            '7#115b13' : [6,7,8], 
             '7b9' : [1], '7b5b9' : [1,6], '75b9' : [1,7],  '7#5b9' : [1,8], '75b9#11' : [1,6,7], 
    '7b9#11b13' : [1,6,8], '75b9b13' : [1,7,8], '7#115b13' : [6,7,8]}

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def get_all_dom7_exts():
    n137 = [0, 4, 10]
    eligible_pitches = set(range(12)).difference(set(n137)) 
    lp =  list(powerset(eligible_pitches))
    return lp

def rank_dom7_exts():
    all_dom7_exts = get_all_dom7_exts()
    print(all_dom7_exts)
    print(len(all_dom7_exts))
    # 512... wow!  of course, most of these aren't going to be in any scales examined.
    # ok for now, just name the chords by the list.
    dom7_atoms = {(str(list(x))) : sorted(list(x) + [0, 4, 10]) for x in all_dom7_exts} 
    dom7_exts_ranked = atoms_to_brightness(dom7_atoms)
    dom7_exts_ranked = dom7_exts_ranked[dom7_exts_ranked.offset == '+ 0']
    dom7_exts_ranked.sort_values(by = ['brightness', 'parent_scale_type'], inplace = True  )
    print(dom7_exts_ranked)
    dom7_exts_ranked.to_csv('dom7_extensions_brightness_sorted.csv')


def aggregate_df_by_chord(df, save_as):
    df = (df.groupby(['atom_name'])
            .agg({'mode': lambda x: "; ".join(x),'parent_scale_type':lambda x: "; ".join(x),\
                  'brightness': lambda x: x.tolist()}).reset_index())
            #.agg({'mode': lambda x: x.tolist(),'parent_scale_type':lambda x: x.tolist(),\
            #      'brightness': lambda x: x.tolist()}).reset_index())
    df['n_compatible_modes'] = [np.array(x).shape[0] for x in df.brightness.values]
    #df['mean_brightness'] = np.mean(df['brightness'].tolist(), axis=1)
    df['mean_brightness'] = [abs(np.array(x).mean()) for x in df.brightness.values]
    df = df.sort_values(by=['n_compatible_modes', 'mean_brightness'], ascending=[False, True]).drop(columns=['n_compatible_modes', 'mean_brightness'])
    #df = df.sort_values(by='n_compatible_modes', ascending=False).drop(columns='n_compatible_modes')
    df.rename(columns = {'atom_name' : 'extensions (pitch classes)', 'mode' : 'compatible modes', 'parent_scale_type' : 'parent scale types'}, inplace = True)
    df = df.reset_index()
    df = df.drop(columns = 'index')
    print(df.to_markdown())
    df.to_csv(save_as)

if __name__ == '__main__':
    if not os.path.exists('dom7_extensions_brightness_sorted.csv'):
        rank_dom7_exts()
    dom7_ext_sorted = pd.read_csv('dom7_extensions_brightness_sorted.csv')
    aggregate_df_by_chord(dom7_ext_sorted, save_as = 'dom7_extensions_brightness_sorted_aggregated.csv')
