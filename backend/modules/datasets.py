from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import os
def search_datasets(keyword):
    api = KaggleApi()
    api.authenticate()
    # Search for datasets matching the keyword
    all_results = []
    page = 1
    while page <= 10:
        datasets = api.dataset_list(search=keyword, page=page)
        if not datasets:
            break
        for ds in datasets:
            # ds.title is the human name, ds.ref is "owner/dataset-slug"
            all_results.append((ds.title, ds.ref))
        page += 1
    return all_results

def search_by_files(files):
    """
    Extract column names from CSV files and search for datasets based on those columns.
    Excludes 'id' and similar identifier columns.
    
    Args:
        files: List of file paths to CSV files
    
    Returns:
        List of tuples containing (title, ref) for found datasets
    """
    all_results = []
    
    # Define patterns for columns to exclude (id-like columns)
    exclude_patterns = ['id', 'index', 'key', 'pk', 'uuid', 'guid']
    
    for file_path in files:
        try:
            # Read CSV file and extract column names
            df = pd.read_csv(file_path)
            columns = df.columns.tolist()
            
            # Filter out id-like columns (case insensitive)
            valid_columns = []
            for column in columns:
                column_lower = column.lower().strip()
                # Check if column name contains any exclude patterns
                if not any(pattern in column_lower for pattern in exclude_patterns):
                    valid_columns.append(column)
            
            # Search for datasets for each valid column
            for column in valid_columns:
                try:
                    column_results = search_datasets(column)
                    all_results.extend(column_results)
                except Exception as e:
                    print(f"Error searching for column '{column}': {e}")
                    continue
                    
        except Exception as e:
            print(f"Error reading file '{file_path}': {e}")
            continue
    
    # Remove duplicates while preserving order
    seen = set()
    unique_results = []
    for result in all_results:
        if result not in seen:
            seen.add(result)
            unique_results.append(result)
    
    return unique_results

# print(search_datasets('financial'))