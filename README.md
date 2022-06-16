<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">

<h2 align="center">Bioinformatics Algorithms</h2>

  <p align="center">
    Three fundemental algorithms of bioinformatics
  </p>
  <br>
</div>

## Quick links

* [Overview](#overview)
* [Semi-Global Alignment](#semi-global-alignment)
    * [Quick start](#quick-start)
* [Block-Based Star Alignment](#block-based-star-alignment)
    * [Quick Start](#quick-start-1)
* [Profile-Based Alignment](#profile-based-alignment)
    * [Quick Start](#quick-start-2)

<!-- ABOUT THE PROJECT -->
## Overview

This is the implementation of three of the most important algorithms that every student interested in the field of Bioinformatics should know (my humble opinion!).  

<!-- <h3 align="left">Semi-Global Alignment</h3> -->
## Semi-Global Alignment
First we initilize and fill in the <b> scoring maxtrix </b> since we're following the <i> Dynamic Programming </i> approach. The idea is that the score of the best possible alignment that ends at `(i, j)` in matrix, is equal to the score of best alignment ending just previous to those positions `(i-1, j-1)`, plus the score for aligning `Xi` and `Yj` (residue `i` in protein sequence `X` and residue `j` in protein seequence `Y`). 
<br>
For scoring we use `PAM250` to calculate Match and Mismatch and consider a fixed score of -9 for gaps. 
<br>
After finding the score of optimum alignment, which would be the highest score in bottom row or right-hand column of the matrix, we <b> trace back </b> through the matrix to recover that optimum alignment.

## Quick Start
Input two protein sequence with maximum length of 100 residues in capital letters. 

```bash
HEAGAWGHE
PAWHEA
```
Output will be the score of the alignment along with the pairwise aligned sequences.
```bash
20
HEAGAWGHE-
---PAW-HEA
```

## Block-Based Star Alignment
First we perform <b>Star Alignment</b> by finding the pariwise alignment scores for each pair of protein sequences and form the distance matrix. Then we pick the center sequence based on the minimum total of distances for each sequence. Then sequences will be added to get aligned in dicreasing order of similarity (increase of distance) in respect to the center sequence.
<br>
Now to have better alignment for more divergent sequences we improve on the multiple sueqence alignemnt that we have achived by performing <b>Block Based</b> alignment. This is how we do this:
<br>
we find blocks with minimum two columns within the alignment containing gaps or mismatches, then apply the `star_alignment` for these blocks alone. If realignment of any block improves the overall score of total alignments we switch to the realigned block.
## Quick Start
Input number of protein sequences to be aligned and then each sequence in separate line with capital letters.

```bash
5
TAGCTACCAGGA
CAGCTACCAGG
TAGCTACCAGT
CAGCTATCGCGGC
CAGCTACCAGGA
```
Output will be the overall score of the multiple sequence alignment and aligned sequences in each line respectively to the input sequence.

```bash
240
TAGCTA-C-CAGGA
CAGCTA-C-CAGG-
TAGCTA-C-CA-GT
CAGCTATCGC-GGC
CAGCTA-C-CAGGA
```

## Profile-Based Alignment
Here we construct a statistical model by first building a profile using the given multiple sequenses, calculating the probability of appearance for each residue at it's respective position. In this process we use pseudocount of `2` to avoid the zero probability. After that we will localy align a given long sequence to previous multiple sequences using the profile for scoring the alignment and then report the subsequence with the highest score of alignment.

## Quick Start
Input number of multiple sequences to build a profile from. After that each sequence should be in separate lines followed by the long sequence.

```bash
4
HVLIP
H-MIP
HVL-P
LVLIP
LIVPHHVPIPVLVIHPVLPPHIVLHHIHVHIHLPVLHIVHHLVIHLHPIVL
```
output will show the aligned subsequence with highest score.

```bash
H-L-P
```