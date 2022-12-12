ACTION_MAP = {
    'A': 0,  # rock
    'B': 1,  # paper
    'C': 2,  # scissors
    'X': 0,  # rock
    'Y': 1,  # paper
    'Z': 2,  # scissors
}

ACTION_TRANSITIONS = {
    'A': (2, 0, 1), # 0 rock
    'B': (0, 1, 2), # 1 paper
    'C': (1, 2, 0), # 2 scissors
}

def get_strategy_guide(filename):
    strategy_guide = []
    with open(filename, 'r') as f:
        for line in f:
            opponent, response = line.strip().split(' ')
            strategy_guide.append((opponent, response))
    return strategy_guide

def get_round_score(opponent_action, response_action):
    outcome = (opponent_action - response_action) % 3
    # draw
    if outcome == 0:
        outcome_bonus = 3
    # loss
    elif outcome == 1:
        outcome_bonus = 0
    # win
    elif outcome == 2:
        outcome_bonus = 6
    else:
        raise ValueError('what on earth has happened here?')

    return outcome_bonus + response_action + 1

def score_rounds_part_1(strategy_guide):
    return [
        get_round_score(ACTION_MAP[opponent], ACTION_MAP[response])
        for opponent, response in strategy_guide
    ]

def score_rounds_part_2(strategy_guide):
    scores = []
    for opponent, required_outcome in strategy_guide:
        required_outcome_idx = ACTION_MAP[required_outcome]
        response_action = ACTION_TRANSITIONS[opponent][required_outcome_idx]
        round_score = get_round_score(ACTION_MAP[opponent], response_action)
        scores.append(round_score)

    return scores

def main():
    strategy_guide = get_strategy_guide('input.txt')

    print('Part 1')
    scores = score_rounds_part_1(strategy_guide)
    print('Total score according to the the `plan`', sum(scores))

    print('Part 2')
    scores = score_rounds_part_2(strategy_guide)
    print('Total score according to the the `plan`', sum(scores))


if __name__=='__main__':
    main()
