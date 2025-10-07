#!/usr/bin/env python3
"""
Interactive Dataset Search
This script lets you input your own keywords and search for datasets.
"""

import sys
from metadata_search_engine import MetadataSearchEngine

def interactive_search():
    """Interactive search for datasets with user input."""
    
    print("=" * 70)
    print("INTERACTIVE DATASET SEARCH FOR DATA LAKE")
    print("=" * 70)
    
    # Initialize search engine
    engine = MetadataSearchEngine()
    
    print("\n🎯 Let's search for datasets! You can input keywords, tags, or domains.")
    print("Examples: 'finance', 'healthcare', 'machine learning', 'customer analytics'")
    
    while True:
        print("\n" + "="*50)
        print("SEARCH OPTIONS:")
        print("1. Keyword search")
        print("2. Tag search") 
        print("3. File type search")
        print("4. Multi-criteria search")
        print("5. Exit")
        
        choice = input("\nChoose an option (1-5): ").strip()
        
        if choice == '1':
            keyword_search(engine)
        elif choice == '2':
            tag_search(engine)
        elif choice == '3':
            file_type_search(engine)
        elif choice == '4':
            multi_criteria_search(engine)
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please choose 1-5.")

def keyword_search(engine):
    """Perform keyword search with user input."""
    print("\n🔍 KEYWORD SEARCH")
    print("-" * 30)
    
    keywords_input = input("Enter keywords (comma-separated): ").strip()
    
    if not keywords_input:
        print("❌ No keywords entered!")
        return
    
    keywords = [kw.strip() for kw in keywords_input.split(',')]
    
    try:
        max_results = int(input("Max results per keyword (default 20): ") or "20")
    except ValueError:
        max_results = 20
    
    print(f"\n🔍 Searching for keywords: {keywords}")
    print(f"Max results per keyword: {max_results}")
    
    results = engine.search_by_keywords(keywords, max_results)
    
    print(f"\n✅ Found {len(results)} datasets!")
    display_results(results, max_display=10)

def tag_search(engine):
    """Perform tag search with user input."""
    print("\n🏷️ TAG SEARCH")
    print("-" * 30)
    
    tags_input = input("Enter tags (comma-separated): ").strip()
    
    if not tags_input:
        print("❌ No tags entered!")
        return
    
    tags = [tag.strip() for tag in tags_input.split(',')]
    
    try:
        max_results = int(input("Max results per tag (default 15): ") or "15")
    except ValueError:
        max_results = 15
    
    print(f"\n🏷️ Searching for tags: {tags}")
    print(f"Max results per tag: {max_results}")
    
    results = engine.search_by_tags(tags, max_results)
    
    print(f"\n✅ Found {len(results)} datasets!")
    display_results(results, max_display=10)

def file_type_search(engine):
    """Perform file type search with user input."""
    print("\n📄 FILE TYPE SEARCH")
    print("-" * 30)
    
    file_types_input = input("Enter file types (comma-separated, e.g., csv,json): ").strip()
    
    if not file_types_input:
        print("❌ No file types entered!")
        return
    
    file_types = [ft.strip() for ft in file_types_input.split(',')]
    
    try:
        max_results = int(input("Max results per file type (default 10): ") or "10")
    except ValueError:
        max_results = 10
    
    print(f"\n📄 Searching for file types: {file_types}")
    print(f"Max results per file type: {max_results}")
    
    results = engine.search_by_file_type(file_types, max_results)
    
    print(f"\n✅ Found {len(results)} datasets!")
    display_results(results, max_display=10)

def multi_criteria_search(engine):
    """Perform multi-criteria search with user input."""
    print("\n🎯 MULTI-CRITERIA SEARCH")
    print("-" * 30)
    
    keywords_input = input("Keywords (comma-separated, optional): ").strip()
    keywords = [kw.strip() for kw in keywords_input.split(',')] if keywords_input else None
    
    tags_input = input("Tags (comma-separated, optional): ").strip()
    tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else None
    
    file_types_input = input("File types (comma-separated, optional): ").strip()
    file_types = [ft.strip() for ft in file_types_input.split(',')] if file_types_input else None
    
    column_keywords_input = input("Column keywords (comma-separated, optional): ").strip()
    column_keywords = [ck.strip() for ck in column_keywords_input.split(',')] if column_keywords_input else None
    
    if not any([keywords, tags, file_types, column_keywords]):
        print("❌ At least one search criteria required!")
        return
    
    try:
        max_results = int(input("Max total results (default 50): ") or "50")
    except ValueError:
        max_results = 50
    
    print(f"\n🎯 Multi-criteria search:")
    if keywords: print(f"  Keywords: {keywords}")
    if tags: print(f"  Tags: {tags}")
    if file_types: print(f"  File types: {file_types}")
    if column_keywords: print(f"  Column keywords: {column_keywords}")
    print(f"  Max results: {max_results}")
    
    results = engine.multi_criteria_search(
        keywords=keywords,
        tags=tags,
        file_types=file_types,
        column_keywords=column_keywords,
        max_results=max_results
    )
    
    print(f"\n✅ Found {len(results)} datasets!")
    display_results(results, max_display=15)

def display_results(results, max_display=10):
    """Display search results."""
    if not results:
        print("No datasets found.")
        return
    
    print(f"\n📋 TOP {min(max_display, len(results))} RESULTS:")
    for i, dataset in enumerate(results[:max_display]):
        print(f"\n  {i+1}. {dataset.title}")
        print(f"     Ref: {dataset.ref}")
        print(f"     Size: {dataset.size_bytes/1024/1024:.1f} MB")
        print(f"     Downloads: {dataset.download_count:,}")
        print(f"     Votes: {dataset.vote_count}")
        print(f"     Score: {dataset.search_score:.1f}")
        if dataset.tags:
            print(f"     Tags: {', '.join(dataset.tags[:3])}")
    
    if len(results) > max_display:
        print(f"\n... and {len(results) - max_display} more datasets")
    
    # Ask if user wants to export results
    export_choice = input(f"\n💾 Export all {len(results)} results to CSV? (y/n): ").strip().lower()
    if export_choice in ['y', 'yes']:
        filename = engine.export_metadata_index(results)
        print(f"✅ Exported to: {filename}")

def quick_search_example():
    """Show a quick example of how to use the search programmatically."""
    print("\n" + "="*70)
    print("QUICK SEARCH EXAMPLE")
    print("="*70)
    
    print("""
If you want to search programmatically instead of interactively:

from metadata_search_engine import MetadataSearchEngine

# Initialize engine
engine = MetadataSearchEngine()

# Search by keywords
results = engine.search_by_keywords(['finance', 'banking'], max_results=20)

# Search by tags  
results = engine.search_by_tags(['machine-learning'], max_results=15)

# Multi-criteria search
results = engine.multi_criteria_search(
    keywords=['customer analytics'],
    tags=['business'],
    file_types=['csv'],
    max_results=50
)

# Export results
filename = engine.export_metadata_index(results)
print(f"Exported to: {filename}")
    """)

if __name__ == "__main__":
    try:
        interactive_search()
    except KeyboardInterrupt:
        print("\n\n👋 Search interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure your Kaggle API is set up correctly.")
    
    # Show quick example at the end
    quick_search_example()
