import os
import sys
import argparse
import pymol
from pymol import cmd

def analyze_cif_contacts(directory_path, distance_threshold):
    """
    Parses a directory of CIF files using PyMOL and counts how many structures
    have specific residue interactions within the distance threshold.
    """
    
    # Define PyMOL selection strings. 
    # We explicitly exclude hydrogens ('not elem H') to avoid false positive clashes.
    sel1 = "(chain K and resi 11+12+13) and not elem H"
    
    sel2 = "(((chain C+G and resi 46+51+54+62+80+81+82) or " \
           "(chain D+H and resi 20+74+82))) and not elem H"
           
    # The 'within' operator syntax: "Select atoms in sel1 that are within X Å of sel2"
    contact_query = f"({sel1}) within {distance_threshold} of ({sel2})"

    interaction_count = 0
    total_processed = 0

    print(f"Scanning directory: {directory_path} for contacts < {distance_threshold} Å...")

    for filename in os.listdir(directory_path):
        if filename.endswith(".cif"):
            filepath = os.path.join(directory_path, filename)
            
            try:
                # Load the structure into PyMOL, assigning it the object name "struct"
                cmd.load(filepath, "struct")
                
                # cmd.select executes the selection and returns the number of matching atoms
                # We suppress the selection output in the console using quiet=1
                atoms_in_contact = cmd.select("contact_atoms", contact_query, quiet=1)
                
                # If at least one atom meets the criteria, we count it as a positive interaction
                if atoms_in_contact > 0:
                    interaction_count += 1
                
                total_processed += 1
                
                # Progress tracker
                if total_processed % 100 == 0:
                    print(f"Processed {total_processed} files...")
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                
            finally:
                # Crucial: Clear PyMOL's memory after each file to prevent RAM exhaustion
                cmd.delete("all")

    # Final Report
    print("-" * 40)
    print("ANALYSIS COMPLETE")
    print("-" * 40)
    print(f"Total CIF files processed: {total_processed}")
    print(f"Structures with an interaction: {interaction_count}")
    
    if total_processed > 0:
        percentage = (interaction_count / total_processed) * 100
        print(f"Percentage: {percentage:.2f}%")

if __name__ == "__main__":
    # --- SETUP COMMAND LINE ARGUMENTS ---
    parser = argparse.ArgumentParser(description="Analyze CIF files for specific chain contacts using PyMOL.")
    
    # Required positional argument for the directory
    parser.add_argument("directory", help="Path to the folder containing the CIF files")
    
    # Optional argument for the distance threshold (defaults to 5.0)
    parser.add_argument("-t", "--threshold", type=float, default=5.0, 
                        help="Distance threshold in Angstroms (default: 5.0)")
    
    args = parser.parse_args()

    # Validate that the provided directory exists
    if not os.path.isdir(args.directory):
        print(f"Error: The directory '{args.directory}' does not exist.")
        sys.exit(1)

    # --- LAUNCH PYMOL HEADLESSLY ---
    # -c : command line only (no GUI)
    # -q : quiet launch (suppresses splash screen text)
    pymol.pymol_argv = ['pymol', '-cq']
    pymol.finish_launching()
    
    # Run the analysis with the provided arguments
    analyze_cif_contacts(args.directory, args.threshold)
    
    # Quit PyMOL when done
    cmd.quit()
