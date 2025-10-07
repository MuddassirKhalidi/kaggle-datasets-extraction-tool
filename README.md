# Data Lakes Research - Dataset Search Platform

A web application for searching and discovering datasets using Kaggle API with both keyword-based and file-based search capabilities.

## 📁 Directory Structure

```
src/
├── backend/                          # FastAPI backend server
│   ├── main.py                      # Main FastAPI application
│   ├── modules/
│   │   ├── __init__.py
│   │   └── datasets.py              # Dataset search logic with rate limiting
│   ├── requirements.txt             # Python dependencies
│   └── venv/                        # Virtual environment
├── DS-DUST/                         # Alternative dataset search tools
│   ├── activate_env.sh              # Environment activation script
│   ├── comprehensive_finance_index.csv
│   ├── maximum_collection_engine.py
│   ├── metadata_search_engine.py
│   ├── quick_search_example.py
│   ├── search_datasets.py
│   ├── setup_kaggle_auth.py
│   └── requirements.txt
├── index.html                       # Main frontend HTML
├── script.js                        # Frontend JavaScript
├── styles.css                       # Frontend CSS styling
├── config.js                        # Frontend configuration
└── README.md                        # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+ 
- Node.js (optional, for serving frontend files)
- Kaggle API credentials

### 1. Kaggle API Setup

Before running the application, you need to set up Kaggle API authentication:

#### Option A: Automated Setup (Recommended)
```bash
cd DS-DUST
python setup_kaggle_auth.py
```

#### Option B: Manual Setup
1. Go to [Kaggle Account Settings](https://www.kaggle.com/account)
2. Scroll to the 'API' section and click 'Create New API Token'
3. Download the `kaggle.json` file
4. Move it to `~/.kaggle/kaggle.json`
5. Set proper permissions:
   ```bash
   mkdir -p ~/.kaggle
   mv kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   ```

### 2. Backend Setup and Run

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
python main.py
```

The backend will start on `http://localhost:8000`

### 3. Frontend Setup and Run

#### Option A: Simple HTTP Server (Recommended)
```bash
# From the src/ directory, serve the frontend files
python -m http.server 3000
```

#### Option B: Using Node.js
```bash
# Install a simple HTTP server
npm install -g http-server

# Serve the frontend
http-server -p 3000
```

#### Option C: Open directly in browser
Simply open `index.html` in your web browser.

The frontend will be available at `http://localhost:3000`

## 🔧 Configuration

### Backend Configuration

The backend uses the following default settings:
- **Port**: 8000
- **Rate Limiting**: 2 seconds between API calls
- **Max Retries**: 3 attempts with exponential backoff
- **Default Pages**: 5 pages per search

### Frontend Configuration

Edit `config.js` to modify:
- Backend URL (default: `http://localhost:8000`)
- API endpoints
- Other frontend settings

## 📖 Usage

### 1. Keyword Search
1. Open the frontend in your browser
2. Select "Keyword Search" mode
3. Enter a search term (e.g., "financial data", "housing prices")
4. Click "Search" to find relevant datasets

### 2. File-Based Search
1. Select "File Upload" mode
2. Upload one or more CSV files
3. The system will extract column names and search for similar datasets
4. Results will show datasets with matching column structures

### 3. Dataset Information
Each dataset result includes:
- **Title**: Dataset name
- **Reference**: Kaggle dataset reference
- **License**: Dataset license information
- **Tags**: Relevant tags and categories
- **Last Updated**: When the dataset was last modified
- **Files**: List of files in the dataset with sizes

## 🔍 Features

### Rate Limiting
- Built-in rate limiting to respect Kaggle API limits
- Automatic retry with exponential backoff
- Conservative delays between requests

### Search Options
- **Keyword Search**: Search by terms like "machine learning", "financial data"
- **File-Based Search**: Upload CSV files to find similar datasets
- **Smart Stopping**: Stops immediately when no results are found

### Dataset Details
- Click on any dataset to view its files
- Direct links to Kaggle datasets
- File size information
- License and metadata

## 🛠️ API Endpoints

### Backend API (FastAPI)

- `GET /` - Health check
- `GET /search-keyword?keyword={term}` - Search datasets by keyword
- `POST /search-files` - Search datasets by uploaded files
- `POST /download` - Download selected datasets (placeholder)

### Example API Usage

```bash
# Search by keyword
curl "http://localhost:8000/search-keyword?keyword=financial"

# Search by files (requires multipart/form-data)
curl -X POST "http://localhost:8000/search-files" \
  -F "files=@your_file.csv"
```

## 📦 Dependencies

### Backend Dependencies (`backend/requirements.txt`)
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `kaggle` - Kaggle API client
- `pandas` - Data manipulation
- `pydantic` - Data validation

### Frontend Dependencies
- Pure HTML, CSS, and JavaScript (no build process required)
- Modern browser with ES6 support

## 🔧 Development

### Backend Development
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Adding New Features
1. **Backend**: Add new endpoints in `main.py`
2. **Frontend**: Modify `script.js` for new functionality
3. **Styling**: Update `styles.css` for UI changes

### Rate Limiting Configuration
Edit `backend/modules/datasets.py` to adjust:
- `min_delay`: Minimum delay between requests
- `max_delay`: Maximum backoff delay
- `base_delay`: Base delay for exponential backoff

## 🐛 Troubleshooting

### Common Issues

1. **Kaggle API Authentication Error**
   ```bash
   # Fix permissions
   chmod 600 ~/.kaggle/kaggle.json
   ```

2. **Rate Limiting Errors (429)**
   - The system automatically handles rate limits
   - Increase delays in `datasets.py` if needed

3. **Frontend Can't Connect to Backend**
   - Ensure backend is running on port 8000
   - Check `config.js` for correct backend URL
   - Verify CORS settings in `main.py`

4. **No Search Results**
   - Try different search terms
   - Check if Kaggle API is accessible
   - Verify your API credentials

### Logs
- Backend logs are displayed in the terminal
- Frontend errors are shown in browser console (F12)