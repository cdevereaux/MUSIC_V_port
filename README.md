# MUSIC_V_port

## Description
An implementation of the Music V audio programming language written in Python. Based on the gfortran version at https://github.com/vlazzarini/MUSICV/ and the description of the original software given in Max Matthew's book, The Technology of Computer Music, a pdf of which may be found here: https://bitsavers.informatik.uni-stuttgart.de/pdf/bellLabs/The_Technology_of_Computer_Music_1969.pdf .

## Remaining Milestones

1. Add support for PLF, PLS, and CONVT subroutines and metronomic operations.
2. Implement a system by which aliases may be provided for the user-defined subroutines used in a given score. Allowing multiple scores to be computed without modifying the source code. Create one or two examples for this.
3. Add support for more scores, such as some of those found here: https://github.com/vlazzarini/MUSICV/tree/cprog-lb/scores

These milestones will be tested by comparing the generated audio with that generated by vlazzarini's version.

## How To Run
```
python path_to_music5.py path_to_score_file
```
Note: PLF, PLS, and CONVT subroutines and metronomic operations are not yet supported. **Requires python version 3.10 or greater.**
