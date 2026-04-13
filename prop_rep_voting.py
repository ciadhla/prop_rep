import re, os
import random
import math
import argparse
import pandas as pd
from collections import defaultdict


def check_format(df):
    """Check that the dataframe is formatted correctly"""
    positions = set()
    names = set()
    col_name_regex = re.compile('(.*)\s\[(.*)\]')
    for col in df.columns:
        try:
            match = re.match(col_name_regex, col)
            position, name = match.groups()
            positions.add(position)
            names.add(name)
        except:
            continue

    if len(positions) == 0 or len(names) == 0:
        raise ValueError('The specified document is of the incorrect format. '
                         'Column headings must be of the form "Position [Name]".')


def make_candidate_dictionary():
    """Create dictionary of positions and candidates with empty counts"""
    counts = defaultdict(dict)
    col_name_regex = re.compile('(.*)\s\[(.*)\]')
    cols = votes.columns

    for column in cols:
        # Extract position & candidate name from column name using regex
        try:
            match = re.match(col_name_regex, column)
            position, name = match.groups()
        except:
            continue

        # Add to dictionary of candidates
        counts[position][name] = 0

    return counts


def count_votes(position):
    """Function to count votes according to proportional representation"""
    # Extract only the columns pertaining to the current position
    position_df = votes.filter(like=position + ' [', axis=1)
    round = 1
    round_results = []

    while True:
        # Count all first preference votes
        for index, row in position_df.iterrows():
            for candidate in counts[position]:
                if row[f'{position} [{candidate}]'] == 1:
                    counts[position][candidate] += 1
                    row[f'{position} [{candidate}]'] = 0   # set 1st pref to 0 so as not to count again in later rounds
                    break

        print(f'Round {round} results: {counts[position]}')

        # Store the results of each round in case of an intermediate tie
        round_results.append(counts[position].copy())

        # Check if the quota has been reached
        if max(counts[position].values()) >= quota:
            elected = max(counts[position], key=counts[position].get)
            results[position] = elected
            print(f'{elected} is elected as {position} after round {round}.')
            break


        # Check for a tie in minimum votes
        round_counts = list(counts[position].values())
        num_lowest_candidates = round_counts.count(min(round_counts))

        if num_lowest_candidates > 1:
            remaining_candidates = list(counts[position].keys())

            # Check if the tie is between the last remaining candidates - return tie if so
            if num_lowest_candidates == len(remaining_candidates):
                remaining = list(counts[position].keys())
                print(f'!!! Tie for {position} after round {round}. '
                      f'Remaining candidates: {remaining}')
                results[position] = f'Tie – {remaining}'
                break

            # Eliminate intermediate ties
            # Get tied lowest candidates
            min_votes = min(counts[position].values())
            tied_candidates = [
                candidate for candidate, current_votes in counts[position].items()
                if current_votes == min_votes
            ]

            # Check if either candidate had a lower number of votes in a previous round
            n = 2  # first check the previous round (index of -2 since starting from 0)
            while round - n >= 0:
                prev_results = {candidate: round_results[round-n][candidate] for candidate in tied_candidates}
                num_lowest_candidates = list(prev_results.values()).count(min(prev_results.values()))
                if num_lowest_candidates == 1:
                    min_candidate = min(prev_results, key=prev_results.get)
                    print(f'Tie - {min_candidate} is eliminated due to lower votes in the previous round.')
                    break
                n += 1  # go to previous round

            # If still tied across all previous rounds → random choice
            else:
                min_candidate = random.choice(tied_candidates)
                print(f'Tie - {min_candidate} is eliminated by random choice.')

        else:  # no tie
            min_candidate = min(counts[position], key=counts[position].get)
            print(f'{min_candidate} is eliminated.')

        # Eliminate the candidate with the fewest votes
        counts[position].pop(min_candidate)

        # Adjust DataFrame values: decrease all preference numbers after the eliminated candidate
        for index, row in position_df.iterrows():
            eliminated_pref = row[f'{position} [{min_candidate}]']
            for candidate in counts[position]:
                if row[f'{position} [{candidate}]'] > eliminated_pref:
                    position_df.at[index, f'{position} [{candidate}]'] -= 1

        round += 1


if __name__ == "__main__":

    # Sets global variables for functions, rather than passing arguments

    # Pass the votes file as an argument
    parser = argparse.ArgumentParser(
        description="Count votes according to a proportional representation system."
    )
    parser.add_argument("votes", help="Path to the csv file containing the votes")
    args = parser.parse_args()
    filename = args.votes

    # Verify the votes file exists and is a .csv
    if not filename.lower().endswith(".csv"):
        raise ValueError("The --votes file must be a CSV file.")

    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")

    # Load votes
    try:
        votes = pd.read_csv(filename)
    except Exception as e:
        raise ValueError(f"Failed to read CSV file: {e}")
    
    votes = pd.read_csv(filename)
    if 'Timestamp' in votes.columns:
        votes = votes.drop('Timestamp', axis=1)
    check_format(votes)

    # Calculate quota
    quota = math.floor(len(votes.index) / 2 + 1)
    print(f'Quota: {quota}')

    # Assemble candidate dictionary
    counts = make_candidate_dictionary()
    if len(counts) == 1:
        print(f'1 position up for vote: {", ".join(list(counts.keys()))}')
    else:
        print(f'{len(counts)} positions up for vote: {", ".join(list(counts.keys()))}')

    results = {}

    # Count votes
    for position in counts.keys():
        print(f'\nCounting {position}...')
        count_votes(position)

    # Print results
    print('\n\n***** Results *****')
    for position in results:
        print(f'{position}: {results[position]}')
