#!/usr/bin/env python3
"""
Bokeh dashboard for NYC 311 response time analysis by zipcode.
"""

import json
from datetime import datetime
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import Select
from bokeh.plotting import figure

# load the data
with open('preprocessed_data.json', 'r') as f:
    data = json.load(f)

# get zipcodes list
zipcodes = sorted(data['by_zipcode'].keys())

# get all months
all_months = sorted(set(data['overall'].keys()))
dates = [datetime.strptime(m, '%Y-%m') for m in all_months]

# setup the plot
p = figure(
    x_axis_type='datetime',
    title='Monthly Average Response Time by Zipcode',
    width=800,
    height=400
)

p.xaxis.axis_label = 'Month'
p.yaxis.axis_label = 'Average Response Time (hours)'

# get initial data
zip1 = zipcodes[0] if zipcodes else '10001'
zip2 = zipcodes[1] if len(zipcodes) > 1 else '10002'

# overall data
overall_vals = []
for m in all_months:
    if m in data['overall']:
        overall_vals.append(data['overall'][m])
    else:
        overall_vals.append(None)

# zipcode 1 data
zip1_vals = []
for m in all_months:
    if zip1 in data['by_zipcode'] and m in data['by_zipcode'][zip1]:
        zip1_vals.append(data['by_zipcode'][zip1][m])
    else:
        zip1_vals.append(None)

# zipcode 2 data
zip2_vals = []
for m in all_months:
    if zip2 in data['by_zipcode'] and m in data['by_zipcode'][zip2]:
        zip2_vals.append(data['by_zipcode'][zip2][m])
    else:
        zip2_vals.append(None)

# draw the lines
line1 = p.line(dates, overall_vals, legend_label='Overall (All Zipcodes)',
               line_width=2, color='navy')
line2 = p.line(dates, zip1_vals, legend_label=f'Zipcode {zip1}',
               line_width=2, color='red')
line3 = p.line(dates, zip2_vals, legend_label=f'Zipcode {zip2}',
               line_width=2, color='green')

p.legend.location = 'top_left'
p.legend.click_policy = 'hide'

# create dropdowns
dropdown1 = Select(title='Zipcode 1:', value=zip1, options=zipcodes, width=200)
dropdown2 = Select(title='Zipcode 2:', value=zip2, options=zipcodes, width=200)

# update function
def update(attr, old, new):
    # get selected zipcodes
    z1 = dropdown1.value
    z2 = dropdown2.value
    
    # get new data for zipcode 1
    new_zip1_vals = []
    for m in all_months:
        if z1 in data['by_zipcode'] and m in data['by_zipcode'][z1]:
            new_zip1_vals.append(data['by_zipcode'][z1][m])
        else:
            new_zip1_vals.append(None)
    
    # get new data for zipcode 2
    new_zip2_vals = []
    for m in all_months:
        if z2 in data['by_zipcode'] and m in data['by_zipcode'][z2]:
            new_zip2_vals.append(data['by_zipcode'][z2][m])
        else:
            new_zip2_vals.append(None)
    
    # update the lines
    line2.data_source.data = {'x': dates, 'y': new_zip1_vals}
    line3.data_source.data = {'x': dates, 'y': new_zip2_vals}
    
    # update legend
    p.legend.items[1].label.value = f'Zipcode {z1}'
    p.legend.items[2].label.value = f'Zipcode {z2}'

# connect dropdowns to update function
dropdown1.on_change('value', update)
dropdown2.on_change('value', update)

# put everything together
layout = column(dropdown1, dropdown2, p)

# add to document
curdoc().add_root(layout)
curdoc().title = "NYC 311 Response Time Dashboard"
