// Sample dataset data for demonstration
const sampleDatasets = [
    {
        id: 1,
        name: "COVID-19 Global Dataset",
        description: "Comprehensive dataset containing COVID-19 cases, deaths, and recovery data worldwide",
        size: "2.3 MB",
        category: "Health"
    },
    {
        id: 2,
        name: "Stock Market Data 2023",
        description: "Daily stock prices and trading volume for major companies",
        size: "15.7 MB",
        category: "Finance"
    },
    {
        id: 3,
        name: "Weather Patterns Analysis",
        description: "Historical weather data including temperature, humidity, and precipitation",
        size: "8.9 MB",
        category: "Environment"
    },
    {
        id: 4,
        name: "Customer Purchase History",
        description: "E-commerce transaction data with customer demographics",
        size: "45.2 MB",
        category: "Business"
    },
    {
        id: 5,
        name: "Social Media Sentiment",
        description: "Twitter and Facebook sentiment analysis data",
        size: "12.1 MB",
        category: "Social"
    },
    {
        id: 6,
        name: "Machine Learning Features",
        description: "Preprocessed features for ML model training",
        size: "67.8 MB",
        category: "Technology"
    },
    {
        id: 7,
        name: "Real Estate Prices",
        description: "Property prices and characteristics across major cities",
        size: "23.4 MB",
        category: "Real Estate"
    },
    {
        id: 8,
        name: "Energy Consumption Data",
        description: "Electricity and gas consumption patterns by region",
        size: "31.6 MB",
        category: "Energy"
    }
];

class DatasetManager {
    constructor() {
        this.availableDatasets = [];
        this.uploadedFiles = [];
        this.selectedDataset = null;
        this.currentMode = 'files'; // 'files' or 'keyword'
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        const fileInput = document.getElementById('fileInput');
        const uploadBtn = document.getElementById('uploadBtn');
        const fileUploadArea = document.getElementById('fileUploadArea');
        const searchInput = document.getElementById('searchInput');
        const searchBtn = document.getElementById('searchBtn');
        const clearAllBtn = document.getElementById('clearAllBtn');
        
        // Mode switching
        const modeRadios = document.querySelectorAll('input[name="searchMode"]');
        modeRadios.forEach(radio => {
            radio.addEventListener('change', (e) => this.handleModeChange(e.target.value));
        });

        // File upload functionality
        uploadBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            fileInput.click();
        });
        
        fileInput.addEventListener('change', (e) => {
            if (e.target.files && e.target.files.length > 0) {
                this.handleFileSelect(e.target.files);
                // Clear the input value to allow selecting the same file again
                e.target.value = '';
            }
        });
        
        // Drag and drop functionality
        fileUploadArea.addEventListener('click', (e) => {
            // Only trigger if the click is not on the upload button
            if (e.target !== uploadBtn && !uploadBtn.contains(e.target)) {
                fileInput.click();
            }
        });
        fileUploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        fileUploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        fileUploadArea.addEventListener('drop', (e) => this.handleDrop(e));

        // Search functionality
        searchBtn.addEventListener('click', () => this.handleSearch());
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.handleSearch();
            }
        });

        // Clear all functionality
        clearAllBtn.addEventListener('click', () => this.clearAll());
    }

    // File validation
    isValidFileType(file) {
        const allowedTypes = ['.csv', '.pdf', '.docx', '.xlsx'];
        const fileName = file.name.toLowerCase();
        return allowedTypes.some(type => fileName.endsWith(type));
    }

    // Get file icon based on type
    getFileIcon(fileName) {
        const ext = fileName.toLowerCase().split('.').pop();
        const icons = {
            'csv': '📊',
            'pdf': '📄',
            'docx': '📝',
            'xlsx': '📈'
        };
        return icons[ext] || '📁';
    }

    // Format file size
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Handle file selection
    handleFileSelect(files) {
        console.log('Files selected:', files.length);
        
        const validFiles = [];
        const invalidFiles = [];

        Array.from(files).forEach(file => {
            console.log('Processing file:', file.name, 'Type:', file.type, 'Size:', file.size);
            if (this.isValidFileType(file)) {
                validFiles.push(file);
            } else {
                invalidFiles.push(file);
            }
        });

        if (invalidFiles.length > 0) {
            const invalidNames = invalidFiles.map(f => f.name).join(', ');
            alert(`The following files are not supported: ${invalidNames}\n\nSupported formats: CSV, PDF, Word (.docx), Excel (.xlsx)`);
        }

        if (validFiles.length > 0) {
            this.uploadedFiles = [...this.uploadedFiles, ...validFiles];
            console.log('Total uploaded files:', this.uploadedFiles.length);
            this.renderUploadedFiles();
            // Don't automatically populate Available Datasets - only show uploaded files list
        }
    }

    // Handle drag over
    handleDragOver(e) {
        e.preventDefault();
        e.currentTarget.classList.add('drag-over');
    }

    // Handle drag leave
    handleDragLeave(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('drag-over');
    }

    // Handle drop
    handleDrop(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        this.handleFileSelect(files);
    }

    // Process uploaded files and create dataset entries
    processUploadedFiles() {
        this.availableDatasets = this.uploadedFiles.map((file, index) => ({
            id: index + 1,
            name: file.name,
            description: `Uploaded file: ${file.name} (${this.formatFileSize(file.size)})`,
            size: this.formatFileSize(file.size),
            category: 'Uploaded File',
            file: file
        }));

        this.renderAvailableDatasets();
    }

    // Render uploaded files list
    renderUploadedFiles() {
        const container = document.getElementById('uploadedFiles');
        const fileList = document.getElementById('fileList');

        if (this.uploadedFiles.length === 0) {
            container.style.display = 'none';
            return;
        }

        container.style.display = 'block';
        fileList.innerHTML = this.uploadedFiles.map((file, index) => `
            <div class="file-item">
                <div class="file-info">
                    <span class="file-icon">${this.getFileIcon(file.name)}</span>
                    <span class="file-name">${file.name}</span>
                    <span class="file-size">${this.formatFileSize(file.size)}</span>
                </div>
                <button class="remove-file-btn" onclick="datasetManager.removeFile(${index})">×</button>
            </div>
        `).join('');
    }

    // Remove file from uploaded files
    removeFile(index) {
        this.uploadedFiles.splice(index, 1);
        this.renderUploadedFiles();
    }

    // Handle mode change
    handleModeChange(mode) {
        this.currentMode = mode;
        const fileUploadArea = document.getElementById('fileUploadArea');
        const searchInputArea = document.getElementById('searchInputArea');
        
        if (mode === 'files') {
            fileUploadArea.style.display = 'flex';
            searchInputArea.style.display = 'none';
        } else {
            fileUploadArea.style.display = 'none';
            searchInputArea.style.display = 'flex';
        }
    }

    // Handle search (unified method for both modes)
    async handleSearch() {
        if (this.currentMode === 'files') {
            await this.handleSearchWithFiles();
        } else {
            await this.handleSearchWithKeyword();
        }
    }

    // Handle search with files
    async handleSearchWithFiles() {
        if (this.uploadedFiles.length === 0) {
            alert('Please upload at least one file before searching for similar datasets.');
            return;
        }

        try {
            // Show loading state
            const container = document.getElementById('availableDatasets');
            container.innerHTML = '<p class="loading">Searching for similar datasets...</p>';

            // Create FormData with uploaded files
            const formData = new FormData();
            
            // Add each uploaded file to FormData
            this.uploadedFiles.forEach(file => {
                formData.append('files', file);
            });

            console.log(`Sending ${this.uploadedFiles.length} files to backend for search`);

            // Call the FastAPI backend with POST request and FormData
            const response = await fetch(`${CONFIG.BACKEND_URL}/search-files`, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }
            
            const data = await response.json();
            console.log('Search response:', data);
            
            // Transform the API response to match the expected format
            this.availableDatasets = data.datasets.map((dataset, index) => ({
                id: index + 1,
                title: dataset.title,
                reference: dataset.reference,
                license: dataset.license,
                tags: dataset.tags,
                last_updated: dataset.last_updated,
                files: dataset.files,
                category: 'Similar Dataset'
            }));

            this.renderAvailableDatasets();
            
            // Show success message
            console.log(data.message);
            
        } catch (error) {
            console.error('Error searching similar datasets:', error);
            const container = document.getElementById('availableDatasets');
            container.innerHTML = `<p class="error">Error searching for similar datasets. Please make sure the backend server is running on ${CONFIG.BACKEND_URL}</p>`;
        }
    }

    // Handle search with keyword
    async handleSearchWithKeyword() {
        const searchInput = document.getElementById('searchInput');
        const searchTerm = searchInput.value.trim();

        if (!searchTerm) {
            alert('Please enter a search keyword');
            return;
        }

        try {
            // Show loading state
            const container = document.getElementById('availableDatasets');
            container.innerHTML = '<p class="loading">Searching datasets...</p>';

            // Call the FastAPI backend
            const response = await fetch(`${CONFIG.BACKEND_URL}/search-keyword?keyword=${encodeURIComponent(searchTerm)}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Transform the API response to match the expected format
            this.availableDatasets = data.datasets.map((dataset, index) => ({
                id: index + 1,
                title: dataset.title,
                reference: dataset.reference,
                license: dataset.license,
                tags: dataset.tags,
                last_updated: dataset.last_updated,
                files: dataset.files,
                category: 'Search Result'
            }));

            this.renderAvailableDatasets();
            
        } catch (error) {
            console.error('Error searching datasets:', error);
            const container = document.getElementById('availableDatasets');
            container.innerHTML = `<p class="error">Error searching datasets. Please make sure the backend server is running on ${CONFIG.BACKEND_URL}</p>`;
        }
    }

    renderAvailableDatasets() {
        const container = document.getElementById('availableDatasets');
        
        if (this.availableDatasets.length === 0) {
            container.innerHTML = '<p class="no-data">No datasets found matching your search criteria.</p>';
            return;
        }

        container.innerHTML = this.availableDatasets.map(dataset => {
            // Create Kaggle URL from the reference
            const kaggleUrl = `https://www.kaggle.com/datasets/${dataset.reference}`;
            
            return `
                <div class="dataset-item" data-id="${dataset.id}" onclick="datasetManager.selectDataset(${dataset.id})">
                    <div class="dataset-info">
                        <div class="dataset-title">
                            <a href="${kaggleUrl}" target="_blank" rel="noopener noreferrer" class="dataset-link">
                                ${dataset.title}
                            </a>
                        </div>
                        <div class="dataset-reference">${dataset.reference}</div>
                        <div class="dataset-license">License: ${dataset.license}</div>
                        <div class="dataset-last-updated">Updated: ${dataset.last_updated}</div>
                        <div class="dataset-tags">
                            ${dataset.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    selectDataset(datasetId) {
        this.selectedDataset = this.availableDatasets.find(d => d.id === datasetId);
        this.renderFilesList();
    }

    renderFilesList() {
        const container = document.getElementById('filesList');
        
        if (!this.selectedDataset) {
            container.innerHTML = '<p class="no-data">Click on a dataset to view its files.</p>';
            return;
        }

        if (!this.selectedDataset.files || this.selectedDataset.files.length === 0) {
            container.innerHTML = '<p class="no-data">No files available for this dataset.</p>';
            return;
        }

        container.innerHTML = `
            <div class="files-header">
                <h3>Files in "${this.selectedDataset.title}"</h3>
            </div>
            <div class="files-list">
                ${this.selectedDataset.files.map(file => `
                    <div class="file-item">
                        <div class="file-name">${file[0]}</div>
                        <div class="file-size">${file[1]}</div>
                    </div>
                `).join('')}
            </div>
        `;
    }


    clearAll() {
        this.availableDatasets = [];
        this.uploadedFiles = [];
        this.selectedDataset = null;
        
        document.getElementById('availableDatasets').innerHTML = 
            '<p class="no-data">No search results yet. Upload files or enter a keyword to search for datasets.</p>';
        document.getElementById('filesList').innerHTML = 
            '<p class="no-data">Click on a dataset to view its files.</p>';
        document.getElementById('uploadedFiles').style.display = 'none';
        document.getElementById('fileInput').value = '';
        document.getElementById('searchInput').value = '';
    }

}

// Initialize the application
const datasetManager = new DatasetManager();

// Add some demo functionality
document.addEventListener('DOMContentLoaded', () => {
    console.log('File Upload & Dataset Manager initialized');
    
    // Add a welcome message
    setTimeout(() => {
        const uploadArea = document.getElementById('fileUploadArea');
        if (uploadArea) {
            console.log('Upload area ready. Supported formats: CSV, PDF, Word (.docx), Excel (.xlsx)');
        }
    }, 1000);
});
