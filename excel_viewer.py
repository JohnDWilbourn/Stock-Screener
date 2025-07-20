from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global variable to store the current dataframe
current_df = None
current_filename = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global current_df, current_filename
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.endswith('.xlsx'):
        try:
            # Read the Excel file
            current_df = pd.read_excel(file)
            current_filename = secure_filename(file.filename)
            
            # Clean the data to handle special characters and NaN values
            current_df = current_df.fillna('')  # Replace NaN with empty string
            
            # Get column headers and clean them
            headers = [str(header).strip() for header in current_df.columns.tolist()]
            
            # Convert data to records with proper handling of special characters
            all_data = []
            for index, row in current_df.iterrows():
                row_dict = {}
                for header in headers:
                    value = row[header]
                    # Handle different data types and special characters
                    if pd.isna(value):
                        row_dict[header] = ''
                    elif isinstance(value, (int, float)):
                        row_dict[header] = value
                    else:
                        # Convert to string and clean special characters
                        row_dict[header] = str(value).strip()
                all_data.append(row_dict)
            
            return jsonify({
                'success': True,
                'filename': current_filename,
                'headers': headers,
                'preview': all_data,
                'total_rows': len(current_df)
            })
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            return jsonify({'error': f'Error reading file: {str(e)}', 'details': error_details}), 400
    else:
        return jsonify({'error': 'Please upload an Excel (.xlsx) file'}), 400

@app.route('/get_data')
def get_data():
    global current_df
    
    if current_df is None:
        return jsonify({'error': 'No file loaded'}), 400
    
    # Get sorting parameters
    sort_column = request.args.get('sort_column', '')
    sort_direction = request.args.get('sort_direction', 'asc')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    
    # Create a copy for sorting
    df_sorted = current_df.copy()
    
    # Apply sorting if specified
    if sort_column and sort_column in df_sorted.columns:
        df_sorted = df_sorted.sort_values(by=sort_column, ascending=(sort_direction == 'asc'))
    
    # Calculate pagination
    total_rows = len(df_sorted)
    total_pages = (total_rows + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    # Get the page data
    page_data = df_sorted.iloc[start_idx:end_idx].to_dict('records')
    
    return jsonify({
        'data': page_data,
        'total_rows': total_rows,
        'total_pages': total_pages,
        'current_page': page,
        'per_page': per_page,
        'headers': df_sorted.columns.tolist()
    })

@app.route('/get_all_data')
def get_all_data():
    global current_df
    
    if current_df is None:
        return jsonify({'error': 'No file loaded'}), 400
    
    # Get sorting parameters
    sort_column = request.args.get('sort_column', '')
    sort_direction = request.args.get('sort_direction', 'asc')
    
    # Create a copy for sorting
    df_sorted = current_df.copy()
    
    # Apply sorting if specified
    if sort_column and sort_column in df_sorted.columns:
        df_sorted = df_sorted.sort_values(by=sort_column, ascending=(sort_direction == 'asc'))
    
    return jsonify({
        'data': df_sorted.to_dict('records'),
        'headers': df_sorted.columns.tolist()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 