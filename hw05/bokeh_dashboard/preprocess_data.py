#!/usr/bin/env python3
"""
Preprocess NYC 311 data for Bokeh dashboard.
Calculate monthly average response times by zipcode.
"""

import csv
from datetime import datetime
import json

def main():
    input_file = 'nyc_311_2024.csv'
    output_file = 'preprocessed_data.json'
    
    zipcode_data = {}
    overall_data = {}
    
    valid = 0
    skipped = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        for row in reader:
            if len(row) < 23:
                skipped += 1
                continue
            
            # get data from columns
            closed_str = row[1].strip()
            zipcode = row[8].strip()
            status = row[19].strip()
            created_str = row[22].strip()
            
            # skip if missing zipcode or not closed
            if not zipcode or len(zipcode) < 5:
                skipped += 1
                continue
            
            if not closed_str or status == 'In Progress':
                skipped += 1
                continue
            
            if not created_str:
                skipped += 1
                continue
            
            # parse dates
            created = None
            for fmt in ['%m/%d/%Y %I:%M:%S %p', '%m/%d/%Y %H:%M:%S', '%m/%d/%Y']:
                try:
                    created = datetime.strptime(created_str, fmt)
                    break
                except:
                    continue
            
            if not created or created.year != 2024:
                skipped += 1
                continue
            
            closed = None
            for fmt in ['%m/%d/%Y %I:%M:%S %p', '%m/%d/%Y %H:%M:%S', '%m/%d/%Y']:
                try:
                    closed = datetime.strptime(closed_str, fmt)
                    break
                except:
                    continue
            
            if not closed:
                skipped += 1
                continue
            
            # calculate hours
            diff = closed - created
            hours = diff.total_seconds() / 3600
            
            if hours < 0:
                skipped += 1
                continue
            
            # group by month closed
            month = f"{closed.year}-{closed.month:02d}"
            
            # store data
            if zipcode not in zipcode_data:
                zipcode_data[zipcode] = {}
            if month not in zipcode_data[zipcode]:
                zipcode_data[zipcode][month] = []
            zipcode_data[zipcode][month].append(hours)
            
            if month not in overall_data:
                overall_data[month] = []
            overall_data[month].append(hours)
            
            valid += 1
    
    print(f"Processed {valid} valid rows, skipped {skipped}")
    
    if valid == 0:
        print("No valid data found")
        return
    
    # calculate averages
    results = {
        'overall': {},
        'by_zipcode': {}
    }
    
    for month in overall_data:
        times = overall_data[month]
        results['overall'][month] = sum(times) / len(times)
    
    for zipcode in zipcode_data:
        results['by_zipcode'][zipcode] = {}
        for month in zipcode_data[zipcode]:
            times = zipcode_data[zipcode][month]
            results['by_zipcode'][zipcode][month] = sum(times) / len(times)
    
    # save
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Saved to {output_file}")

if __name__ == '__main__':
    main()
