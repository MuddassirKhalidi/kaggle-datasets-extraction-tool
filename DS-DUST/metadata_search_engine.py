#!/usr/bin/env python3
"""
Metadata Search Engine for Data Lake Indexing
This system efficiently searches and filters Kaggle datasets using metadata-only operations.
"""

import pandas as pd
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from kaggle.api.kaggle_api_extended import KaggleApi

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class DatasetMetadata:
    """Lightweight metadata structure for dataset indexing."""
    ref: str
    title: str
    description: str
    size_bytes: int
    last_updated: str
    download_count: int
    vote_count: int
    usability_rating: float
    tags: List[str]
    search_score: float = 0.0
    file_types: List[str] = None
    estimated_rows: int = 0

class MetadataSearchEngine:
    """
    Efficient metadata search engine for data lake indexing.
    Uses Kaggle's search API to filter datasets before expensive operations.
    """
    
    def __init__(self):
        """Initialize the search engine with Kaggle API."""
        self.api = KaggleApi()
        self.api.authenticate()
        self.search_history = []
        logger.info("Metadata Search Engine initialized")
    
    def search_by_keywords(self, keywords: List[str], max_results: int = 100) -> List[DatasetMetadata]:
        """
        Search datasets by keywords in title/description.
        
        Args:
            keywords: List of search terms
            max_results: Maximum number of results to return
            
        Returns:
            List of DatasetMetadata objects
        """
        all_datasets = []
        
        for keyword in keywords:
            logger.info(f"Searching for keyword: '{keyword}'")
            
            try:
                # Use Kaggle's search API
                results = self.api.dataset_list(search=keyword, sort_by='hottest')
                
                # Convert to our metadata format
                for dataset in results[:max_results//len(keywords)]:
                    metadata = self._extract_metadata(dataset, keyword)
                    if metadata:
                        all_datasets.append(metadata)
                        
            except Exception as e:
                logger.error(f"Error searching for '{keyword}': {e}")
        
        # Remove duplicates and sort by relevance
        unique_datasets = self._deduplicate_datasets(all_datasets)
        unique_datasets.sort(key=lambda x: x.search_score, reverse=True)
        
        logger.info(f"Found {len(unique_datasets)} unique datasets from keyword search")
        return unique_datasets[:max_results]
    
    def search_by_tags(self, tags: List[str], max_results: int = 100) -> List[DatasetMetadata]:
        """
        Search datasets by tags.
        
        Args:
            tags: List of tags to search for
            max_results: Maximum number of results
            
        Returns:
            List of DatasetMetadata objects
        """
        all_datasets = []
        
        for tag in tags:
            logger.info(f"Searching for tag: '{tag}'")
            
            try:
                # Search with tag-specific query
                search_query = f"tag:{tag}"
                results = self.api.dataset_list(search=search_query, sort_by='hottest')
                
                for dataset in results[:max_results//len(tags)]:
                    metadata = self._extract_metadata(dataset, tag, search_type='tag')
                    if metadata and tag.lower() in [t.lower() for t in metadata.tags]:
                        all_datasets.append(metadata)
                        
            except Exception as e:
                logger.error(f"Error searching for tag '{tag}': {e}")
        
        unique_datasets = self._deduplicate_datasets(all_datasets)
        unique_datasets.sort(key=lambda x: x.vote_count, reverse=True)
        
        logger.info(f"Found {len(unique_datasets)} unique datasets from tag search")
        return unique_datasets[:max_results]
    
    def search_by_file_type(self, file_types: List[str], max_results: int = 100) -> List[DatasetMetadata]:
        """
        Search datasets by file types.
        
        Args:
            file_types: List of file extensions (e.g., ['csv', 'json'])
            max_results: Maximum number of results
            
        Returns:
            List of DatasetMetadata objects
        """
        all_datasets = []
        
        for file_type in file_types:
            logger.info(f"Searching for file type: '{file_type}'")
            
            try:
                # Use Kaggle's file type filtering
                results = self.api.dataset_list(file_type=file_type, sort_by='hottest')
                
                for dataset in results[:max_results//len(file_types)]:
                    metadata = self._extract_metadata(dataset, file_type, search_type='file_type')
                    if metadata:
                        all_datasets.append(metadata)
                        
            except Exception as e:
                logger.error(f"Error searching for file type '{file_type}': {e}")
        
        unique_datasets = self._deduplicate_datasets(all_datasets)
        unique_datasets.sort(key=lambda x: x.size_bytes, reverse=True)
        
        logger.info(f"Found {len(unique_datasets)} unique datasets from file type search")
        return unique_datasets[:max_results]
    
    def search_by_columns(self, column_keywords: List[str], max_results: int = 100) -> List[DatasetMetadata]:
        """
        Search datasets by column names/keywords.
        This leverages Kaggle's search in dataset descriptions and metadata.
        
        Args:
            column_keywords: List of column names or data field keywords
            max_results: Maximum number of results
            
        Returns:
            List of DatasetMetadata objects
        """
        all_datasets = []
        
        for keyword in column_keywords:
            logger.info(f"Searching for column keyword: '{keyword}'")
            
            try:
                # Search for datasets that might contain this column
                search_queries = [
                    keyword,  # Direct keyword search
                    f"column {keyword}",  # Column-specific search
                    f"field {keyword}",   # Field-specific search
                    f"feature {keyword}"  # Feature-specific search
                ]
                
                for query in search_queries:
                    results = self.api.dataset_list(search=query, sort_by='hottest')
                    
                    for dataset in results[:max_results//(len(column_keywords) * len(search_queries))]:
                        metadata = self._extract_metadata(dataset, keyword, search_type='column')
                        if metadata:
                            all_datasets.append(metadata)
                        
            except Exception as e:
                logger.error(f"Error searching for column keyword '{keyword}': {e}")
        
        unique_datasets = self._deduplicate_datasets(all_datasets)
        unique_datasets.sort(key=lambda x: x.search_score, reverse=True)
        
        logger.info(f"Found {len(unique_datasets)} unique datasets from column search")
        return unique_datasets[:max_results]
    
    def multi_criteria_search(self, 
                            keywords: List[str] = None,
                            tags: List[str] = None, 
                            file_types: List[str] = None,
                            column_keywords: List[str] = None,
                            max_results: int = 100) -> List[DatasetMetadata]:
        """
        Perform multi-criteria search combining different search methods.
        
        Args:
            keywords: Keywords for title/description search
            tags: Tags to search for
            file_types: File types to filter by
            column_keywords: Column names to search for
            max_results: Maximum number of results
            
        Returns:
            List of DatasetMetadata objects ranked by relevance
        """
        logger.info("Starting multi-criteria metadata search...")
        
        all_datasets = []
        
        # Perform different types of searches
        if keywords:
            keyword_results = self.search_by_keywords(keywords, max_results//4)
            all_datasets.extend(keyword_results)
            
        if tags:
            tag_results = self.search_by_tags(tags, max_results//4)
            all_datasets.extend(tag_results)
            
        if file_types:
            file_type_results = self.search_by_file_type(file_types, max_results//4)
            all_datasets.extend(file_type_results)
            
        if column_keywords:
            column_results = self.search_by_columns(column_keywords, max_results//4)
            all_datasets.extend(column_results)
        
        # Combine and rank results
        unique_datasets = self._deduplicate_datasets(all_datasets)
        ranked_datasets = self._rank_by_relevance(unique_datasets, keywords, tags, column_keywords)
        
        logger.info(f"Multi-criteria search found {len(ranked_datasets)} unique datasets")
        return ranked_datasets[:max_results]
    
    def _extract_metadata(self, dataset, search_term: str, search_type: str = 'keyword') -> Optional[DatasetMetadata]:
        """Extract metadata from Kaggle dataset object."""
        try:
            # Calculate search score based on match type
            search_score = self._calculate_search_score(dataset, search_term, search_type)
            
            # Extract file types from dataset metadata
            file_types = self._extract_file_types(dataset)
            
            # Estimate rows based on size and file type
            estimated_rows = self._estimate_rows(getattr(dataset, 'total_bytes', 0), file_types)
            
            # Handle tags properly (could be ApiCategory object or list)
            tags = dataset.tags
            if hasattr(tags, '__iter__') and not isinstance(tags, str):
                # Convert to list of strings
                tags_list = []
                for tag in tags:
                    if hasattr(tag, 'name'):
                        tags_list.append(tag.name)
                    else:
                        tags_list.append(str(tag))
                tags = tags_list
            else:
                tags = [str(tags)] if tags else []
            
            metadata = DatasetMetadata(
                ref=dataset.ref,
                title=dataset.title,
                description=getattr(dataset, 'description', '')[:500],
                size_bytes=getattr(dataset, 'total_bytes', 0),
                last_updated=str(getattr(dataset, 'last_updated', 'N/A')),
                download_count=getattr(dataset, 'download_count', 0),
                vote_count=getattr(dataset, 'vote_count', 0),
                usability_rating=getattr(dataset, 'usability_rating', 0.0),
                tags=tags,
                search_score=search_score,
                file_types=file_types,
                estimated_rows=estimated_rows
            )
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error extracting metadata for {dataset.ref}: {e}")
            return None
    
    def _calculate_search_score(self, dataset, search_term: str, search_type: str) -> float:
        """Calculate relevance score for search results."""
        score = 0.0
        search_term_lower = search_term.lower()
        
        # Title match (highest weight)
        if search_term_lower in dataset.title.lower():
            score += 10.0
            
        # Description match
        description = getattr(dataset, 'description', '').lower()
        if search_term_lower in description:
            score += 5.0
            
        # Tag match
        tags = dataset.tags
        if hasattr(tags, '__iter__') and not isinstance(tags, str):
            for tag in tags:
                tag_str = tag.name if hasattr(tag, 'name') else str(tag)
                if search_term_lower in tag_str.lower():
                    score += 8.0
        elif tags:
            tag_str = str(tags)
            if search_term_lower in tag_str.lower():
                score += 8.0
                
        # Usability and popularity factors
        usability_rating = getattr(dataset, 'usability_rating', 0.0)
        vote_count = getattr(dataset, 'vote_count', 0)
        download_count = getattr(dataset, 'download_count', 0)
        
        score += usability_rating * 2.0  # Usability rating (0-10)
        score += min(vote_count / 100.0, 5.0)  # Vote count (capped at 5)
        score += min(download_count / 1000.0, 3.0)  # Downloads (capped at 3)
        
        return score
    
    def _extract_file_types(self, dataset) -> List[str]:
        """Extract file types from dataset metadata."""
        # This would ideally come from dataset file information
        # For now, we'll make educated guesses based on common patterns
        file_types = []
        
        # Check if dataset has file information
        if hasattr(dataset, 'files') and dataset.files:
            for file_info in dataset.files:
                if hasattr(file_info, 'name'):
                    extension = file_info.name.split('.')[-1].lower()
                    if extension not in file_types:
                        file_types.append(extension)
        
        return file_types if file_types else ['unknown']
    
    def _estimate_rows(self, size_bytes: int, file_types: List[str]) -> int:
        """Estimate number of rows based on file size and type."""
        if not file_types or 'unknown' in file_types:
            return 0
            
        # Rough estimates for different file types
        estimates = {
            'csv': size_bytes // 100,  # ~100 bytes per row average
            'json': size_bytes // 200,  # JSON tends to be more verbose
            'parquet': size_bytes // 50,  # Parquet is more compressed
            'xlsx': size_bytes // 150,  # Excel files
            'tsv': size_bytes // 100,   # Similar to CSV
        }
        
        # Use the most common file type for estimation
        primary_type = file_types[0] if file_types else 'csv'
        return estimates.get(primary_type, size_bytes // 100)
    
    def _deduplicate_datasets(self, datasets: List[DatasetMetadata]) -> List[DatasetMetadata]:
        """Remove duplicate datasets based on ref."""
        seen_refs = set()
        unique_datasets = []
        
        for dataset in datasets:
            if dataset.ref not in seen_refs:
                seen_refs.add(dataset.ref)
                unique_datasets.append(dataset)
        
        return unique_datasets
    
    def _rank_by_relevance(self, datasets: List[DatasetMetadata], 
                          keywords: List[str], tags: List[str], 
                          column_keywords: List[str]) -> List[DatasetMetadata]:
        """Rank datasets by relevance to search criteria."""
        
        def calculate_relevance_score(dataset):
            score = dataset.search_score
            
            # Boost score for multiple criteria matches
            if keywords:
                keyword_matches = sum(1 for kw in keywords if kw.lower() in dataset.title.lower())
                score += keyword_matches * 2.0
                
            if tags:
                tag_matches = sum(1 for tag in tags if tag.lower() in [t.lower() for t in dataset.tags])
                score += tag_matches * 3.0
                
            if column_keywords:
                col_matches = sum(1 for col in column_keywords if col.lower() in dataset.description.lower())
                score += col_matches * 1.5
            
            return score
        
        # Sort by relevance score
        datasets.sort(key=calculate_relevance_score, reverse=True)
        return datasets
    
    def export_metadata_index(self, datasets: List[DatasetMetadata], filename: str = None) -> str:
        """Export metadata to CSV for further analysis."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"metadata_index_{timestamp}.csv"
        
        # Convert to DataFrame
        data = []
        for dataset in datasets:
            data.append({
                'ref': dataset.ref,
                'title': dataset.title,
                'description': dataset.description,
                'size_bytes': dataset.size_bytes,
                'size_mb': dataset.size_bytes / (1024 * 1024),
                'last_updated': dataset.last_updated,
                'download_count': dataset.download_count,
                'vote_count': dataset.vote_count,
                'usability_rating': dataset.usability_rating,
                'tags': ', '.join(dataset.tags),
                'search_score': dataset.search_score,
                'file_types': ', '.join(dataset.file_types),
                'estimated_rows': dataset.estimated_rows
            })
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        
        logger.info(f"Metadata index exported to {filename}")
        return filename

def main():
    """Demo the metadata search engine capabilities."""
    
    print("=" * 70)
    print("METADATA SEARCH ENGINE FOR DATA LAKE INDEXING")
    print("=" * 70)
    
    # Initialize search engine
    engine = MetadataSearchEngine()
    
    # Example 1: Keyword search
    print("\n EXAMPLE 1: Keyword Search")
    print("-" * 50)
    
    keywords = ['machine learning', 'customer data', 'sales analytics']
    keyword_results = engine.search_by_keywords(keywords, max_results=20)
    
    print(f"Found {len(keyword_results)} datasets matching keywords: {keywords}")
    for i, dataset in enumerate(keyword_results[:5]):
        print(f"  {i+1}. {dataset.title}")
        print(f"     Ref: {dataset.ref}")
        print(f"     Size: {dataset.size_bytes/1024/1024:.1f} MB")
        print(f"     Score: {dataset.search_score:.1f}")
        print()
    
    # Example 2: Tag-based search
    print("\n EXAMPLE 2: Tag-based Search")
    print("-" * 50)
    
    tags = ['finance', 'time-series', 'classification']
    tag_results = engine.search_by_tags(tags, max_results=15)
    
    print(f"Found {len(tag_results)} datasets matching tags: {tags}")
    for i, dataset in enumerate(tag_results[:3]):
        print(f"  {i+1}. {dataset.title}")
        print(f"     Tags: {', '.join(dataset.tags[:5])}")
        print(f"     Votes: {dataset.vote_count}")
        print()
    
    # Example 3: File type search
    print("\n EXAMPLE 3: File Type Search")
    print("-" * 50)
    
    file_types = ['csv', 'json']
    file_results = engine.search_by_file_type(file_types, max_results=10)
    
    print(f"Found {len(file_results)} datasets with file types: {file_types}")
    for i, dataset in enumerate(file_results[:3]):
        print(f"  {i+1}. {dataset.title}")
        print(f"     File types: {', '.join(dataset.file_types)}")
        print(f"     Size: {dataset.size_bytes/1024/1024:.1f} MB")
        print()
    
    # Example 4: Multi-criteria search
    print("\n EXAMPLE 4: Multi-criteria Search")
    print("-" * 50)
    
    multi_results = engine.multi_criteria_search(
        keywords=['customer', 'analytics'],
        tags=['business'],
        file_types=['csv'],
        column_keywords=['customer_id', 'purchase_amount'],
        max_results=25
    )
    
    print(f"Multi-criteria search found {len(multi_results)} datasets")
    for i, dataset in enumerate(multi_results[:3]):
        print(f"  {i+1}. {dataset.title}")
        print(f"     Score: {dataset.search_score:.1f}")
        print(f"     Downloads: {dataset.download_count}")
        print()
    
    # Export results
    print("\n EXPORTING METADATA INDEX")
    print("-" * 50)
    
    all_results = keyword_results + tag_results + file_results + multi_results
    unique_results = engine._deduplicate_datasets(all_results)
    
    filename = engine.export_metadata_index(unique_results)
    print(f" Exported {len(unique_results)} datasets to {filename}")
    
    # Summary statistics
    print(f"\n SUMMARY STATISTICS")
    print("-" * 50)
    print(f"Total unique datasets found: {len(unique_results)}")
    print(f"Average size: {sum(d.size_bytes for d in unique_results) / len(unique_results) / 1024 / 1024:.1f} MB")
    print(f"Average votes: {sum(d.vote_count for d in unique_results) / len(unique_results):.1f}")
    print(f"Average downloads: {sum(d.download_count for d in unique_results) / len(unique_results):.1f}")
    
    print(f"\n Metadata search engine demo completed!")
    print(f"This system efficiently filters thousands of datasets down to dozens/hundreds")
    print(f"based on metadata-only operations - perfect for data lake indexing!")

if __name__ == "__main__":
    main()
