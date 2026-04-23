#!/bin/bash

# Align BUSCO genes
for i in *.reformatted; do mafft $i > ${i}.aln; done

# Trim alignments 
for i in *.aln; do trimal -i $i -out ${i}.trim -gappyout; done

#Concatenate 
ls *.trim > fastas.txt
phykit cc -a fastas.txt -p concat_fasta

# Build Phylogenetic tree 
iqtree -s concat_fasta.fa -m LG+G4 -B 1000