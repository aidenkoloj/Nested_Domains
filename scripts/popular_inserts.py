import pandas as pd
import os
from collections import defaultdict
import sys
def process_tsv_file(input_file, output_file):
    """
    Process the TSV file to analyze insert_cath and parent_cath relationships.
    
    Args:
        input_file (str): Path to the input TSV file
        output_file (str): Path to the output CSV file
    """
    try:
        # Read the TSV file
        print(f"Reading TSV file: {input_file}")
        df = pd.read_csv(input_file, sep='\t')
        
        # Display basic info about the dataset
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Check if required columns exist
        required_columns = ['insert_cath', 'parent_cath']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Error: Missing required columns: {missing_columns}")
            print(f"Available columns: {list(df.columns)}")
            return
        
        # Remove rows with missing values in the required columns
        initial_rows = len(df)
        df = df.dropna(subset=['insert_cath', 'parent_cath'])
        final_rows = len(df)
        
        if initial_rows != final_rows:
            print(f"Removed {initial_rows - final_rows} rows with missing values")
        
        # Step 1: Generate a list of all unique insert_caths
        unique_insert_caths = df['insert_cath'].unique()
        print(f"Found {len(unique_insert_caths)} unique insert_cath values")
        
        # Step 2-4: For each unique insert_cath, count unique parent_caths
        results = []
        
        for insert_cath in unique_insert_caths:
            # Filter the dataframe for this insert_cath
            filtered_df = df[df['insert_cath'] == insert_cath]
            
            # Count unique parent_caths
            unique_parent_caths = filtered_df['parent_cath'].nunique()
            
            results.append({
                'insert_cath': insert_cath,
                'unique_parent_caths_count': unique_parent_caths
            })
            
            print(f"Insert CATH: {insert_cath} -> {unique_parent_caths} unique parent CATHs")
        
        # Create results DataFrame
        results_df = pd.DataFrame(results)
        
        # Sort by count (descending) for better readability
        results_df = results_df.sort_values('unique_parent_caths_count', ascending=False)
        
        # Save to CSV
        results_df.to_csv(output_file, index=False)
        print(f"\nResults saved to: {output_file}")
        
        # Display summary statistics
        print("\n=== SUMMARY STATISTICS ===")
        print(f"Total unique insert_cath values: {len(results_df)}")
        print(f"Average unique parent_caths per insert_cath: {results_df['unique_parent_caths_count'].mean():.2f}")
        print(f"Median unique parent_caths per insert_cath: {results_df['unique_parent_caths_count'].median():.2f}")
        print(f"Max unique parent_caths for a single insert_cath: {results_df['unique_parent_caths_count'].max()}")
        print(f"Min unique parent_caths for a single insert_cath: {results_df['unique_parent_caths_count'].min()}")
        
        # Display top 10 results
        print("\n=== TOP 10 INSERT_CATHS BY PARENT_CATH DIVERSITY ===")
        print(results_df.head(10).to_string(index=False))
        
        return results_df
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return None
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return None

def main():
    # File paths
    #input_file = "uniref50_nested_domain_pairs.tsv"
    input_file = sys.argv[1]
    #output_file = "insert_cath_parent_cath_analysis.csv"
    output_file = sys.argv[2]
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' not found in current directory.")
        print("Please make sure the file exists and try again.")
        return
    
    # Process the file
    print("Starting TSV processing...")
    results = process_tsv_file(input_file, output_file)
    
    if results is not None:
        print("\nProcessing completed successfully!")
        print(f"Output file: {output_file}")
    else:
        print("Processing failed!")

if __name__ == "__main__":
    main()