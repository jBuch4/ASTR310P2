import pandas as pd

def hms_to_decimal(hms_str, is_ra=True):
    """
    Converts an RA or Dec value from 'HH:MM:SS.SS' or 'DD:MM:SS.SS' format to decimal degrees.
    
    Parameters:
    - hms_str: string, RA or Dec in 'HH:MM:SS.SS' or 'DD:MM:SS.SS' format.
    - is_ra: boolean, if True, treats hms_str as RA; if False, treats it as Dec.
    
    Returns:
    - float, decimal degrees representation of the input value.
    """
    parts = hms_str.strip().split(':')
    
    # Ensure each component has a value, default to 0 if missing or invalid
    hours_or_deg = float(parts[0].strip()) if parts[0].strip() else 0
    minutes = float(parts[1].strip()) if len(parts) > 1 and parts[1].strip() else 0
    seconds = float(parts[2].strip()) if len(parts) > 2 and parts[2].strip() else 0

    if is_ra:
        # Convert RA: hours to degrees (1 hour = 15 degrees)
        return 15 * (hours_or_deg + minutes / 60 + seconds / 3600)
    else:
        # Convert Dec: degrees remain as degrees
        return hours_or_deg + (minutes / 60) + (seconds / 3600)


def write_ipac_table_from_csv(data, output_file='cv_table.ipac'):
    """
    Takes CV data from DataFrame, extracts RA and Dec, and writes them to an IPAC-format table file.

    Parameters:
    - input_file: string, the path to the CSV file with CV data.
    - output_file: string, the name of the output IPAC file (default is 'cv_table.ipac').
    """
    
    ra_values = data.iloc[:, 1].apply(hms_to_decimal, is_ra=True)
    dec_values = data.iloc[:, 2].apply(hms_to_decimal, is_ra=False)

    # Define the column headers for the IPAC table format
    headers = ["|    ra        |     dec      |",
"|    double    |     double   |"]

    # Open the file and write header informat
    with open(output_file, 'w') as file:
        #file.write("\\ |CVs in Galactic Bulge|\n")

        # Write column headers
        for header in headers:
            file.write(header + '\n')

        # Write separator row (required in IPAC format)
        #file.write("|---------|------|\n")

        # Write data rows
        for ra, dec in zip(ra_values, dec_values):
            file.write(f"    {ra:<11.6f}  {dec:<11.6f}\n")


    print(f"IPAC table created successfully: {output_file}")




def BulgeDisk(file):
    """
    Takes csv files, reads to a pandas dataframe, creates three dataframes, one for each region
    
    l: Galactic Longitude
    b: Galactic Latitude
    """
    
    # Read the csv with the data and columns aligned properly, but removes the column names
    data_csv = pd.read_csv(file, header=None, skiprows=1, usecols=(range(0,32)))
    
    # Read and reassign column names
    colnames = pd.read_csv(file, skiprows=0, header=0).columns
    data_csv.columns = colnames
    
    # Drop Indices with nan l or b
    data_csv = data_csv.dropna(subset=('l','b'))
    
    
    
    # Creates dataframes based on positional constraints using Galactic Coordinates
    
    # CV is in the bulge
    inBulge = data_csv[(data_csv['b'].abs() <= 7) & ((data_csv['l'] <= 7) | (data_csv['l'] >= 353))]
    
    
    # CV is in the disk
    inDisk = data_csv[(data_csv['b'].abs() < 7) & ( ((data_csv['l'] > 7) & (data_csv['l'] < 353)) )]

    
    # CV is in the halo
    inHalo = data_csv[(data_csv['b'].abs() > 10)]
    

    
    
    return data_csv, inBulge, inDisk, inHalo
    
    





input_file = 'C:/Users/Owner/PhysicsSims/ASTR310/Project 2/stscicat.txt'

data, inBulge, inDisk, inHalo = BulgeDisk(input_file)

write_ipac_table_from_csv(inDisk, output_file='inDisk.ipac')
write_ipac_table_from_csv(inBulge, output_file='inBulge1.ipac')
write_ipac_table_from_csv(inHalo, output_file='inHalo.ipac')










