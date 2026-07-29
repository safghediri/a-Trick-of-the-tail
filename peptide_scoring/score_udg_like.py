#!/usr/bin/env python3
"""Score 15-aa UDG-like candidate peptides against the human UNG2 RKR region.

Input CSV columns:  UniProt,Peptide
Output CSV columns: UniProt,Peptide,Score_global_new,Align_norm,
                    Center_score_new,Charge,SerPro_fraction
"""

import csv
from pathlib import Path

REFERENCE_UDG = "FSPSPARKRHAPSPE"  # human UNG2 residues 11-25; RKR at 17-19
VALID_AA = set("ACDEFGHIKLMNPQRSTVWY")
CONSERVATIVE = {frozenset(("R", "K")), frozenset(("D", "E")), frozenset(("S", "T"))}


def alignment_score(peptide):
    score = 0
    for observed, reference in zip(peptide, REFERENCE_UDG):
        if observed == reference:
            score += 2
        elif frozenset((observed, reference)) in CONSERVATIVE:
            score += 1
        else:
            score -= 1
    return score / 30.0


def central_motif_score(peptide):
    central_region = peptide[6:11]  # positions 7-11 of the 15-aa window
    triplets = {central_region[i:i + 3] for i in range(3)}
    if "RKR" in triplets:
        return 1.0
    # RRR is also treated as a partial RKR-like match, matching udg_like_scores.csv.
    if triplets.intersection({"KRK", "RRK", "RKK", "KKR", "RRR"}):
        return 0.5
    return 0.0


def charge_score(peptide):
    return ((peptide.count("R") + peptide.count("K")) - (peptide.count("D") + peptide.count("E"))) / 15.0


def serpro_fraction(peptide):
    return (peptide.count("S") + peptide.count("P")) / 15.0


def score(peptide):
    align = alignment_score(peptide)
    center = central_motif_score(peptide)
    charge = charge_score(peptide)
    serpro = serpro_fraction(peptide)
    total = 0.5 * align + 0.3 * center + 0.1 * charge + 0.1 * serpro
    return total, align, center, charge, serpro


def main():
    here = Path(__file__).resolve().parent
    input_path = here / "Data_set.csv"
    output_path = here / "udg_like_scores.csv"
    scored_rows = []
    skipped = []

    with input_path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            peptide = row["Peptide"].strip().upper()
            if len(peptide) != 15 or not set(peptide).issubset(VALID_AA):
                skipped.append(row["UniProt"])
                scored_rows.append({
                    "UniProt": row["UniProt"], "Peptide": peptide,
                    "Score_global_new": "", "Align_norm": "", "Center_score_new": "",
                    "Charge": "", "SerPro_fraction": "",
                })
                continue
            total, align, center, charge, serpro = score(peptide)
            scored_rows.append({
                "UniProt": row["UniProt"], "Peptide": peptide,
                "Score_global_new": round(total, 3), "Align_norm": round(align, 3),
                "Center_score_new": center, "Charge": round(charge, 3),
                "SerPro_fraction": round(serpro, 3),
            })

    scored_rows.sort(key=lambda row: row["Score_global_new"] if isinstance(row["Score_global_new"], float) else float("-inf"), reverse=True)
    fields = ["UniProt", "Peptide", "Score_global_new", "Align_norm", "Center_score_new", "Charge", "SerPro_fraction"]
    with output_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(scored_rows)
    print(f"Wrote {len(scored_rows)} motifs to {output_path.name}.")
    if skipped:
        print(f"Skipped {len(skipped)} incomplete/unresolved motifs: {', '.join(skipped)}")


if __name__ == "__main__":
    main()
