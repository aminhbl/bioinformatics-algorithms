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

<!-- ABOUT THE PROJECT -->
## Overview

This is the implementation of three of the most important algorithms that every student interested in the field of Bioinformatics should know (my humble opinion!).  

<!-- <h3 align="left">Semi-Global Alignment</h3> -->
## <i> Semi-Global Alignment </i>
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