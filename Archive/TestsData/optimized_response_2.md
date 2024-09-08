# Optimized Response

Here's an example Python script that reads data from an input CSV file, filters out rows with a specific value in a particular column, calculates the average of another column, and writes the processed data to an output CSV file:

```python
import csv

input_file = 'input.csv'
output_file = 'output.csv'

try:
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]

    filtered_data = [row for row in data if row['column_name'] != 'filter_value']

    total = sum(float(row['numeric_column']) for row in filtered_data)
    average = total / len(filtered_data)

    for row in filtered_data:
        row['average_column'] = average

    fieldnames = reader.fieldnames + ['average_column']

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_data)

    print('Data processed successfully and written to', output_file)

except FileNotFoundError:
    print('File not found. Please make sure the input file exists.')

except PermissionError:
    print('Permission error. Please make sure you have the necessary permissions to read and write files.')

except Exception as e:
    print('An error occurred:', e)
```

Replace `'input.csv'`, `'column_name'`, `'filter_value'`, and `'numeric_column'` with appropriate values for your input data. Make sure to adjust the processing logic and fieldnames as needed for your specific use case.

To run this script, save it to a Python file (e.g., `data_processing.py`) and run it using `python data_processing.py` in the command line, making sure the input CSV file is in the same directory as the script.