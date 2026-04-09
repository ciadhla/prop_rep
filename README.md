# prop_rep

This is a counter for proportional representation systems involving one or more positions, each with a single winner. The original use case was for the committee elections of a university club.

The counter was created to work with Google Sheets. Each position must be entered as a single question with a multiple choice grid, as in [this](https://forms.gle/dLpdXYZnHMM6N1UaA) example form. 

Open the form responses in Google Sheets and export them as a .csv file with the default settings. Ensure the .csv file is in the same folder as the python script. 

It is recommended to make a copy of the linked Google form rather than creating your own. If you are creating your own csv file, ensure the column headers are of the format "Position \[Candidate Name\]".

## Usage

```bash
python prop_rep_voting.py votes.csv
```

## GitHub Pages

This codebase can also be run directly [in the browser](https://ciadhla.github.io/prop_rep/). Here, you can upload the csv file without needing python installed on your device. Everything runs locally and no data leaves your device.
