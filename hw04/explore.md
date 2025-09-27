# Dataset Exploration

## How big is the dataset?
Command: `wc -l clean_dialog.csv`
Result: 36860 lines

## What's the structure of the data?
Command: `head -n 5 clean_dialog.csv`
Fields: title, writer, pony, dialog
The data contains episode transcripts with 4 columns showing episode title, writer, character name, and their dialog.

## How many episodes does it cover?
Command: `csvtool -t COMMA col 1 clean_dialog.csv | tail -n +2 | sort | uniq | wc -l`
Result: 197 episodes

## Unexpected aspect of the dataset
Command: `grep "\[" clean_dialog.csv | head -3`
Issue Found: The dialog field contains stage directions and sound effects in square brackets (e.g., [sigh], [grunts], [gasp]) mixed with actual spoken text. This could create issues for dialog analysis as these are not actual spoken words but rather descriptions of how lines are delivered or actions that occur.
