import os
import numpy as np
import pandas as pd

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 10)

atoms = {'maj' : [0,4, 7], 'min' : [0, 3, 7], 'dim' : [0, 3, 6], 'aug' : [0, 4, 8]}


bright_dark_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_seven_note_modes_sorted_dark_to_bright.csv')
bd = pd.read_csv(bright_dark_csv)

bd = bd[bd.contains_root == True]
bd['notes'] = bd['notes'].apply(eval)


list_of_dicts = [] 
for a_lower, ns_lower in atoms.items():
    for a_upper, ns_upper in atoms.items():
        for t in range(12):
            transp = sorted([(n + t) % 12 for n in ns_upper])
            pitches = sorted(list(set(ns_lower + transp)))
            if t > 6:
                t_printable = '- ' + str(12 - t)
            else:
                t_printable = '+ ' + str(t)
            for index, row in bd.iterrows():  
                m_set = set(row['notes'])
                # because bright dark csv is in D
                pitches_in_d = set([(p + 2) % 12 for p in pitches])
                if set(pitches_in_d).issubset(m_set): 
                    brightness = row['brightness'] 
                    mode_name = row['common_name'] 
                    scale_type = row['scale_type'] 
                    d = {'lower' : a_lower, 'offset' : t_printable,\
                         'upper' : a_upper, 'pitches' : pitches,\
                         'n_pitch_classes' : len(pitches), 'brightness' : brightness,\
                         'parent_scale_type' : scale_type, 'mode' : mode_name }
                    list_of_dicts.append(d)

def aggregate_chords(df):
    df = (df.groupby(['lower','offset','upper'])
            .agg({'mode': lambda x: "; ".join(x),'parent_scale_type':lambda x: "; ".join(x),\
                  'brightness': lambda x: x.tolist()}).reset_index())
            #.agg({'mode': lambda x: x.tolist(),'parent_scale_type':lambda x: x.tolist(),\
            #      'brightness': lambda x: x.tolist()}).reset_index())
    df['n_compatible_modes'] = [np.array(x).shape[0] for x in df.brightness.values]
    #df['mean_brightness'] = np.mean(df['brightness'].tolist(), axis=1)
    df['mean_brightness'] = [np.array(x).mean() for x in df.brightness.values]
    df.drop(columns = ['n_compatible_modes'], inplace = True)
    df = df.sort_values(by=['mean_brightness'], ascending= True).reset_index(drop = True)
    return df

all_2_triads = pd.DataFrame(list_of_dicts)
print(all_2_triads)
# drop duplicates.  workaround is because lists are unhashable
all_2_triads_dedup = all_2_triads.loc[all_2_triads.astype(str).drop_duplicates(subset = ['pitches', 'mode']).index]

six_note_chords = all_2_triads_dedup[all_2_triads_dedup['n_pitch_classes'] == 6]
agg = aggregate_chords(six_note_chords)
agg.to_csv('all_six_note_triad_combos.csv')
#print(agg)
#print(six_note_chords.sort_values(by = 'brightness').reset_index())

all_11th_like = all_2_triads[all_2_triads.offset.isin(['- 1', '- 2', '- 3'])]
all_11th_like = all_11th_like[all_11th_like['n_pitch_classes'] == 6]
agg = aggregate_chords(all_11th_like)
#print(agg)

