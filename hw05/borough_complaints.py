#!/usr/bin/env python3
"""
Command-line tool to analyze NYC 311 complaints by borough and complaint type.
"""

import argparse
import csv
import sys
from datetime import datetime

def main():
    # setup argparse
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
    
    # parse the dates
    try:
        start = datetime.strptime(args.start, '%m/%d/%Y')
        end = datetime.strptime(args.end, '%m/%d/%Y')
    except:
        print("Error: dates must be in MM/DD/YYYY format")
        sys.exit(1)
    
    if start > end:
        print("Error: start date must be before end date")
        sys.exit(1)
    
    # read the csv and count complaints
    counts = {}
    
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # get the date
                date_str = row.get('Created Date', '')
                if not date_str:
                    continue
                
                try:
                    date = datetime.strptime(date_str.split()[0], '%m/%d/%Y')
                except:
                    continue
                
                # check if in range
                if date < start or date > end:
                    continue
                
                # get complaint type and borough
                complaint = row.get('Complaint Type', '').strip()
                borough = row.get('Borough', '').strip()
                
                if not complaint or not borough:
                    continue
                
                # count it
                key = (complaint, borough)
                if key in counts:
                    counts[key] += 1
                else:
                    counts[key] = 1
                    
    except FileNotFoundError:
        print(f"Error: file {args.input} not found")
        sys.exit(1)
    
    # sort the results
    sorted_results = sorted(counts.items())
    
    # output results
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
