#!/usr/bin/env python3
"""
Maximum Collection Engine for Data Lake Indexing
This focuses on collecting AS MANY relevant datasets as possible, not uniqueness.
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
    search_method: str = ""  # Track which method found this dataset

class MaximumCollectionEngine:
    """
    Maximum dataset collection engine for data lake indexing.
    Focuses on getting AS MANY relevant datasets as possible.
    """
    
    def __init__(self):
        """Initialize the collection engine with Kaggle API."""
        self.api = KaggleApi()
        self.api.authenticate()
        self.collection_stats = {
            'keyword_searches': 0,
            'tag_searches': 0,
            'file_type_searches': 0,
            'column_searches': 0,
            'total_datasets_found': 0
        }
        logger.info("Maximum Collection Engine initialized")
    
    def collect_by_keyword_variations(self, base_keywords: List[str], max_per_variation: int = 50) -> List[DatasetMetadata]:
        """
        Collect datasets using multiple keyword variations to maximize coverage.
        
        Args:
            base_keywords: Base keywords to expand
            max_per_variation: Max datasets per keyword variation
            
        Returns:
            List of DatasetMetadata objects
        """
        all_datasets = []
        
        for base_keyword in base_keywords:
            # Create multiple variations of each keyword
            variations = [
                base_keyword,
                f"{base_keyword} data",
                f"{base_keyword} dataset", 
                f"{base_keyword} analytics",
                f"{base_keyword} analysis",
                f"{base_keyword} machine learning",
                f"{base_keyword} csv",
                f"{base_keyword} json"
            ]
            
            logger.info(f"Collecting datasets for base keyword: '{base_keyword}'")
            
            for variation in variations:
                try:
                    results = self.api.dataset_list(search=variation, sort_by='hottest')
                    
                    for dataset in results[:max_per_variation]:
                        metadata = self._extract_metadata(dataset, variation, 'keyword')
                        if metadata:
                            metadata.search_method = f"keyword:{variation}"
                            all_datasets.append(metadata)
                            
                    self.collection_stats['keyword_searches'] += 1
                    
                except Exception as e:
                    logger.error(f"Error searching for '{variation}': {e}")
        
        self.collection_stats['total_datasets_found'] += len(all_datasets)
        logger.info(f"Keyword collection found {len(all_datasets)} datasets")
        return all_datasets
    
    def collect_by_tag_expansion(self, base_tags: List[str], max_per_tag: int = 30) -> List[DatasetMetadata]:
        """
        Collect datasets using tag expansion to maximize coverage.
        
        Args:
            base_tags: Base tags to expand
            max_per_tag: Max datasets per tag
            
        Returns:
            List of DatasetMetadata objects
        """
        all_datasets = []
        
        # Define tag expansion rules
        tag_expansions = {
            'finance': ['business', 'economics', 'banking', 'investment', 'financial', 'money', 'credit', 'loan', 'market', 'trading'],
            'healthcare': ['health', 'medical', 'medicine', 'patient', 'clinical', 'hospital', 'diagnosis', 'treatment'],
            'technology': ['tech', 'software', 'computer', 'ai', 'machine learning', 'data science', 'programming'],
            'business': ['marketing', 'sales', 'customer', 'revenue', 'profit', 'company', 'corporate'],
            'education': ['student', 'learning', 'academic', 'school', 'university', 'course', 'training']
        }
        
        for base_tag in base_tags:
            # Get expanded tags
            expanded_tags = tag_expansions.get(base_tag, [base_tag])
            
            logger.info(f"Collecting datasets for base tag: '{base_tag}' (expanding to {len(expanded_tags)} tags)")
            
            for tag in expanded_tags:
                try:
                    search_query = f"tag:{tag}"
                    results = self.api.dataset_list(search=search_query, sort_by='hottest')
                    
                    for dataset in results[:max_per_tag]:
                        metadata = self._extract_metadata(dataset, tag, 'tag')
                        if metadata:
                            metadata.search_method = f"tag:{tag}"
                            all_datasets.append(metadata)
                            
                    self.collection_stats['tag_searches'] += 1
                    
                except Exception as e:
                    logger.error(f"Error searching for tag '{tag}': {e}")
        
        self.collection_stats['total_datasets_found'] += len(all_datasets)
        logger.info(f"Tag collection found {len(all_datasets)} datasets")
        return all_datasets
    
    def collect_by_file_types(self, file_types: List[str], max_per_type: int = 25) -> List[DatasetMetadata]:
        """
        Collect datasets by file types to maximize coverage.
        
        Args:
            file_types: File types to search for
            max_per_type: Max datasets per file type
            
        Returns:
            List of DatasetMetadata objects
        """
        all_datasets = []
        
        for file_type in file_types:
            logger.info(f"Collecting datasets for file type: '{file_type}'")
            
            try:
                results = self.api.dataset_list(file_type=file_type, sort_by='hottest')
                
                for dataset in results[:max_per_type]:
                    metadata = self._extract_metadata(dataset, file_type, 'file_type')
                    if metadata:
                        metadata.search_method = f"file_type:{file_type}"
                        all_datasets.append(metadata)
                        
                self.collection_stats['file_type_searches'] += 1
                
            except Exception as e:
                logger.error(f"Error searching for file type '{file_type}': {e}")
        
        self.collection_stats['total_datasets_found'] += len(all_datasets)
        logger.info(f"File type collection found {len(all_datasets)} datasets")
        return all_datasets
    
    def collect_by_column_keywords(self, column_keywords: List[str], max_per_keyword: int = 20) -> List[DatasetMetadata]:
        """
        Collect datasets by column keywords to maximize coverage.
        
        Args:
            column_keywords: Column names/keywords to search for
            max_per_keyword: Max datasets per keyword
            
        Returns:
            List of DatasetMetadata objects
        """
        all_datasets = []
        
        for keyword in column_keywords:
            logger.info(f"Collecting datasets for column keyword: '{keyword}'")
            
            # Create multiple search queries for each keyword
            search_queries = [
                keyword,
                f"column {keyword}",
                f"field {keyword}",
                f"feature {keyword}",
                f"variable {keyword}",
                f"{keyword} data"
            ]
            
            for query in search_queries:
                try:
                    results = self.api.dataset_list(search=query, sort_by='hottest')
                    
                    for dataset in results[:max_per_keyword]:
                        metadata = self._extract_metadata(dataset, keyword, 'column')
                        if metadata:
                            metadata.search_method = f"column:{keyword}"
                            all_datasets.append(metadata)
                            
                    self.collection_stats['column_searches'] += 1
                    
                except Exception as e:
                    logger.error(f"Error searching for '{query}': {e}")
        
        self.collection_stats['total_datasets_found'] += len(all_datasets)
        logger.info(f"Column keyword collection found {len(all_datasets)} datasets")
        return all_datasets
    
    def comprehensive_collection(self, domain: str, max_total: int = 500) -> List[DatasetMetadata]:
        """
        Perform comprehensive collection using all methods for maximum coverage.
        
        Args:
            domain: Domain to collect datasets for
            max_total: Maximum total datasets to collect
            
        Returns:
            List of DatasetMetadata objects
        """
        logger.info(f"Starting comprehensive collection for domain: '{domain}'")
        
        all_datasets = []
        
        # Method 1: Keyword variations
        print(f"\n Method 1: Keyword variations for '{domain}'")
        keyword_datasets = self.collect_by_keyword_variations([domain], max_per_variation=30)
        all_datasets.extend(keyword_datasets)
        print(f"  Collected: {len(keyword_datasets)} datasets")
        
        # Method 2: Tag expansion
        print(f"\n Method 2: Tag expansion for '{domain}'")
        tag_datasets = self.collect_by_tag_expansion([domain], max_per_tag=20)
        all_datasets.extend(tag_datasets)
        print(f"  Collected: {len(tag_datasets)} datasets")
        
        # Method 3: File types
        print(f"\n Method 3: File type collection")
        file_datasets = self.collect_by_file_types(['csv', 'json', 'xlsx'], max_per_type=15)
        all_datasets.extend(file_datasets)
        print(f"  Collected: {len(file_datasets)} datasets")
        
        # Method 4: Column keywords (domain-specific)
        print(f"\n Method 4: Column keyword collection for '{domain}'")
        column_keywords = self._get_domain_column_keywords(domain)
        column_datasets = self.collect_by_column_keywords(column_keywords, max_per_keyword=10)
        all_datasets.extend(column_datasets)
        print(f"  Collected: {len(column_datasets)} datasets")
        
        # Combine all results (keep ALL for maximum coverage)
        total_collected = len(all_datasets)
        logger.info(f"Comprehensive collection found {total_collected} total datasets")
        
        # Sort by relevance score
        all_datasets.sort(key=lambda x: x.search_score, reverse=True)
        
        # Limit to max_total if needed
        if len(all_datasets) > max_total:
            all_datasets = all_datasets[:max_total]
            logger.info(f"Limited to top {max_total} datasets by relevance")
        
        return all_datasets
    
    def _get_domain_column_keywords(self, domain: str) -> List[str]:
        """Get domain-specific column keywords."""
        domain_keywords = {
            'finance': ['amount', 'price', 'cost', 'revenue', 'profit', 'transaction', 'payment', 'balance', 'account', 'interest'],
            'healthcare': ['patient', 'diagnosis', 'treatment', 'symptom', 'medication', 'age', 'gender', 'blood', 'pressure'],
            'technology': ['user', 'session', 'click', 'download', 'performance', 'error', 'log', 'timestamp', 'device'],
            'business': ['customer', 'order', 'product', 'sales', 'marketing', 'campaign', 'conversion', 'retention'],
            'education': ['student', 'grade', 'course', 'assignment', 'score', 'attendance', 'teacher', 'subject']
        }
        
        return domain_keywords.get(domain, ['id', 'name', 'date', 'value', 'type', 'category'])
    
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
                estimated_rows=estimated_rows,
                search_method=""
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
    
    def export_collection_index(self, datasets: List[DatasetMetadata], filename: str = None) -> str:
        """Export collection to CSV for analysis."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"maximum_collection_index_{timestamp}.csv"
        
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
                'search_method': dataset.search_method,
                'file_types': ', '.join(dataset.file_types),
                'estimated_rows': dataset.estimated_rows
            })
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        
        logger.info(f"Collection index exported to {filename}")
        return filename
    
    def print_collection_stats(self):
        """Print collection statistics."""
        print(f"\n COLLECTION STATISTICS:")
        print(f"  Keyword searches: {self.collection_stats['keyword_searches']}")
        print(f"  Tag searches: {self.collection_stats['tag_searches']}")
        print(f"  File type searches: {self.collection_stats['file_type_searches']}")
        print(f"  Column searches: {self.collection_stats['column_searches']}")
        print(f"  Total datasets found: {self.collection_stats['total_datasets_found']}")

def main():
    """Demo the maximum collection engine."""
    
    print("=" * 80)
    print("MAXIMUM COLLECTION ENGINE DEMO")
    print("=" * 80)
    
    # Initialize engine
    engine = MaximumCollectionEngine()
    
    # Perform comprehensive collection for finance domain
    domain = "finance"
    print(f"\n🎯 Performing maximum collection for domain: {domain}")
    
    datasets = engine.comprehensive_collection(domain, max_total=200)
    
    # Print results
    print(f"\n COLLECTION RESULTS:")
    print(f"  Total datasets collected: {len(datasets)}")
    
    # Show top results
    print(f"\n TOP 15 DATASETS:")
    for i, dataset in enumerate(datasets[:15]):
        print(f"  {i+1:2d}. {dataset.title}")
        print(f"      Ref: {dataset.ref}")
        print(f"      Size: {dataset.size_bytes/1024/1024:.1f} MB")
        print(f"      Downloads: {dataset.download_count:,}")
        print(f"      Score: {dataset.search_score:.1f}")
        print(f"      Method: {dataset.search_method}")
        print()
    
    # Export results
    filename = engine.export_collection_index(datasets)
    
    # Print statistics
    engine.print_collection_stats()
    
    print(f"\n MAXIMUM COLLECTION COMPLETED!")
    print(f"  Exported {len(datasets)} datasets to {filename}")
    print(f"  Ready for data lake indexing and processing!")

if __name__ == "__main__":
    main()
