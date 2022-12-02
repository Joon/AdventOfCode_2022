import pandas as pd

df = pd.read_csv('day2_input.txt', sep=" ")

def score_val(option):
    move_score_map = {
        'X': 1, 'Y': 2, 'Z': 3
    }
    return move_score_map[option[0]]

def score_win(option):
    # A for Rock, B for Paper, and C for Scissors
    # X for Rock, Y for Paper, and Z for Scissors
    # outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won)
    value_map = {
        "A_X": 3, "A_Y": 6, "A_Z": 0,
        "B_X": 0, "B_Y": 3, "B_Z": 6,
        "C_X": 6, "C_Y": 0, "C_Z": 3
    }    
    
    return value_map["{}_{}".format(option[0], option[1])]

def required_move(option):
    # X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win
    # X for Rock, Y for Paper, and Z for Scissors
    required_move_map = {
        # A for Rock
        "A_X": "Z", "A_Y": "X", "A_Z": "Y",
        # B for Paper
        "B_X": "X", "B_Y": "Y", "B_Z": "Z",
        # C for Scissors
        "C_X": "Y", "C_Y": "Z", "C_Z": "X"
    }    
    
    return required_move_map["{}_{}".format(option[0], option[1])]

def required_score(option):
    # X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win
    required_score_map = {'X': 0, 'Y': 3, 'Z': 6}
    return required_score_map[option[1]]

df['value_score'] = df['You'].apply(score_val)
df['outcome_score'] = df.apply(score_win, axis=1)
df['required_outcome_score'] = df.apply(required_score, axis=1)
df['required_move'] = df.apply(required_move, axis=1)
df['required_move_score'] = df['required_move'].apply(score_val)

df['score'] = df['value_score'] + df['outcome_score']
df['required_score'] = df['required_move_score'] + df['required_outcome_score']

print("Question 1: {}".format(df['score'].sum()))
print("Question 2: {}".format(df['required_score'].sum()))