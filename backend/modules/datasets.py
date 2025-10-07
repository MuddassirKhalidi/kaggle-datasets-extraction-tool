from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import os
import time
import random
from functools import lru_cache
from typing import List, Tuple, Optional
import requests

class RateLimitedKaggleAPI:
    """Wrapper for Kaggle API with built-in rate limiting and retry logic"""
    
    def __init__(self):
        self.api = KaggleApi()
        self.api.authenticate()
        # Conservative rate limits - adjust based on your needs
        self.min_delay = 1.0  # Minimum delay between requests (seconds)
        self.max_delay = 3.0  # Maximum delay for backoff
        self.base_delay = 1.0  # Base delay for exponential backoff
        
    def _make_request_with_retry(self, func, *args, max_retries=3, **kwargs):
        """Make API request with exponential backoff retry logic"""
        for attempt in range(max_retries + 1):
            try:
                # Add random delay to avoid thundering herd
                delay = random.uniform(self.min_delay, self.min_delay * 1.5)
                time.sleep(delay)
                
                return func(*args, **kwargs)
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:  # Rate limited
                    if attempt < max_retries:
                        # Exponential backoff with jitter
                        backoff_delay = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
                        backoff_delay = min(backoff_delay, self.max_delay)
                        print(f"Rate limited. Waiting {backoff_delay:.2f} seconds before retry {attempt + 1}/{max_retries}")
                        time.sleep(backoff_delay)
                        continue
                    else:
                        print(f"Max retries exceeded for rate limit. Skipping this request.")
                        raise
                else:
                    raise
            except Exception as e:
                print(f"API request failed: {e}")
                if attempt < max_retries:
                    time.sleep(self.base_delay * (attempt + 1))
                    continue
                else:
                    raise
    
    def dataset_list(self, search=None, page=1, **kwargs):
        """Rate-limited dataset list"""
        return self._make_request_with_retry(
            self.api.dataset_list, search=search, page=page, **kwargs
        )
    
    def dataset_list_files(self, dataset_ref, **kwargs):
        """Rate-limited dataset files list"""
        return self._make_request_with_retry(
            self.api.dataset_list_files, dataset_ref, **kwargs
        )

# Cache for search results to avoid redundant API calls
@lru_cache(maxsize=100)
def cached_search_datasets(keyword: str) -> List[Tuple]:
    """Cached version of search_datasets to avoid redundant API calls"""
    return _search_datasets_impl(keyword, max_pages=5, include_file_details=True, file_details_per_page=None)

def search_datasets_all_pages(keyword: str, include_file_details: bool = True, file_details_per_page: Optional[int] = None) -> List[Tuple]:
    """
    Search for datasets with no page limit - fetches ALL available pages
    
    Args:
        keyword: Search term
        include_file_details: Whether to fetch file details for datasets
        file_details_per_page: How many datasets per page to get file details for (None = all datasets)
    
    Returns:
        List of all matching datasets
    """
    return _search_datasets_impl(keyword, max_pages=None, include_file_details=include_file_details, file_details_per_page=file_details_per_page)

def search_datasets_limited(keyword: str, max_pages: int = 10, include_file_details: bool = True, file_details_per_page: Optional[int] = None) -> List[Tuple]:
    """
    Search for datasets with a specific page limit
    
    Args:
        keyword: Search term
        max_pages: Maximum number of pages to fetch
        include_file_details: Whether to fetch file details for datasets
        file_details_per_page: How many datasets per page to get file details for (None = all datasets)
    
    Returns:
        List of matching datasets
    """
    return _search_datasets_impl(keyword, max_pages=max_pages, include_file_details=include_file_details, file_details_per_page=file_details_per_page)

def _search_datasets_impl(keyword: str, max_pages: int = None, include_file_details: bool = True, file_details_per_page: Optional[int] = 3) -> List[Tuple]:
    """
    Internal implementation of dataset search with rate limiting
    
    Args:
        keyword: Search term
        max_pages: Maximum number of pages to fetch (None for all pages)
        include_file_details: Whether to fetch file details for datasets
        file_details_per_page: How many datasets per page to get file details for (None = all datasets)
    """
    api_wrapper = RateLimitedKaggleAPI()
    all_results = []
    
    print(f"Searching for datasets with keyword: '{keyword}'")
    print(f"Rate limiting: {api_wrapper.min_delay}s minimum delay between requests")
    
    page = 1
    
    while True:
        # Check if we've reached the maximum page limit
        if max_pages and page > max_pages:
            print(f"Reached maximum page limit of {max_pages}")
            break
            
        try:
            print(f"Fetching page {page}...")
            datasets = api_wrapper.dataset_list(search=keyword, page=page)
            
            if not datasets or len(datasets) == 0:
                print(f"No datasets found on page {page}. Stopping search.")
                break
                
            print(f"Found {len(datasets)} datasets on page {page}")
            
            for i, ds in enumerate(datasets):
                try:
                    print(f"  Processing dataset {i+1}/{len(datasets)}: {ds.title[:50]}...")
                    
                    # Get basic dataset info first
                    basic_info = (
                        ds.title,
                        ds.ref,
                        ds.license_name,
                        [tag.name for tag in ds.tags],
                        ds.last_updated,
                        None  # Placeholder for files info
                    )
                    all_results.append(basic_info)
                    
                    # Get file info if requested and within the limit
                    if include_file_details and (file_details_per_page is None or i < file_details_per_page):
                        try:
                            files_info = api_wrapper.dataset_list_files(ds.ref)
                            file_details = [
                                (f.name, "{:.2f}".format(f.total_bytes / 1048576)) 
                                for f in files_info.files
                            ]
                            # Update the last element with file info
                            all_results[-1] = basic_info[:-1] + (file_details,)
                        except Exception as e:
                            print(f"    Warning: Could not get file details: {e}")
                            # Keep the placeholder None for file info
                    
                except Exception as e:
                    print(f"    Error processing dataset: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break
            
        page += 1
    
    print(f"Search completed. Found {len(all_results)} total datasets across {page-1} pages.")
    return all_results

def search_datasets(keyword: str) -> List[Tuple]:
    """Search for datasets matching the keyword with rate limiting and caching"""
    return cached_search_datasets(keyword)

def search_by_files(files: List[str]) -> List[Tuple]:
    """
    Extract column names from CSV files and search for datasets based on those columns.
    Excludes 'id' and similar identifier columns.
    
    Args:
        files: List of file paths to CSV files
    
    Returns:
        List of tuples containing (title, ref, license, tags, last_updated, files) for found datasets
    """
    all_results = []
    
    # Define patterns for columns to exclude (id-like columns)
    exclude_patterns = ['id', 'index', 'key', 'pk', 'uuid', 'guid']
    
    for file_path in files:
        try:
            print(f"Processing file: {file_path}")
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
            
            print(f"Found {len(valid_columns)} valid columns to search: {valid_columns[:5]}...")
            
            # Search for datasets for each valid column with rate limiting
            for i, column in enumerate(valid_columns):
                try:
                    print(f"  Searching for column '{column}' ({i+1}/{len(valid_columns)})")
                    column_results = search_datasets_limited(column, max_pages=2)
                    all_results.extend(column_results)
                    
                    # Add delay between column searches to be respectful to the API
                    if i < len(valid_columns) - 1:  # Don't delay after the last column
                        time.sleep(5)  # 5 second delay between column searches
                        
                except Exception as e:
                    print(f"    Error searching for column '{column}': {e}")
                    continue
                    
        except Exception as e:
            print(f"Error reading file '{file_path}': {e}")
            continue
    
    # Remove duplicates while preserving order
    seen = set()
    unique_results = []
    for result in all_results:
        # Use title and ref as the unique identifier
        result_key = (result[0], result[1])  # (title, ref)
        if result_key not in seen:
            seen.add(result_key)
            unique_results.append(result)
    
    print(f"Search by files completed. Found {len(unique_results)} unique datasets.")
    return unique_results

# Example usage:

# 1. Default behavior (5 pages, cached)
# results = search_datasets('financial')

# 2. Fetch ALL available pages (no limit)
# results = search_datasets_all_pages('financial')

# 3. Fetch specific number of pages
# results = search_datasets_limited('financial', max_pages=20)

# 4. Fetch all pages but skip file details for faster execution
# results = search_datasets_all_pages('financial', include_file_details=False)

# 5. Fetch all pages but get file details for more datasets per page
# results = search_datasets_all_pages('financial', file_details_per_page=5)

if __name__ == "__main__":
    # Test with a small search to demonstrate
    results = search_datasets_limited('housing in riyadh', max_pages=2)
    print(results)
    print(f"Found {len(results)} datasets")