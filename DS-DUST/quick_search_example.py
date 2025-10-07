#!/usr/bin/env python3
"""
Quick Search Example - How to input keywords programmatically
This shows you exactly where to put your keywords in the code.
"""

from metadata_search_engine import MetadataSearchEngine
from maximum_collection_engine import MaximumCollectionEngine

def example_1_basic_keyword_search():
    """Example 1: Basic keyword search with your own keywords."""
    
    print("=" * 60)
    print("EXAMPLE 1: BASIC KEYWORD SEARCH")
    print("=" * 60)
    
    # Initialize the search engine
    engine = MetadataSearchEngine()
    
    #  CHANGE THESE KEYWORDS TO YOUR OWN:
    keywords = [
        'machine learning',      # ← Change this
        'customer data',         # ← Change this  
        'sales analytics',       # ← Change this
        'healthcare',           # ← Add your own
        'finance'               # ← Add your own
    ]
    
    print(f" Searching for keywords: {keywords}")
    
    # Search for datasets
    results = engine.search_by_keywords(keywords, max_results=20)
    
    print(f"\n Found {len(results)} datasets!")
    
    # Show top results
    for i, dataset in enumerate(results[:5]):
        print(f"\n  {i+1}. {dataset.title}")
        print(f"     Size: {dataset.size_bytes/1024/1024:.1f} MB")
        print(f"     Downloads: {dataset.download_count:,}")
        print(f"     Score: {dataset.search_score:.1f}")
    
    # Export results
    filename = engine.export_metadata_index(results, "my_keyword_search.csv")
    print(f"\n Exported to: {filename}")

def example_2_domain_specific_search():
    """Example 2: Domain-specific search with tags."""
    
    print("\n" + "=" * 60)
    print("EXAMPLE 2: DOMAIN-SPECIFIC SEARCH")
    print("=" * 60)
    
    engine = MetadataSearchEngine()
    
    #  CHANGE THE DOMAIN TO YOUR INTEREST:
    domain = "healthcare"  # ← Change this to: finance, technology, education, etc.
    
    # Define search criteria for your domain
    keywords = [f"{domain} data", f"{domain} analytics", f"{domain} machine learning"]
    tags = [domain, "business", "classification"]  # ← Adjust these tags
    file_types = ["csv", "json"]  # ← Adjust file types you want
    
    print(f" Searching for domain: {domain}")
    print(f"   Keywords: {keywords}")
    print(f"   Tags: {tags}")
    print(f"   File types: {file_types}")
    
    # Multi-criteria search
    results = engine.multi_criteria_search(
        keywords=keywords,
        tags=tags,
        file_types=file_types,
        max_results=30
    )
    
    print(f"\n Found {len(results)} datasets for {domain}!")
    
    # Show results
    for i, dataset in enumerate(results[:5]):
        print(f"\n  {i+1}. {dataset.title}")
        print(f"     Tags: {', '.join(dataset.tags[:3])}")
        print(f"     Downloads: {dataset.download_count:,}")
    
    # Export
    filename = engine.export_metadata_index(results, f"{domain}_datasets.csv")
    print(f"\n Exported to: {filename}")

def example_3_maximum_collection():
    """Example 3: Maximum collection for a specific domain."""
    
    print("\n" + "=" * 60)
    print("EXAMPLE 3: MAXIMUM COLLECTION")
    print("=" * 60)
    
    # Initialize maximum collection engine
    engine = MaximumCollectionEngine()
    
    # CHANGE THE DOMAIN TO YOUR INTEREST:
    domain = "technology"  # ← Change this to: finance, healthcare, education, etc.
    
    print(f" Maximum collection for domain: {domain}")
    print("This will search using multiple methods to get the most datasets possible...")
    
    # Comprehensive collection
    results = engine.comprehensive_collection(domain, max_total=100)
    
    print(f"\n Collected {len(results)} datasets for {domain}!")
    
    # Show top results
    print(f"\n TOP 10 DATASETS:")
    for i, dataset in enumerate(results[:10]):
        print(f"  {i+1}. {dataset.title}")
        print(f"     Method: {dataset.search_method}")
        print(f"     Score: {dataset.search_score:.1f}")
        print()
    
    # Export
    filename = engine.export_collection_index(results, f"maximum_{domain}_collection.csv")
    print(f" Exported to: {filename}")
    
    # Show statistics
    engine.print_collection_stats()

def example_4_custom_column_search():
    """Example 4: Search by specific column names you're interested in."""
    
    print("\n" + "=" * 60)
    print("EXAMPLE 4: CUSTOM COLUMN SEARCH")
    print("=" * 60)
    
    engine = MetadataSearchEngine()
    
    #  CHANGE THESE TO COLUMNS YOU'RE LOOKING FOR:
    column_keywords = [
        'customer_id',          # ← Change this
        'purchase_amount',      # ← Change this
        'transaction_date',     # ← Change this
        'user_rating',          # ← Add your own
        'product_category'      # ← Add your own
    ]
    
    print(f" Searching for datasets with columns: {column_keywords}")
    
    # Search by column keywords
    results = engine.search_by_columns(column_keywords, max_results=25)
    
    print(f"\n Found {len(results)} datasets with these columns!")
    
    # Show results
    for i, dataset in enumerate(results[:5]):
        print(f"\n  {i+1}. {dataset.title}")
        print(f"     Description: {dataset.description[:100]}...")
        print(f"     Score: {dataset.search_score:.1f}")
    
    # Export
    filename = engine.export_metadata_index(results, "column_search_results.csv")
    print(f"\n Exported to: {filename}")

def main():
    """Run all examples."""
    
    print(" KEYWORD INPUT EXAMPLES")
    print("This shows you exactly where to put your keywords!")
    
    try:
        # Run all examples
        example_1_basic_keyword_search()
        example_2_domain_specific_search() 
        example_3_maximum_collection()
        example_4_custom_column_search()
        
        print("\n" + "=" * 60)
        print(" ALL EXAMPLES COMPLETED!")
        print("=" * 60)
        
        print("""
 TO USE YOUR OWN KEYWORDS:

1. Edit the variables in each example function:
   - keywords = ['your', 'keywords', 'here']
   - domain = "your_domain"
   - column_keywords = ['your', 'columns']

2. Run the specific example you want:
   python quick_search_example.py

3. Or use the interactive search:
   python search_datasets.py
        """)
        
    except Exception as e:
        print(f" Error: {e}")
        print("Make sure your Kaggle API is set up correctly.")

if __name__ == "__main__":
    main()
