import numpy as np
import matplotlib.pyplot as plt

#%%
def read_eigenval(file_path):
    """
    Reads the EIGENVAL file and extracts k-points and band energies.
    Returns k-points and band energies as lists.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Read the header information
    header = lines[0].split()
    num_kpoints = int(header[0])  # Number of k-points
    num_bands = int(header[1])    # Number of bands

    # Skip the first 7 lines of metadata
    index = 7

    kpoints = []
    bands = []

    # Read each k-point and the corresponding band energies
    for i in range(num_kpoints):
        # Read the k-point line (the first line contains k-point coordinates)
        kpoint_line = lines[index].split()
        
        # Check if the k-point line has the required number of elements
        if len(kpoint_line) < 3:
            print(f"Warning: k-point line at index {index} is incomplete: {kpoint_line}")
            continue

        kpoints.append([float(x) for x in kpoint_line[:3]])  # Only take the first 3 values (k-point coordinates)
        index += 1

        # Read the band energies for this k-point
        kpoint_bands = []
        for j in range(num_bands):
            band_line = lines[index].split()
            print(band_line)
            
            # Check if the band line has enough elements
            if len(band_line) < 2:
                print(f"Error: Band line at index {index} is incomplete: {band_line}")
                raise IndexError(f"Band line at index {index} is incomplete.")

            # Now using index 1 for the band energy (2nd value)
            band_energy = float(band_line[1])  
            kpoint_bands.append(band_energy)
            print(index)
            index += 1
        
        bands.append(kpoint_bands)

    return kpoints, bands

#%%
def write_band_file(kpoints, bands, output_path):
    """
    Writes the .band file for CASTEP based on k-points and band energies.
    """
    num_kpoints = len(kpoints)
    num_bands = len(bands[0]) if bands else 0

    with open(output_path, 'w') as f:
        # Write header information: number of k-points and number of bands
        f.write(f"{num_kpoints} {num_bands}\n")
        
        for i, kpoint in enumerate(kpoints):
            # Write k-point coordinates (3 values)
            f.write(f"{' '.join(f'{coord:.8f}' for coord in kpoint)}\n")
            
            # Write the band energies at this k-point
            f.write(f"{' '.join(f'{energy:.8f}' for energy in bands[i])}\n")

#%%
def convert_eigenval_to_band(eigenval_path, output_band_path):
    """
    Main conversion function from EIGENVAL (VASP) to .band (CASTEP).
    """
    kpoints, bands = read_eigenval(eigenval_path)
    write_band_file(kpoints, bands, output_band_path)

#%%
# Example usage:
eigenval_file = 'EIGENVAL'  # Path to the VASP EIGENVAL file
output_band_file = 'output.band'  # Path to the output .band file

convert_eigenval_to_band(eigenval_file, output_band_file)