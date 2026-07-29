UDG-like peptide scoring

This folder contains the sequence-based scoring workflow used to identify 15-residue candidate peptides with features similar to the N-terminal RKR-containing region of human UNG2.

Files

Data_set.csv - input dataset. Each row contains a UniProt accession and one 15-residue peptide window.

score_udg_like.py - Python script that calculates the component scores and the final score.

udg_like_scores.csv - scored output table generated from the input dataset.

Requirements

The workflow uses only the Python standard library. Python 3 is sufficient; no additional packages are required.

Run the scoring

Place the three files in the same directory. The script currently expects the input file to be named Data_set.csv and writes udg_like_scores.csv.

Therefore, either rename the input file before running:

mv your_file.csv Data_set.csv
python3 score_udg_like.py

or change the two filename definitions in the main() function of the script to use your_file.csv as input and your_scores.csv as output.

The output is sorted from the highest to the lowest global score.
