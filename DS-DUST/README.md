# DS-DUST: Data Science Data Lake Utility and Search Tool

This project is designed for experimenting with extracting, indexing, and managing datasets using data lakes to enhance and diversify existing datasets. The initial focus is on testing Kaggle API and its indexing capabilities.

## 🚀 Quick Start

### 1. Virtual Environment Setup

The project is already configured with a virtual environment. To activate it:

```bash
source venv/bin/activate
```

### 2. Kaggle API Authentication

Before running any tests, you need to set up Kaggle API credentials:

```bash
python setup_kaggle_auth.py
```

This will guide you through the authentication process.

**Manual Setup (if needed):**
1. Go to [Kaggle Account Settings](https://www.kaggle.com/account)
2. Scroll to the 'API' section and click 'Create New API Token'
3. Download the `kaggle.json` file
4. Move it to `~/.kaggle/kaggle.json`
5. Set proper permissions: `chmod 600 ~/.kaggle/kaggle.json`

### 3. Run Metadata Search Engine

```bash
python metadata_search_engine.py
```

Or for maximum dataset collection:

```bash
python maximum_collection_engine.py
```

## 📁 Project Structure

```
DS-DUST/
├── venv/                          # Virtual environment
├── metadata_search_engine.py     # Core metadata search engine
├── maximum_collection_engine.py  # Maximum dataset collection engine
├── setup_kaggle_auth.py          # Authentication setup helper
├── activate_env.sh               # Environment activation script
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── comprehensive_finance_index.csv # Example dataset index
└── downloaded_datasets/          # Directory for downloaded datasets (created during tests)
```

## 🧪 Core Features

The metadata search engines provide:

### 1. Dataset Search Capabilities
- Search by keywords ('machine learning', 'data science', 'time series', 'image classification')
- Filter by file type, sort options
- Pagination support

### 2. Dataset Metadata Extraction
- Detailed dataset information (title, description, size, downloads, votes)
- File listings with sizes
- Tags and usability ratings
- Last updated timestamps

### 3. Dataset Indexing
- Create searchable index of datasets
- Export to CSV format with timestamps
- Metadata aggregation and analysis

### 4. Dataset Download
- Download complete datasets
- Download specific files
- Automatic unzipping
- Organized storage structure

## 📊 Sample Output

The metadata search engines will:
1. Search for datasets across multiple categories using various methods
2. Extract comprehensive metadata for all results
3. Create a searchable CSV index with deduplication
4. Generate summary statistics and export results

Example output from comprehensive search:
```
📊 TOTAL COLLECTION RESULTS:
  Raw datasets collected: 240
  Unique datasets: 190

🏆 TOP 10 RESULTS:
  1. US Consumer Finance Complaints
     Size: 84.5 MB
     Downloads: 26,396
     Score: 26.1

  2. US Funds dataset from Yahoo Finance
     Size: 353.3 MB
     Downloads: 18,955
     Score: 25.7
```

## 🔧 Dependencies

All dependencies are listed in `requirements.txt`:

- **kaggle**: Official Kaggle API client
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **requests**: HTTP library
- **jupyter**: Interactive development environment
- **matplotlib**: Plotting library
- **seaborn**: Statistical data visualization
- **scikit-learn**: Machine learning library

## 🎯 Next Steps for Data Lake Implementation

Based on the Kaggle API testing, future enhancements could include:

1. **Multi-Source Integration**: Extend beyond Kaggle to include other data sources
2. **Advanced Indexing**: Implement full-text search, semantic indexing
3. **Data Quality Assessment**: Automated quality scoring and validation
4. **Metadata Enrichment**: Add data lineage, provenance tracking
5. **API Development**: REST API for dataset discovery and access
6. **Storage Optimization**: Implement data partitioning and compression
7. **Real-time Updates**: Webhook integration for new dataset notifications

## 🐛 Troubleshooting

### Common Issues:

1. **Authentication Error**: Make sure `~/.kaggle/kaggle.json` exists and has correct permissions
2. **Import Errors**: Ensure virtual environment is activated and all packages are installed
3. **Download Failures**: Check internet connection and Kaggle API status
4. **Permission Denied**: Run `chmod 600 ~/.kaggle/kaggle.json`

### Getting Help:

- Check Kaggle API documentation: https://www.kaggle.com/docs/api
- Review error messages in the console output
- Ensure you have an active Kaggle account

## 📝 License

This project is for educational and research purposes. Please respect Kaggle's terms of service when using their API.

---

**Ready to explore data lakes?** Run `python test_kaggle_api.py` to get started! 🚀
