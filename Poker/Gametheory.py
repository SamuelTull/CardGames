import operator as op
from functools import reduce

# Player 1 has one of [1,2,3,4,5]
# Player 2 has one of [1,2,3,4,5]
C1 = [1, 2, 3, 4, 5]
C2 = [1, 2, 3, 4, 5]
P = [[0 if i == j else 1 / (5 * 4) for i in range(5)] for j in range(5)]

# Player 1 Folds/Bets
# if bet Player 2 folds/Calls

# S1 = ["P_bet" for each hand]
# S2 = ["P_call" for each hand]
S1 = [1.0, 01.0, 01.0, 01.0, 1.0]
S2 = [01.0, 01.0, 01.0, 01.0, 01.0]
# U1 = payoff for P1 = [fold,bet-call(win/lose),bet-fold]
# U2 = payoff for P2 = [fold,bet-call(win/lose),bet-fold]
U1 = [-2, (5, -5), 0]
U2 = [2, (5, -5), 0]


def ncr(n, r):
    r = min(r, n - r)
    numer = reduce(op.mul, range(n, n - r, -1), 1)
    denom = reduce(op.mul, range(1, r + 1), 1)
    return numer // denom  # or / in Python 2


def inv(p):
    assert 0 <= p <= 1
    return 1 - p


def win(x, y, u):
    assert x != y
    if x > y:
        return u[0]
    if y > x:
        return u[1]


def get_payoff_p1(C1, C2, P, S1, S2, U2):
    EV = 0
    for j in range(len(C2)):
        for i in range(len(C1)):
            p = P[i][j]
            if p > 0:
                # proba fold
                EV += p * inv(S1[i]) * U1[0]
                # call - bet
                EV += p * S1[i] * S2[j] * win(C1[i], C2[j], U1[1])
                # call- fold
                EV += p * S1[i] * inv(S2[j]) * U1[2]
    return EV


def get_payoff_p1_fixed(i, C1, C2, P, S1, S2, U2):
    EV = 0
    for j in range(len(C2)):
        p = P[i][j]
        if p > 0:
            # proba fold
            EV += p * inv(S1[i]) * U1[0]
            # call - bet
            EV += p * S1[i] * S2[j] * win(C1[i], C2[j], U1[1])
            # call- fold
            EV += p * S1[i] * inv(S2[j]) * U1[2]
    return EV


def get_payoff_p2(C1, C2, P, S1, S2, U2):
    EV = 0
    for i in range(len(C1)):
        for j in range(len(C2)):
            p = P[i][j]
            if p > 0:
                # proba fold
                EV += p * inv(S1[i]) * U2[0]
                # call - bet
                EV += p * S1[i] * S2[j] * win(C2[j], C1[i], U2[1])
                # call- fold
                EV += p * S1[i] * inv(S2[j]) * U2[2]
    return EV


def get_payoff_p2_fixed(j, C1, C2, P, S1, S2, U2):
    EV = 0
    for i in range(len(C1)):
        p = P[i][j]
        if p > 0:
            # proba fold
            EV += p * inv(S1[i]) * U2[0]
            # call - bet
            EV += p * S1[i] * S2[j] * win(C2[j], C1[i], U2[1])
            # call- fold
            EV += p * S1[i] * inv(S2[j]) * U2[2]
    return EV


def update_p1_strategy(C1, C2, P, S1, S2, U2, shift):
    # print("Updating S1")
    best = [x for x in S1]
    for i in range(len(C1)):
        curr_i = get_payoff_p1_fixed(i, C1, C2, P, S1, S2, U2)
        for s in [max(0, S1[i] - shift), min(1, S1[i] + shift)]:
            S1[i] = s
            new_i = get_payoff_p1_fixed(i, C1, C2, P, S1, S2, U2)
            if new_i > curr_i:
                curr_i = new_i
                best[i] = S1[i]
            S1[i] = best[i]
    return S1


def update_p2_strategy(C1, C2, P, S1, S2, U2, shift):
    # print("Updating S2")
    best = [x for x in S2]
    for j in range(len(C2)):
        curr_j = get_payoff_p2_fixed(j, C1, C2, P, S1, S2, U2)
        for s in [max(0, S2[j] - shift), min(1, S2[j] + shift)]:
            S2[j] = s
            new_j = get_payoff_p2_fixed(j, C1, C2, P, S1, S2, U2)
            if new_j > curr_j:
                curr_j = new_j
                best[j] = S2[j]
            S2[j] = best[j]
    return S2


"""for shift in [0.1, 0.01, 0.001]:
    for i in range(10):
        curr = get_payoff_p2(C1, C2, P, S1, S2, U2)
        S2 = update_p2_strategy(C1, C2, P, S1, S2, U2, shift)
        new = get_payoff_p2(C1, C2, P, S1, S2, U2)
        print(f"{i}, {shift} , Payoff {new} from {curr}")
        print(S2)
        if new == curr:
            break"""

"""for shift in [0.1, 0.01, 0.001]:
    for i in range(10):
        curr = get_payoff_p1(C1, C2, P, S1, S2, U2)
        S1 = update_p1_strategy(C1, C2, P, S1, S2, U2, shift)
        new = get_payoff_p1(C1, C2, P, S1, S2, U2)
        print(f"{i}, {shift} , Payoff {new} from {curr}")
        print(S1)
        if new == curr:
            break"""


for shift in [0.1, 0.01, 0.001]:
    for i in range(50000):
        curr_1 = get_payoff_p1(C1, C2, P, S1, S2, U2)
        curr_2 = get_payoff_p2(C1, C2, P, S1, S2, U2)
        S1 = update_p1_strategy(C1, C2, P, S1, S2, U2, shift)
        mid_1 = get_payoff_p1(C1, C2, P, S1, S2, U2)
        mid_2 = get_payoff_p2(C1, C2, P, S1, S2, U2)
        S2 = update_p2_strategy(C1, C2, P, S1, S2, U2, shift)
        new_1 = get_payoff_p1(C1, C2, P, S1, S2, U2)
        new_2 = get_payoff_p2(C1, C2, P, S1, S2, U2)
        print(
            f"{i}, {shift}, First {curr_1}, {curr_2}, Mid {mid_1}, {mid_2}, Now {new_1}, {new_2}"
        )
        print("S1:", S1)
        print("S2:", S2)
        print()
        if new_1 == curr_1:
            if new_2 == curr_2:
                break
