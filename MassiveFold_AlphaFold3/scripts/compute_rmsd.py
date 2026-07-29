import sys
import argparse
import csv
import statistics
from pathlib import Path

# Import PyMOL 
import pymol
from pymol import cmd

def compute_batch_rmsd(cif_folder, output_csv="rmsd_results.csv"):
    # Initialize PyMOL in headless mode (no GUI, quiet)
    pymol.pymol_argv = ['pymol', '-cq']
    pymol.finish_launching()
    
    reference_name = "1emh"
    print(f"Fetching reference structure: {reference_name.upper()}...")
    
    # Fetch the reference structure directly from the PDB
    try:
        cmd.fetch(reference_name)
    except Exception as e:
        print(f"Error fetching {reference_name}: {e}")
        sys.exit(1)
    
    # Validate the directory
    folder_path = Path(cif_folder)
    if not folder_path.is_dir():
        print(f"Error: Directory '{cif_folder}' does not exist.")
        cmd.quit()
        sys.exit(1)
        
    # Gather all .cif files in the directory
    cif_files = list(folder_path.glob("*.cif"))
    if not cif_files:
        print(f"No '.cif' files found in '{cif_folder}'.")
        cmd.quit()
        sys.exit(0)
        
    print(f"Found {len(cif_files)} CIF files. Computing RMSD (5 cycles) against {reference_name.upper()}...\n")
    
    rmsd_values = []
    
    # Open CSV file for writing
    with open(output_csv, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header
        writer.writerow(["CIF_File", "RMSD"])
        
        # Iterate over each CIF file
        for cif_file in cif_files:
            target_name = cif_file.stem
            
            # Load the target structure into PyMOL
            cmd.load(str(cif_file), target_name)
            
            try:
                # cmd.align returns a 7-item tuple. Index 0 is the RMSD.
                result = cmd.align(mobile=target_name, target=reference_name, cycles=5)
                
                rmsd_val = result[0]
                rmsd_values.append(rmsd_val)
                
                # Write to CSV
                writer.writerow([cif_file.name, rmsd_val])
                print(f"Processed: {cif_file.name:<25} | RMSD: {rmsd_val:.4f}")
                
            except Exception as e:
                print(f"Failed: {cif_file.name:<25} | Error during alignment: {e}")
                
            finally:
                # Delete the target object to free memory for the next iteration
                cmd.delete(target_name)

    # Calculate and output the median RMSD
    if rmsd_values:
        median_rmsd = statistics.median(rmsd_values)
        mean_rmsd = statistics.mean(rmsd_values)
        print("-" * 45)
        print(f"Results saved to: {output_csv}")
        print(f"Median RMSD across all files: {median_rmsd:.4f} Å")
        print(f"Mean RMSD across all files: {mean_rmsd:.4f} Å")
    else:
        print("\nNo successful alignments to calculate median.")

    # Quit PyMOL safely
    cmd.quit()

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Compute RMSD (5 cycles) between 1EMH and a folder of CIF files.")
    parser.add_argument("folder", help="Path to the directory containing the target .cif files")
    parser.add_argument("--output", default="rmsd_results.csv", help="Optional: Name of the output CSV file (default: rmsd_results.csv)")
    
    args = parser.parse_args()
    
    compute_batch_rmsd(args.folder, args.output)
