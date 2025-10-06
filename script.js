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
        this.downloadDatasets = [];
        this.uploadedFiles = [];
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
        const downloadSelectedBtn = document.getElementById('downloadSelectedBtn');
        
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

        // Download selected functionality
        downloadSelectedBtn.addEventListener('click', () => this.handleDownload());

        // Update download button state
        this.updateDownloadButton();
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
        // Don't automatically update Available Datasets when removing files
        this.renderDownloadDatasets();
        this.updateDownloadButton();
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
                name: dataset.title,
                description: dataset.reference,
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
                name: dataset.title,
                description: dataset.reference,
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
            // Create Kaggle URL from the description/reference
            const kaggleUrl = `https://www.kaggle.com/datasets/${dataset.description}`;
            
            return `
                <div class="dataset-item" data-id="${dataset.id}" draggable="true">
                    <input type="checkbox" class="dataset-checkbox" data-id="${dataset.id}">
                    <div class="dataset-info">
                        <div class="dataset-name">
                            <a href="${kaggleUrl}" target="_blank" rel="noopener noreferrer" class="dataset-link">
                                ${dataset.name}
                            </a>
                        </div>
                        <div class="dataset-description">${dataset.description}</div>
                    </div>
                </div>
            `;
        }).join('');

        // Add event listeners for checkboxes
        this.attachCheckboxListeners();
        
        // Add drag and drop functionality
        this.attachDragAndDropListeners();
    }

    attachCheckboxListeners() {
        const checkboxes = document.querySelectorAll('.dataset-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const datasetId = parseInt(e.target.dataset.id);
                this.toggleDatasetSelection(datasetId);
            });
        });
    }

    attachDragAndDropListeners() {
        const datasetItems = document.querySelectorAll('.dataset-item');
        const downloadContainer = document.getElementById('downloadDatasets');

        datasetItems.forEach(item => {
            let isDragging = false;
            
            item.addEventListener('dragstart', (e) => {
                // Only allow dragging from the dataset item itself, not from links
                if (e.target.classList.contains('dataset-link')) {
                    e.preventDefault();
                    return;
                }
                isDragging = true;
                e.dataTransfer.setData('text/plain', e.target.dataset.id);
                e.target.classList.add('dragging');
            });

            item.addEventListener('dragend', (e) => {
                isDragging = false;
                e.target.classList.remove('dragging');
            });
            
            // Prevent link clicks during drag operations
            item.addEventListener('click', (e) => {
                if (isDragging && e.target.classList.contains('dataset-link')) {
                    e.preventDefault();
                }
            });
        });

        // Download container drag events
        downloadContainer.addEventListener('dragover', (e) => {
            e.preventDefault();
            downloadContainer.classList.add('drag-over');
        });

        downloadContainer.addEventListener('dragleave', (e) => {
            downloadContainer.classList.remove('drag-over');
        });

        downloadContainer.addEventListener('drop', (e) => {
            e.preventDefault();
            downloadContainer.classList.remove('drag-over');
            
            const datasetId = parseInt(e.dataTransfer.getData('text/plain'));
            this.addToDownloadList(datasetId);
        });
    }

    toggleDatasetSelection(datasetId) {
        const dataset = this.availableDatasets.find(d => d.id === datasetId);
        const existingIndex = this.downloadDatasets.findIndex(d => d.id === datasetId);

        if (existingIndex === -1) {
            // Add to download list
            this.downloadDatasets.push(dataset);
        } else {
            // Remove from download list
            this.downloadDatasets.splice(existingIndex, 1);
        }

        this.renderDownloadDatasets();
        this.updateDownloadButton();
    }

    addToDownloadList(datasetId) {
        const dataset = this.availableDatasets.find(d => d.id === datasetId);
        
        if (!dataset) return;

        const existingIndex = this.downloadDatasets.findIndex(d => d.id === datasetId);
        if (existingIndex === -1) {
            this.downloadDatasets.push(dataset);
            
            // Check the corresponding checkbox
            const checkbox = document.querySelector(`.dataset-checkbox[data-id="${datasetId}"]`);
            if (checkbox) {
                checkbox.checked = true;
            }
        }

        this.renderDownloadDatasets();
        this.updateDownloadButton();
    }

    renderDownloadDatasets() {
        const container = document.getElementById('downloadDatasets');
        
        if (this.downloadDatasets.length === 0) {
            container.innerHTML = '<p class="no-data">Selected datasets will appear here.</p>';
            return;
        }

        container.innerHTML = this.downloadDatasets.map(dataset => `
            <div class="dataset-item selected" data-id="${dataset.id}">
                <div class="dataset-info">
                    <div class="dataset-name">${dataset.name}</div>
                    <div class="dataset-description">${dataset.description}</div>
                </div>
                <button class="remove-btn" onclick="datasetManager.removeFromDownloadList(${dataset.id})">×</button>
            </div>
        `).join('');

        // Add remove button styles
        this.addRemoveButtonStyles();
    }

    addRemoveButtonStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .remove-btn {
                background: #dc3545;
                color: white;
                border: none;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                font-size: 18px;
                font-weight: bold;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
                margin-left: auto;
            }
            
            .remove-btn:hover {
                background: #c82333;
                transform: scale(1.1);
            }
        `;
        
        if (!document.querySelector('style[data-remove-btn]')) {
            style.setAttribute('data-remove-btn', 'true');
            document.head.appendChild(style);
        }
    }

    removeFromDownloadList(datasetId) {
        this.downloadDatasets = this.downloadDatasets.filter(d => d.id !== datasetId);
        
        // Uncheck the corresponding checkbox
        const checkbox = document.querySelector(`.dataset-checkbox[data-id="${datasetId}"]`);
        if (checkbox) {
            checkbox.checked = false;
        }

        this.renderDownloadDatasets();
        this.updateDownloadButton();
    }

    clearAll() {
        this.downloadDatasets = [];
        this.availableDatasets = [];
        this.uploadedFiles = [];
        
        document.getElementById('availableDatasets').innerHTML = 
            '<p class="no-data">No search results yet. Upload files or enter a keyword to search for datasets.</p>';
        document.getElementById('downloadDatasets').innerHTML = 
            '<p class="no-data">Selected datasets will appear here.</p>';
        document.getElementById('uploadedFiles').style.display = 'none';
        document.getElementById('fileInput').value = '';
        document.getElementById('searchInput').value = '';
        
        this.updateDownloadButton();
    }

    async handleDownload() {
        if (this.downloadDatasets.length === 0) {
            alert('Please select at least one file to download.');
            return;
        }

        try {
            // Create a zip file with selected files
            const selectedFiles = this.downloadDatasets.map(dataset => dataset.file).filter(file => file);
            
            if (selectedFiles.length === 0) {
                alert('No files available for download.');
                return;
            }

            // For now, we'll trigger individual downloads for each file
            // In a real application, you might want to create a zip file
            selectedFiles.forEach(file => {
                const url = URL.createObjectURL(file);
                const a = document.createElement('a');
                a.href = url;
                a.download = file.name;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            });

            alert(`Downloaded ${selectedFiles.length} file(s) successfully!`);
            
        } catch (error) {
            console.error('Error downloading files:', error);
            alert('Error downloading files. Please try again.');
        }
    }

    updateDownloadButton() {
        const downloadBtn = document.getElementById('downloadSelectedBtn');
        downloadBtn.disabled = this.downloadDatasets.length === 0;
        
        if (this.downloadDatasets.length > 0) {
            downloadBtn.textContent = `Download Selected (${this.downloadDatasets.length})`;
        } else {
            downloadBtn.textContent = 'Download Selected';
        }
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
