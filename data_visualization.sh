#!/bin/bash

for file in *.csv; do
python Data_visualization.py $file
done