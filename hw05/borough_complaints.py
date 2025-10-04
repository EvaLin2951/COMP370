#!/usr/bin/env python3
"""
Command-line tool to analyze NYC 311 complaints by borough and complaint type.
"""

import argparse
import csv
import sys
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(
        description='Analyze NYC 311 complaints by borough and type for a given date range.'
    )
    
    parser.add_argument('-i', '--input', required=True, 
                       help='Input CSV file')
    parser.add_argument('-s', '--start', required=True,
                       help='Start date (MM/DD/YYYY)')
    parser.add_argument('-e', '--end', required=True,
                       help='End date (MM/DD/YYYY)')
    parser.add_argument('-o', '--output',
                       help='Output file (optional)')
    
    args = parser.parse_args()
    
    try:
        start = datetime.strptime(args.start, '%m/%d/%Y')
        end = datetime.strptime(args.end, '%m/%d/%Y')
    except:
        print("Error: dates must be in MM/DD/YYYY format", file=sys.stderr)
        sys.exit(1)
    
    if start > end:
        print("Error: start date must be before end date", file=sys.stderr)
        sys.exit(1)
    
    counts = {}
    total_rows = 0
    valid_rows = 0
    
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            # Check if first row is header
            first_row = next(reader)
            if 'Created Date' not in first_row[0]:
                # No header, process first row as data
                f.seek(0)
                reader = csv.reader(f)
            
            for row in reader:
                total_rows += 1
                
                if len(row) < 26:
                    continue
                
                date_str = row[22].strip()  # Created Date is column 22
                complaint = row[5].strip()   # Complaint Type is column 5
                borough = row[25].strip()    # Borough is column 25
                
                if not date_str or not complaint or not borough:
                    continue
                
                try:
                    # Parse date: "08/08/2024 10:12:36 AM"
                    date = datetime.strptime(date_str.split()[0], '%m/%d/%Y')
                except:
                    continue
                
                # Check if in range
                if date < start or date > end:
                    continue
                
                # Count it
                key = (complaint, borough)
                if key in counts:
                    counts[key] += 1
                else:
                    counts[key] = 1
                
                valid_rows += 1
                    
    except FileNotFoundError:
        print(f"Error: file {args.input} not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    print(f"DEBUG: Total rows processed: {total_rows}", file=sys.stderr)
    print(f"DEBUG: Valid entries in date range: {valid_rows}", file=sys.stderr)
    
    # Sort and output
    sorted_results = sorted(counts.items())
    
    if args.output:
        out_file = open(args.output, 'w', newline='')
    else:
        out_file = sys.stdout
    
    writer = csv.writer(out_file)
    writer.writerow(['complaint type', 'borough', 'count'])
    
    for (complaint, borough), count in sorted_results:
        writer.writerow([complaint, borough, count])
    
    if args.output:
        out_file.close()

if __name__ == '__main__':
    main()
