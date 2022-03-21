# Computational Harmony v2

This python project assigns a brightness and darkness ordering to modes of the major, melodic minor, harmonic minor, and harmonic major scales.

Other applications or experiments included in this code repository include characterizing and ranking the brightness of all triad combos, of all 7th chords added to a root note, and all 59 possible dominant 7th chord extensions that are subsets of these 48 modes.

Scale network figures were generated with networkx and calculations were done wiith numpy and pandas.

## History

This repo started when I tried [answering my own question](https://music.stackexchange.com/questions/67293/ranking-dominant-chord-alterations-by-dissonance) about ranking dominant 7th extensions by dissonance.  I realized the notion of dissonance is hard to define and complicted, but I also started to appreciate brightness and darkness as a second axis that may be used for thinking about harmonies and scales.

## Defining brightness and darkness.

You may be familiar with the concept in music theory that locrian mode is darkest, lydian is brightest, and dorian is neutral. This is related to the circle of fifths, where going up a fourth is considered a transition from bright to dark. I was able to generalize the notion of brightness beyond major modes to the modes of melodic minor, harmonic minor, and harmonic major with the following simple equation:

```brightness = sum (pitch classes (mode_x)) - sum (pitch classes (Dorian))```

## Results

### Scale modes arranged along the brightness/darkness spectrum

I am considering scales close to C major and all of its modes.  By "close" I mean sharing 6 out of 7 common tones.  Because dorian is the most 'neutral' mode of the major scale (neutral in terms of brightness and darkness), I am also tabulating whether the root D of the dorian mode is in these scales.  The following diagram assigns brightness/darkness score to each of the modes

![modes_spreadsheet](figures/scale_modes_bright_dark.png)


These results are similar to the circle of fifths but generalized to three other jazz scale types.
You can see that for all parent scale types except major, the complete generalized circle of fifths requires passing through modes that lack the dorian root D. Altered scales have their rootless mode at the extremes of bright and dark (locrian and lydian), whereras for harmonic scales, the rootless modes occur at less extreme ends of the spectrum.  

Another interesting observation is that there is a staggered pattern of the three unique diminished seventh chords (considered equivalent under inversion) in the harmonic major and harmonic minor scales.

Perhaps the most useful finding (for negative harmony and jazz composition) is that the neutral modes of the four scale types are dorian (the second mode of themajor scale), mixolydian b6 (the fifth mode of the melodic minor scale), harmonic minor (the first mode of the eponymous parent scale), and mixolydian b2 (the fifth mode of the harmonic major scale).  
These modes can thus be used as a reference point for composing with brightness and darkness.  

The fact that dorian, mixolydian b6, harmonic minor, and mixolydian b2 are neutral centers is to my knowledge, not widely appreciated in the music theory literature.
Perhaps one could argue for systematic renaming of scales according to their graph-theoretical properties and apparent harmonic symmetry; however, the etymological origins of the names of scales most likely predates computers and graph theory, and musicians benefit from having conventions to communicate ideas. Further, they are used to having many names for the same chord (for example "min7b5" and "half-diminished" mean the same thing). Perhaps a new set off names should be proposed.

### directed graphs of scales 

Arrows between scales represent sharing 6 common tones and pointing from bright to dark. 

#### Major, harmonic major, and harmonic minor scales near C major. 

By plotting all 3 scale types (everything but the melodic minor modes) you can see the structure of the scale network fairly clearly.

![7 note pressing scale_network](figures/major_harmonic-maj_harmonic-min.png)

If you add the melodic minor modes (below) you can see the network becomes more complex in the sense that there are many overlapping edges.  The graph cannot be drawn without overlapping edges (graph theoreticians would say it is not a planar graph).

#### Network of 30 scales near C major. 

Network comprised of 7 harmonic minor, 7 harmonic major, and 9 melodic minor scales.

![30 scales](figures/7_note_pressing_scale_network.png)

#### Full cycle of 32 scales near C major. 

After adding F# harmonic minor and Eb harmonic major, two scales maximally distant from D dorian that contain the root D, you see a complete cycle emerges.

![32 scale cycle](figures/all_with_8_harmonic_maj-min.png)

### 18 scale transition rules for maximally smooth voice leading

By inspecting the scale networks and considering the relationships between the roots of the scales, the network is composed of 9 bright-to-dark transitions, or equivalently, 9 types of edges.  The 9 *dark-to-bright* transitions can be easily derived by inverting the dark transitions (by imagining the arrows point in the opposite direction).

Smooth voice leading is defined as transitioning between chords or scales by changing only a few notes by a small amount.  The 18 "maximally" smooth voice leading rules I have tabulated describe transitions where a single note is sharpened or flattened to transition to a new scale.  Smooth and maximally smooth voice leading is described in more detail in prior work by Dmitri Tymoczko in 2004 and Joseph Strauss in 2005 (see [References](#References)).

starting scale | bright or dark | # semitones | ending scale
-------------- | -------------- | ----------- | ------------
major          | dark           |  5          | major
major          | dark           |  0          | harmonic major
major          | dark           |  0          | melodic minor 
melodic minor  | dark           | -2          | major
melodic minor  | dark           |  0          | harmonic minor
harmonic major | dark           |  5          | melodic minor
harmonic major | dark           |  0          | harmonic minor
harmonic minor | dark           |  3          | major 
harmonic minor | dark           |  3          | harmonic major
major          | bright         | -5          | major
major          | bright         |  2          | melodic minor
major          | bright         | -3          | harmonic minor
melodic minor  | bright         |  0          | major
melodic minor  | bright         | -5          | harmonic major
harmonic major | bright         |  0          | major
harmonic major | bright         | -3          | harmonic minor
harmonic minor | bright         |  0          | melodic minor
harmonic minor | bright         |  0          | harmonic major

According to these rules, for every major scale, you can transition to 3 scales by flattening one note a single half step (3 maximally smooth bright-to-dark transitions).  
For the three other scale types--melodic minor, harmonic minor, and harmonic major, you can transition to only two other scales by flattening a single note.
Surprisingly yet satisfyingly, for *dark-to-bright* transitions with *sharpening* a single note, the number of transitions from each starting scale type is identical to that for the *bright-to-dark* transitions, although the destination scale types are different. Symmetry.  
Overall, the finding that there are more rules starting from major scale than the 3 other scale types suggests melodic minor, harmonic minor, and harmonic major scales are less versatile in terms of voice leading opportunities.  This may be part of why they are perceived as more dissonant than the major scales (in my personal experience, citation needed).

These maximally smooth scale transitions could be used as rules for creating generative jazz compostions with a hidden markov model, for example, using the dictionary I have constructed in [this python file](code/scale_change_rules.py).  Or they may assist with choosing modulations in traditional jazz composition.


## References

Tymoczko, Dmitri. "Scale networks and Debussy." Journal of Music Theory 48.2 (2004): 219-294.

Straus, Joseph N. "Voice leading in set-class space." Journal of Music Theory 49.1 (2005): 45-108.
