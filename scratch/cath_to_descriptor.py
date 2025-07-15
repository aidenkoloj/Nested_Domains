import csv

def parse_cath_file(input_file, output_file):
    """
    Parse a CATH file and extract CATHCODE, ARCH, TOPOL, HOMOL information
    """
    entries = []
    current_entry = {}
    
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check for each field type
            if line.startswith('CATHCODE'):
                # If we have a complete entry, save it
                if current_entry and 'CATHCODE' in current_entry:
                    entries.append(current_entry)
                
                # Start new entry
                current_entry = {'CATHCODE': line.split(None, 1)[1]}
                
            elif line.startswith('ARCH'):
                if current_entry:
                    current_entry['ARCH'] = line.split(None, 1)[1]
                    
            elif line.startswith('TOPOL'):
                if current_entry:
                    current_entry['TOPOL'] = line.split(None, 1)[1]
                    
            elif line.startswith('HOMOL'):
                if current_entry:
                    current_entry['HOMOL'] = line.split(None, 1)[1]
    
    # Don't forget the last entry
    if current_entry and 'CATHCODE' in current_entry:
        entries.append(current_entry)
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['CATHCODE', 'ARCH', 'TOPOL', 'HOMOL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for entry in entries:
            # Ensure all fields exist (fill with empty string if missing)
            row = {field: entry.get(field, '') for field in fieldnames}
            writer.writerow(row)
    
    print(f"Parsed {len(entries)} entries and saved to {output_file}")
    return entries



# Example usage
if __name__ == "__main__":
    input_filename = "/home/gridsan/akolodziej/01_insert_domains/data/cath-domain-description-file.txt"  # Replace with your input file name
    output_filename = "cath_descriptor_output.csv"
    
    # Parse the file
    try:
        entries = parse_cath_file(input_filename, output_filename)
        
        # Print first few entries as verification
        print("\nFirst few entries:")
        for i, entry in enumerate(entries[:3]):
            print(f"Entry {i+1}: {entry}")
            
    except FileNotFoundError:
        print(f"Error: Could not find file '{input_filename}'")
        print("Please make sure the file exists and update the filename in the script")
    except Exception as e:
        print(f"Error parsing file: {e}")