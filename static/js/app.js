// Global variables
let currentData = [];
let currentHeaders = [];
let currentPage = 1;
let itemsPerPage = 50;
let currentSortColumn = '';
let currentSortDirection = 'asc';
let filteredData = [];

// DOM elements
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const uploadSection = document.getElementById('uploadSection');
const dataSection = document.getElementById('dataSection');
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const errorMessage = document.getElementById('errorMessage');
const searchInput = document.getElementById('searchInput');
const tableHeader = document.getElementById('tableHeader');
const tableBody = document.getElementById('tableBody');
const prevPageBtn = document.getElementById('prevPage');
const nextPageBtn = document.getElementById('nextPage');
const pageInfo = document.getElementById('pageInfo');

// Event listeners
fileInput.addEventListener('change', handleFileUpload);
uploadArea.addEventListener('dragover', handleDragOver);
uploadArea.addEventListener('dragleave', handleDragLeave);
uploadArea.addEventListener('drop', handleDrop);
searchInput.addEventListener('input', handleSearch);

// File upload handling
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        uploadFile(file);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        uploadFile(files[0]);
    }
}

function uploadFile(file) {
    if (!file.name.endsWith('.xlsx')) {
        showError('Please upload an Excel (.xlsx) file');
        return;
    }

    showLoading();
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        hideLoading();
        if (data.success) {
            currentData = data.preview;
            currentHeaders = data.headers;
            filteredData = [...currentData];
            displayData();
            showDataSection();
        } else {
            showError(data.error || 'Failed to upload file');
        }
    })
    .catch(err => {
        hideLoading();
        console.error('Upload error:', err);
        showError('Error uploading file: ' + err.message);
    });
}

// Data display functions
function displayData() {
    displayHeaders();
    displayTableData();
    updatePagination();
}

function displayHeaders() {
    tableHeader.innerHTML = '';
    const headerRow = document.createElement('tr');
    
    currentHeaders.forEach((header, index) => {
        const th = document.createElement('th');
        th.textContent = header;
        th.className = 'sortable';
        th.onclick = () => sortByColumn(index);
        
        // Add sort indicators
        if (currentSortColumn === index) {
            th.classList.add(currentSortDirection === 'asc' ? 'sort-asc' : 'sort-desc');
        }
        
        headerRow.appendChild(th);
    });
    
    tableHeader.appendChild(headerRow);
}

function displayTableData() {
    tableBody.innerHTML = '';
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageData = filteredData.slice(startIndex, endIndex);
    
    pageData.forEach(row => {
        const tr = document.createElement('tr');
        
        currentHeaders.forEach(header => {
            const td = document.createElement('td');
            const value = row[header];
            
            // Format the cell content
            td.innerHTML = formatCellValue(value, header);
            
            // Add classes for styling
            if (isNumeric(value)) {
                td.classList.add('number-cell');
                if (header.includes('%') || header.includes('Change')) {
                    if (value > 0) td.classList.add('positive');
                    if (value < 0) td.classList.add('negative');
                }
            }
            
            tr.appendChild(td);
        });
        
        tableBody.appendChild(tr);
    });
}

function formatCellValue(value, header) {
    if (value === null || value === undefined || value === '') {
        return '<span style="color: #ccc;">-</span>';
    }
    
    // Format percentages
    if (header.includes('%') && isNumeric(value)) {
        return `<span class="percentage">${value > 0 ? '+' : ''}${value.toFixed(2)}%</span>`;
    }
    
    // Format currency/market cap
    if (header.includes('USD') || header.includes('Cap') || header.includes('Revenue') || header.includes('Income')) {
        if (isNumeric(value) && value >= 1000000) {
            return formatCurrency(value);
        }
    }
    
    // Format ratios
    if (header.includes('P/E') || header.includes('P/S') || header.includes('P/B') || header.includes('P/CFO')) {
        if (isNumeric(value)) {
            return value.toFixed(2);
        }
    }
    
    // Truncate long text
    if (typeof value === 'string' && value.length > 20) {
        return `<div class="cell-content" data-full="${value}">${value.substring(0, 20)}...</div>`;
    }
    
    return value;
}

function formatCurrency(value) {
    if (value >= 1e12) {
        return `$${(value / 1e12).toFixed(2)}T`;
    } else if (value >= 1e9) {
        return `$${(value / 1e9).toFixed(2)}B`;
    } else if (value >= 1e6) {
        return `$${(value / 1e6).toFixed(2)}M`;
    } else {
        return `$${value.toLocaleString()}`;
    }
}

function isNumeric(value) {
    return !isNaN(value) && value !== null && value !== undefined && value !== '';
}

// Sorting functionality
function sortByColumn(columnIndex) {
    const header = currentHeaders[columnIndex];
    
    if (currentSortColumn === columnIndex) {
        currentSortDirection = currentSortDirection === 'asc' ? 'desc' : 'asc';
    } else {
        currentSortColumn = columnIndex;
        currentSortDirection = 'asc';
    }
    
    // Sort the data
    filteredData.sort((a, b) => {
        let aVal = a[header];
        let bVal = b[header];
        
        // Handle null/undefined values
        if (aVal === null || aVal === undefined || aVal === '') aVal = '';
        if (bVal === null || bVal === undefined || bVal === '') bVal = '';
        
        // Convert to numbers if possible
        const aNum = parseFloat(aVal);
        const bNum = parseFloat(bVal);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return currentSortDirection === 'asc' ? aNum - bNum : bNum - aNum;
        }
        
        // String comparison
        const aStr = String(aVal).toLowerCase();
        const bStr = String(bVal).toLowerCase();
        
        if (currentSortDirection === 'asc') {
            return aStr.localeCompare(bStr);
        } else {
            return bStr.localeCompare(aStr);
        }
    });
    
    currentPage = 1; // Reset to first page
    displayData();
}

// Search functionality
function handleSearch() {
    const searchTerm = searchInput.value.toLowerCase();
    
    if (searchTerm === '') {
        filteredData = [...currentData];
    } else {
        filteredData = currentData.filter(row => {
            return currentHeaders.some(header => {
                const value = row[header];
                if (value === null || value === undefined) return false;
                return String(value).toLowerCase().includes(searchTerm);
            });
        });
    }
    
    currentPage = 1; // Reset to first page
    displayTableData();
    updatePagination();
}

// Pagination functions
function changePage(direction) {
    const newPage = currentPage + direction;
    const maxPage = Math.ceil(filteredData.length / itemsPerPage);
    
    if (newPage >= 1 && newPage <= maxPage) {
        currentPage = newPage;
        displayTableData();
        updatePagination();
    }
}

function updatePagination() {
    const maxPage = Math.ceil(filteredData.length / itemsPerPage);
    
    prevPageBtn.disabled = currentPage <= 1;
    nextPageBtn.disabled = currentPage >= maxPage;
    
    pageInfo.textContent = `Page ${currentPage} of ${maxPage} (${filteredData.length} total items)`;
}

// Export functionality
function exportData() {
    if (filteredData.length === 0) {
        alert('No data to export');
        return;
    }
    
    // Create CSV content
    const headers = currentHeaders.join(',');
    const rows = filteredData.map(row => 
        currentHeaders.map(header => {
            const value = row[header];
            // Escape commas and quotes in CSV
            if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
                return `"${value.replace(/"/g, '""')}"`;
            }
            return value || '';
        }).join(',')
    );
    
    const csvContent = [headers, ...rows].join('\n');
    
    // Create and download file
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'stock_screener_data.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// UI state functions
function showLoading() {
    loading.style.display = 'block';
    uploadSection.style.display = 'none';
    dataSection.style.display = 'none';
    error.style.display = 'none';
}

function hideLoading() {
    loading.style.display = 'none';
}

function showDataSection() {
    uploadSection.style.display = 'none';
    dataSection.style.display = 'block';
    error.style.display = 'none';
}

function showError(message) {
    errorMessage.textContent = message;
    error.style.display = 'block';
    loading.style.display = 'none';
    uploadSection.style.display = 'block';
    dataSection.style.display = 'none';
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Set up drag and drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        document.body.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    // Ensure horizontal scrollbar is always visible
    const tableContainer = document.querySelector('.table-container');
    if (tableContainer) {
        // Force horizontal scrollbar to be visible
        tableContainer.style.overflowX = 'scroll';
        
        // Add keyboard navigation for horizontal scrolling
        document.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
                const scrollAmount = 200;
                if (e.key === 'ArrowLeft') {
                    tableContainer.scrollLeft -= scrollAmount;
                } else {
                    tableContainer.scrollLeft += scrollAmount;
                }
                e.preventDefault();
            }
        });
    }
}); 