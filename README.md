# prop_rep

This is a counter for proportional representation systems involving one or more positions, each with a single winner. The original use case was for the committee elections for a university club.

The counter was created to work with Google Sheets. Each position must be entered as a single question with a multiple choice grid, as in [this](https://forms.gle/dLpdXYZnHMM6N1UaA) example form.

Open the form responses in Google Sheets and export them as a .csv file with the default settings. Ensure the .csv file is in the same folder as the python script.

## Usage

```bash
python prop_rep_voting.py votes.csv
```
