import pickle
import pandas as pd
import gzip
import re
from typing import Dict, List
import sys

def parse_uniref50_xml_targeted(xml_file_path: str) -> Dict[str, str]:
    """
    Parse UniRef50 XML file and create a dictionary mapping UniProtKB IDs to UniRef50 IDs
    
    Args:
        xml_file_path (str): Path to the uniref50.xml.gz file
    Returns:
        Dict[str, str]: Dictionary with UniProtKB accession as key and UniRef50 ID as value
    """
    uniprot_to_uniref = {}
    
    print(f"Creating UniprotKB:Uniref50 dictionary...")
    
    try:
        # Open the gzipped XML file
        print('Opening xml file...')
        with gzip.open(xml_file_path, 'rt', encoding='utf-8') as file:
            print('Opened xml file.')
            current_cluster_name = None
            temp_uniprot_list = []
            line_count = 0
            entries_processed = 0
            
            # Regular expressions for pattern matching
            entry_pattern = re.compile(r'<entry id="UniRef50_([^"]+)"')
            accession_pattern = re.compile(r'<property type="UniProtKB accession" value="([^"]+)"')
            
            for line in file:
                line_count += 1
                line = line.strip()
                
                # Progress indicator
                if line_count % 1000000 == 0:
                    print(f"Processed {line_count:,} lines, {entries_processed:,} entries, {len(uniprot_to_uniref):,} mappings")
                
                # Check if line contains an 'entry id' like <entry id="UniRef50_A0AB34IYJ6"
                entry_match = entry_pattern.search(line)
                if entry_match:
                    # If we had a previous cluster, save all its UniProt IDs
                    if current_cluster_name and temp_uniprot_list:
                        for uniprot_id in temp_uniprot_list:
                            uniprot_to_uniref[uniprot_id] = f"UniRef50_{current_cluster_name}"
                        entries_processed += 1
                    
                    # Start new cluster
                    current_cluster_name = entry_match.group(1)  # Get part after UniRef50_
                    temp_uniprot_list = []  # Reset temporary list
                    continue
                
                # Now for every following line see if there is a "UniProtKB accession" value="A0AB34IYJ6"
                if current_cluster_name:  # Only look for accessions if we're in a cluster
                    accession_match = accession_pattern.search(line)
                    if accession_match:
                        # Save this value to a temporary list
                        uniprot_id = accession_match.group(1)
                        temp_uniprot_list.append(uniprot_id)
            
            # Don't forget the last cluster after the file ends
            if current_cluster_name and temp_uniprot_list:
                for uniprot_id in temp_uniprot_list:
                    uniprot_to_uniref[uniprot_id] = f"UniRef50_{current_cluster_name}"
                entries_processed += 1
            
            print(f"Finished processing {line_count:,} lines")
            print(f"Processed {entries_processed:,} UniRef50 entries")
            print(f"Created {len(uniprot_to_uniref):,} UniProtKB to UniRef50 mappings")
    
    except Exception as e:
        print(f"Error parsing XML file: {e}")
        return {}
    
    return uniprot_to_uniref

def save_dictionary_to_pickle(dictionary: Dict[str, str], output_file: str):
    """
    Save the dictionary to a pickle file for fast loading later.
    
    Args:
        dictionary (Dict[str, str]): The UniProtKB to UniRef50 mapping
        output_file (str): Path to output pickle file
    """
    try:
        with open(output_file, 'wb') as f:
            pickle.dump(dictionary, f, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"Dictionary saved to {output_file} ({len(dictionary):,} entries)")
    except Exception as e:
        print(f"Error saving dictionary to pickle: {e}")

def load_dictionary_from_pickle(input_file: str) -> Dict[str, str]:
    """
    Load the dictionary from a pickle file.
    
    Args:
        input_file (str): Path to input pickle file
        
    Returns:
        Dict[str, str]: The UniProtKB to UniRef50 mapping
    """
    try:
        with open(input_file, 'rb') as f:
            dictionary = pickle.load(f)
        print(f"Dictionary loaded from {input_file} ({len(dictionary):,} entries)")
        return dictionary
    except Exception as e:
        print(f"Error loading dictionary from pickle: {e}")
        return {}

def save_dictionary_to_file(dictionary: Dict[str, str], output_file: str):
    """
    Save the dictionary to a text file for human readability.
    
    Args:
        dictionary (Dict[str, str]): The UniProtKB to UniRef50 mapping
        output_file (str): Path to output file
    """
    try:
        with open(output_file, 'w') as f:
            for uniprot_id, uniref_id in dictionary.items():
                f.write(f"{uniprot_id}\t{uniref_id}\n")
        print(f"Dictionary saved to {output_file} ({len(dictionary):,} entries)")
    except Exception as e:
        print(f"Error saving dictionary: {e}")

# Example usage
if __name__ == "__main__":
    # Parse the entire XML file
    if len(sys.argv) != 3:
        print("Usage: python uniref50_to_dict.py <input_xml.gz> <output_pickle>")
        sys.exit(1)

    xml_file_path = sys.argv[1]
    output_pickle_path = sys.argv[2]
    #xml_file_path = "uniref50.xml.gz"
    print("Starting to parse UniRef50 XML file...")
    uniprot_to_uniref_dict = parse_uniref50_xml_targeted(xml_file_path)
    
    if uniprot_to_uniref_dict:
        print(f"\nSuccessfully created dictionary with {len(uniprot_to_uniref_dict):,} entries")
        
        # Save dictionary as pickle (primary method - fast and compact)
        save_dictionary_to_pickle(uniprot_to_uniref_dict, output_pickle_path)
        
        # Also save first 1000 entries as text file for inspection
        #sample_dict = dict(list(uniprot_to_uniref_dict.items())[:1000])
        #save_dictionary_to_file(sample_dict, "sample_uniprot_to_uniref50_mapping.txt")
        
        print(f"\n=== SUMMARY ===")
        print(f"Total mappings created: {len(uniprot_to_uniref_dict):,}")
        print(f"Dictionary saved as: complete_uniprot_to_uniref50_mapping.pkl")
        #print(f"Sample (1000 entries) saved as: sample_uniprot_to_uniref50_mapping.txt")
        
        # Usage example
        print(f"\n=== USAGE EXAMPLE ===")
        print(f"To load and use:")
        print(f"import pickle")
        print(f"with open('complete_uniprot_to_uniref50_mapping.pkl', 'rb') as f:")
        print(f"    mapping = pickle.load(f)")
        print(f"uniref_id = mapping.get('YOUR_UNIPROT_ID')")
    
    else:
        print("Failed to create dictionary. Check the XML file path and format.")
