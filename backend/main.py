from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from kaggle.api.kaggle_api_extended import KaggleApi
from modules.datasets import search_datasets

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

class DownloadRequest(BaseModel):
    descriptions: List[str]

class DownloadResponse(BaseModel):
    message: str
    count: int



@app.get("/", response_model=Dict[str, str])
async def root():
    return {"message": "Dataset Search API is running"}

@app.get("/search", response_model=SearchResponse)
async def search_datasets_endpoint(keyword: str):
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