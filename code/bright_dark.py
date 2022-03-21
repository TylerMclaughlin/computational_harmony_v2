import pandas as pd
from pressing_modes import pruned_bd
from pressing_scales_common_tones import scale_dict

#print(pruned_bd)

# arrange manually 
rel_scales = {k : v for k, v in scale_dict.items() if k in pruned_bd.columns}
#print(len(rel_scales))

def absolute_brightness(notes):
    # subtract 2 because everything relative to d dorian.  we want the root to be zero
    notes = [(n - 2)%12 for n in notes]
    return sum(notes)

def build_abs_brightness():
    list_of_dicts = []
    for s, ns in rel_scales.items():
        root = s[0]
        scale_type = s[1]
        ab = absolute_brightness(ns) - 36 # 36 is the brightness of C
        contains_root = (2 in ns)
        scale_entry = {'root' : root, 'scale_type' : scale_type, 'brightness' : ab, 'contains_root' : contains_root, 'notes' : ns}
        list_of_dicts.append(scale_entry)
    df = pd.DataFrame(list_of_dicts)
    return df

bd = build_abs_brightness()


common_names = []
common_names.append({'root' : 'A', 'scale_type' : 'major',  'common_name' : 'Lydian'})
common_names.append({'root' : 'D', 'scale_type' : 'major',  'common_name' : 'Ionian'})
common_names.append({'root' : 'G', 'scale_type' : 'major',  'common_name' : 'Mixolydian'})
common_names.append({'root' : 'C', 'scale_type' : 'major',  'common_name' : 'Dorian'})
common_names.append({'root' : 'F', 'scale_type' : 'major',  'common_name' : 'Aeolian'})
common_names.append({'root' : 'Bb', 'scale_type' : 'major',  'common_name' : 'Phrygian'})
common_names.append({'root' : 'Eb', 'scale_type' : 'major',  'common_name' : 'Locrian'})

common_names.append({'root' : 'B', 'scale_type' : 'melodic_minor',  'common_name' : 'Lydian #5'})
common_names.append({'root' : 'E', 'scale_type' : 'melodic_minor',  'common_name' : 'Ionian #1'})
common_names.append({'root' : 'A', 'scale_type' : 'melodic_minor',  'common_name' : 'Lydian Dominant'})
common_names.append({'root' : 'D', 'scale_type' : 'melodic_minor',  'common_name' : 'Melodic Minor'})
common_names.append({'root' : 'G', 'scale_type' : 'melodic_minor',  'common_name' : 'Mixolydian b6'})
common_names.append({'root' : 'C', 'scale_type' : 'melodic_minor',  'common_name' : 'Dorian b2'})
common_names.append({'root' : 'F', 'scale_type' : 'melodic_minor',  'common_name' : 'Aeolian b5'})
common_names.append({'root' : 'Bb', 'scale_type' : 'melodic_minor',  'common_name' : 'Phrygian b1'})
common_names.append({'root' : 'Eb', 'scale_type' : 'melodic_minor',  'common_name' : 'Altered'})

common_names.append({'root' : 'F#', 'scale_type' : 'harmonic_minor',  'common_name' : 'Lydian #2'})
common_names.append({'root' : 'B', 'scale_type' : 'harmonic_minor',  'common_name' : 'Ionian #5'})
common_names.append({'root' : 'E', 'scale_type' : 'harmonic_minor',  'common_name' : 'Mixolydian #1'})
common_names.append({'root' : 'A', 'scale_type' : 'harmonic_minor',  'common_name' : 'Dorian #4'})
common_names.append({'root' : 'D', 'scale_type' : 'harmonic_minor',  'common_name' : 'Harmonic Minor'})
common_names.append({'root' : 'G', 'scale_type' : 'harmonic_minor',  'common_name' : 'Phrygian #3'})
common_names.append({'root' : 'C', 'scale_type' : 'harmonic_minor',  'common_name' : 'Locrian #6'})
common_names.append({'root' : 'Eb', 'scale_type' : 'harmonic_minor',  'common_name' : 'Altered b7'})

common_names.append({'root' : 'F#', 'scale_type' : 'harmonic_major',  'common_name' : 'Lydian #5 #2'})
common_names.append({'root' : 'A', 'scale_type' : 'harmonic_major',  'common_name' : 'Lydian b3'})
common_names.append({'root' : 'D', 'scale_type' : 'harmonic_major',  'common_name' : 'Harmonic major'})
common_names.append({'root' : 'G', 'scale_type' : 'harmonic_major',  'common_name' : 'Mixolydian b2'})
common_names.append({'root' : 'C', 'scale_type' : 'harmonic_major',  'common_name' : 'Dorian b5'})
common_names.append({'root' : 'F', 'scale_type' : 'harmonic_major',  'common_name' : 'Aeolian b1'})
common_names.append({'root' : 'Bb', 'scale_type' : 'harmonic_major',  'common_name' : 'Phrygian b4'})
common_names.append({'root' : 'Eb', 'scale_type' : 'harmonic_major',  'common_name' : 'Locrian b7'})

cdf = pd.DataFrame(common_names)

bd = pd.merge(cdf, bd, on = ['root', 'scale_type'], how = 'inner' )

bd.sort_values(by = ['contains_root','brightness', 'scale_type'], inplace = True)

bd.to_csv('all_seven_note_modes_sorted_dark_to_bright.csv')
print(bd)


