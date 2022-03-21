note_names = ['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B']

major = [0,2,4,5,7,9,11]
melodic_minor = [0,2,3,5,7,9,11]
harmonic_major = [0,2,4,5,7,8,11]
harmonic_minor = [0,2,3,5,7,8,11]
# symmetric
octatonic = [0,1,3,4,6,7,9,10]
augmented = [0,3,4,7,8,11]
wholetone = [0,2,4,6,8,10]


def transpose(scale, n):
    return [(x + n) % 12 for x in scale]

def n_common_tones(scale_a, scale_b):
    inters = set(scale_a).intersection( set(scale_b))
    return len(inters)

def build_scale_dict():

    scale_dict = {}
    for degree, note in enumerate(note_names):
        scale_dict[(note_names[degree], 'major')] = transpose(major, degree)
        scale_dict[(note_names[degree], 'melodic_minor')] =\
                transpose(melodic_minor, degree)
        scale_dict[(note_names[degree], 'harmonic_major')] =\
                transpose(harmonic_major, degree)
        scale_dict[(note_names[degree], 'harmonic_minor')] =\
                transpose(harmonic_minor, degree)
        if note in ['C', 'F', 'G']:
            scale_dict[(note_names[degree], 'octatonic')] =\
                    transpose(octatonic, degree)
        if note in ['C', 'F', 'G', 'Bb']:
            scale_dict[(note_names[degree], 'augmented')] =\
                    transpose(augmented, degree)
        if note in ['C', 'F']:
            scale_dict[(note_names[degree], 'wholetone')] =\
                    transpose(wholetone, degree)
    return scale_dict

scale_dict = build_scale_dict()

minor_pentatonic = [0, 3, 5, 7, 10]

def print_minor_penta_intersections():
    penta_dist = {}
    for scale, notes in scale_dict.items():
        penta_dist[scale] = n_common_tones(notes, minor_pentatonic)
    
    for i in reversed(range(6)):
        print(i)
        sub_dict = {k : v for k,v in penta_dist.items() if v == i}
        print(sub_dict)

def print_minor_penta_perfect_fits():
    """ only perfect overlaps
    [0, 3, 5, 7] overlapping scales, [0, 3, 7, 10] overlapping scales, etc.
    """
    for r in range(0,5):
        penta_sub = [x for i, x in enumerate(minor_pentatonic) if i!=r] 
        penta_dist = {}
        for scale, notes in scale_dict.items():
            penta_dist[scale] = n_common_tones(notes, penta_sub)
            sub_dict = {k : v for k,v in penta_dist.items() if v == 4}
        print(penta_sub)
        for x in sub_dict.keys():
            print(x)

    
