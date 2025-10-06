from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from kaggle.api.kaggle_api_extended import KaggleApi
from modules.datasets import search_datasets, search_by_files
import tempfile
import os

app = FastAPI(title="Dataset Search API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class DatasetResponse(BaseModel):
    title: str
    reference: str

class SearchResponse(BaseModel):
    datasets: List[DatasetResponse]

class FileUploadResponse(BaseModel):
    message: str
    files_received: int
    datasets: List[DatasetResponse]

class DownloadRequest(BaseModel):
    descriptions: List[str]

class DownloadResponse(BaseModel):
    message: str
    count: int



@app.get("/", response_model=Dict[str, str])
async def root():
    return {"message": "Dataset Search API is running"}

@app.get("/search-keyword", response_model=SearchResponse)
async def search_datasets_by_keyword(keyword: str):
    """
    Search for datasets using a keyword and return an array of titles and references.
    
    Args:
        keyword: The search term to find datasets
        
    Returns:
        SearchResponse: Object containing a list of datasets with titles and references
    """
    try:
        if not keyword or keyword.strip() == "":
            raise HTTPException(status_code=400, detail="Keyword cannot be empty")
        
        results = search_datasets(keyword.strip())
        
        datasets = [
            DatasetResponse(title=title, reference=reference) 
            for title, reference in results
        ]
        
        return SearchResponse(datasets=datasets)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching datasets: {str(e)}")

@app.post("/search-files", response_model=FileUploadResponse)
async def search_datasets_by_files(files: List[UploadFile] = File(...)):
    """
    Search for similar datasets based on uploaded files by extracting column names.
    
    Args:
        files: List of uploaded files (CSV files)
        
    Returns:
        FileUploadResponse: Object containing message, file count, and similar datasets
    """
    temp_files = []
    try:
        if not files or len(files) == 0:
            raise HTTPException(status_code=400, detail="No files uploaded")
        
        # Save uploaded files temporarily
        for file in files:
            if not file.filename:
                continue
                
            # Check if it's a CSV file
            filename = file.filename.lower()
            if not filename.endswith('.csv'):
                continue  # Skip non-CSV files for now
                
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False)
            temp_files.append(temp_file.name)
            
            # Write uploaded content to temporary file
            content = await file.read()
            temp_file.write(content)
            temp_file.close()
        
        if not temp_files:
            raise HTTPException(status_code=400, detail="No valid CSV files uploaded")
        
        # Call search_by_files function for each file
        all_results = []
        for temp_file_path in temp_files:
            try:
                file_results = search_by_files([temp_file_path])
                all_results.extend(file_results)
            except Exception as e:
                print(f"Error processing file {temp_file_path}: {e}")
                continue
        
        # Remove duplicates while preserving order
        seen = set()
        unique_results = []
        for result in all_results:
            if result not in seen:
                seen.add(result)
                unique_results.append(result)
        
        # Convert results to DatasetResponse objects
        datasets = [
            DatasetResponse(title=title, reference=reference) 
            for title, reference in unique_results
        ]
        
        return FileUploadResponse(
            message=f"Found {len(datasets)} similar datasets based on column analysis of uploaded files",
            files_received=len(files),
            datasets=datasets
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")
    
    finally:
        # Clean up temporary files
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except Exception as e:
                print(f"Error deleting temporary file {temp_file}: {e}")

@app.post("/download", response_model=DownloadResponse)
async def download_datasets_endpoint(request: DownloadRequest):
    """
    Download selected datasets using their descriptions (references).
    
    Args:
        request: DownloadRequest containing a list of dataset descriptions/references
        
    Returns:
        DownloadResponse: Confirmation message and count of datasets
    """
    try:
        if not request.descriptions or len(request.descriptions) == 0:
            raise HTTPException(status_code=400, detail="No datasets selected for download")
        
        # TODO: Implement actual download functionality
        # For now, just return a confirmation message
        return DownloadResponse(
            message=f"Download initiated for {len(request.descriptions)} dataset(s)",
            count=len(request.descriptions)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading datasets: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)