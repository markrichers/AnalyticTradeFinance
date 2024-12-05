import csv
from collections import defaultdict
from datetime import datetime
import os

def process_bank_statement(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        csv_reader = csv.DictReader(infile, delimiter=';')
        fieldnames = csv_reader.fieldnames

        csv_writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        csv_writer.writeheader()

        for row in csv_reader:
            csv_writer.writerow(row)

    print(f"File created: {output_file}")

input_file = 'bank_07-10-2023_18-08-2024.csv'
output_prefix = 'bank_statement'

if __name__ == "__main__":
    # Absolute file path to your bank statement CSV file
    input_file = r'C:\Users\b8nguym23i\OneDrive - KUKA AG\Desktop\Python + SQL\Python New Handmade\Income Analytic\NL16INGB0795288085_18-09-2023_08-11-2024.csv'
    
    # Output CSV file path
    output_file = r'C:\Users\b8nguym23i\OneDrive - KUKA AG\Desktop\Python + SQL\Python New Handmade\Income Analytic\bank_statement.csv'
    
    # Process the bank statement
    process_bank_statement(input_file, output_file)