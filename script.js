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
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        const searchInput = document.getElementById('searchInput');
        const searchBtn = document.getElementById('searchBtn');
        const clearAllBtn = document.getElementById('clearAllBtn');
        const downloadSelectedBtn = document.getElementById('downloadSelectedBtn');

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

    async handleSearch() {
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
            const response = await fetch(`${CONFIG.BACKEND_URL}/search?keyword=${encodeURIComponent(searchTerm)}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Transform the API response to match the expected format
            this.availableDatasets = data.datasets.map((dataset, index) => ({
                id: index + 1,
                name: dataset.title,
                description: dataset.reference,
                category: 'Kaggle Dataset'
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

        container.innerHTML = this.availableDatasets.map(dataset => `
            <div class="dataset-item" data-id="${dataset.id}" draggable="true">
                <input type="checkbox" class="dataset-checkbox" data-id="${dataset.id}">
                <div class="dataset-info">
                    <div class="dataset-name">${dataset.name}</div>
                    <div class="dataset-description">${dataset.description}</div>
                </div>
            </div>
        `).join('');

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
            item.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', e.target.dataset.id);
                e.target.classList.add('dragging');
            });

            item.addEventListener('dragend', (e) => {
                e.target.classList.remove('dragging');
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
        
        document.getElementById('availableDatasets').innerHTML = 
            '<p class="no-data">No search results yet. Enter a keyword to search for datasets.</p>';
        document.getElementById('downloadDatasets').innerHTML = 
            '<p class="no-data">Selected datasets will appear here.</p>';
        document.getElementById('searchInput').value = '';
        
        this.updateDownloadButton();
    }

    async handleDownload() {
        if (this.downloadDatasets.length === 0) {
            alert('Please select at least one dataset to download.');
            return;
        }

        try {
            // Extract descriptions (references) from selected datasets
            const descriptions = this.downloadDatasets.map(dataset => dataset.description);
            
            // Call the backend download endpoint
            const response = await fetch(`${CONFIG.BACKEND_URL}/download`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    descriptions: descriptions
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            alert(`Download initiated for ${result.count} dataset(s):\n\n${result.message}`);
            
        } catch (error) {
            console.error('Error downloading datasets:', error);
            alert('Error downloading datasets. Please try again.');
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
    console.log('Dataset Search & Download Manager initialized');
    
    // Add a welcome message
    setTimeout(() => {
        const searchInput = document.getElementById('searchInput');
        searchInput.placeholder = 'Try searching for "iris", "titanic", "housing", or "covid"...';
    }, 1000);
});
