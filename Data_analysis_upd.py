
import numpy as np
import pandas as pd
from astropy.io import ascii
import os

def readTable(file):
    
    # Define the filename and make sure it reads from the working directory
    filename = file  # Replace this with the name of your IPAC file
    file_path = os.path.join(os.path.dirname(__file__), filename)
    
    # Read the IPAC table into an Astropy Table and then into a Pandas DataFrame
    
    converters = {'oid': np.int64} # Need to define the converter for the OID, otherwise it freaks out ¯\_(ツ)_/¯
    ipac_table = ascii.read(file_path, format='ipac', converters = converters)
    df = ipac_table.to_pandas()
    
    print("Data successfully saved to the database.")
    
    return df


def pickSelectedSources(ztf_data, oid_csv):
    
    # Create a dataframe of the only the data of selected sources by selecting rows based on the OIDs
    
    selected_sources = ztf_data[ztf_data['oid'].isin(oid_csv['id_col'])]
    
    return selected_sources


def magDiff(data):
    """
    Adds a new column 'mag_difference' to the DataFrame, which is the difference
    between the 'medianmag' and 'minmag' columns.

    """
    n = len(data)


    data['eruption'] = data['medianmag'] - data['minmag']

    # Calculate the propagated error
    data['eruption_err'] = np.sqrt(2*data['medmagerr']**2)

    return data, n



# Read in ZTF Data
bf = readTable('inBulge_ztf_data.txt') # ZTF Data of Bulge CVs
df = readTable('inDisk_ztf_data.txt') # ZTF Data of Disk CVs
hf = readTable('inHalo_ztf_data.txt') # ZTF Data of Halo CVs


# Read in CSVs of Selected Sources OIDs
diskCVLC = pd.read_csv(os.path.join(os.path.dirname(__file__), 'diskCV_LC.csv'))
bulgeCVLC = pd.read_csv(os.path.join(os.path.dirname(__file__), 'bulgeCV_LC.csv'))
haloCVLC = pd.read_csv(os.path.join(os.path.dirname(__file__), 'haloCV_LC.csv'))


# Creates list of Selected CVs Data
df_data = pickSelectedSources(df, diskCVLC) # Data of Selected Disk CVs
bf_data = pickSelectedSources(bf, bulgeCVLC) # Data of Selected Bulge CVs
hf_data = pickSelectedSources(hf, haloCVLC) # Data of Selected Halo CVs


def results(data, name):
    
    # Find the average eruption mag. and its uncertainty for each region
    
    d, n = magDiff(data)

    avg = d['eruption'].mean()

    sq_err = data['eruption_err']**2
    sem = np.sqrt(sq_err.sum()) / n

    print(f"\n{name} average: {avg}, Error: {sem}\n")
    
    
results(df_data, "Disk")
results(bf_data, "Bulge")
results(hf_data, "Halo")


# Print Histogram of Eruption Magnitudes
import matplotlib.pyplot as plt

plt.figure()
plt.hist(df_data['eruption'], bins=20, range=(0,6.15))
plt.xlabel("Eruption Magnitude")
plt.ylabel("Counts")
plt.title("Eruption Magnitudes of CVs in the Disk")

plt.figure()
plt.hist(bf_data['eruption'], bins=20, range=(0,6.15))
plt.xlabel("Eruption Magnitude")
plt.ylabel("Counts")
plt.title("Eruption Magnitudes of CVs in the Bulge")

plt.figure()
plt.hist(hf_data['eruption'], bins=20, range=(0,6.15))
plt.xlabel("Eruption Magnitude")
plt.ylabel("Counts")
plt.title("Eruption Magnitudes of CVs in the Halo")


# Print Boxplots of Eruption Magnitudes
plt.figure()
plt.boxplot((df_data['eruption'], hf_data['eruption'], bf_data['eruption']), 
            labels=["Disk CVs", "Halo CVs", "Bulge CVs"])
plt.ylabel('Eruption Magnitude')
plt.title("Eruption Magnitude of CVs in the 3 Regions of the Milky Way")






