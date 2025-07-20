import pandas as pd

# Read the Excel file
df = pd.read_excel('Stock Screener.xlsx')

print("Excel File Analysis")
print("=" * 50)
print(f"File shape: {df.shape}")
print(f"Number of rows: {len(df)}")
print(f"Number of columns: {len(df.columns)}")
print()

print("Column Headers (A1 to AE1):")
print("-" * 30)
for i, col in enumerate(df.columns):
    print(f"Column {i+1} ({chr(65+i)}): {col}")

print()
print("First few rows of data:")
print("-" * 30)
print(df.head())

print()
print("Data types:")
print("-" * 30)
print(df.dtypes)

print()
print("Sample data from first few rows:")
print("-" * 30)
for i, row in df.head(3).iterrows():
    print(f"Row {i+1}:")
    for j, (col, val) in enumerate(row.items()):
        print(f"  {chr(65+j)}: {val}")
    print() 