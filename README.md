# Interactive Excel Stock Screener Viewer

A modern web application for viewing and sorting stock screener data from Excel files. Built with Flask, Pandas, and a responsive HTML/CSS/JavaScript frontend.

## Features

- **Interactive Excel File Upload**: Upload and view Excel (.xlsx) files
- **Dynamic Sorting**: Sort by any column in ascending or descending order
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Pagination**: Handle large datasets efficiently
- **Real-time Search**: Filter data as you type
- **Export Options**: Download sorted data as CSV
- **Modern UI**: Clean, professional interface with dark/light theme support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/excel-stock-viewer.git
cd excel-stock-viewer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python excel_viewer.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. **Upload Excel File**: Click "Choose File" and select your Excel (.xlsx) file
2. **View Data**: The application will display your data in a sortable table
3. **Sort Data**: Click on any column header to sort by that column
4. **Search**: Use the search box to filter data
5. **Navigate**: Use pagination controls to browse through large datasets
6. **Export**: Download the current view as a CSV file

## Project Structure

```
excel-stock-viewer/
├── excel_viewer.py          # Main Flask application
├── templates/               # HTML templates
│   └── index.html          # Main interface
├── static/                  # CSS, JS, and other static files
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   └── js/
│       └── app.js          # Frontend JavaScript
├── requirements.txt         # Python dependencies
├── README.md              # This file
└── .gitignore             # Git ignore file
```

## Dependencies

- Flask: Web framework
- Pandas: Data manipulation and Excel reading
- Werkzeug: File upload handling

## License

MIT License - feel free to use this project for your own needs.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

If you encounter any issues or have questions, please open an issue on GitHub. 