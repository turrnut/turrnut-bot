import json
import random
import os

def pathify(path):
	return path.replace('|', os.sep)

games = {}
earnings = {}

earnings_file = pathify("blackjack|earnings.json")
filename = pathify("blackjack|games.json")

if os.path.exists(filename):
    with open(filename, "r") as f:
        try:
            games = json.load(f)
        except json.JSONDecodeError:
            games = {}

if os.path.exists(earnings_file):
    with open(earnings_file, "r") as f:
        try:
            earnings = json.load(f)
        except json.JSONDecodeError:
            earnings = {}

def save_games():
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump({str(k): v for k, v in games.items()}, f)

def save_earnings():
    with open(earnings_file, "w") as f:
        json.dump({str(k): v for k, v in earnings.items()}, f)

def pathify(path):
	return path.replace('|', os.sep)


def update_earnings(userid: str, amount: float):
    global earnings

    userid = str(userid)

    if userid not in earnings:
        earnings[userid] = 0.0

    earnings[userid] += amount
    save_earnings()

def bj(userid: str, wager: int):
    global games
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                games = json.load(f)
            except json.JSONDecodeError:
                games = {}

    if str(userid) in games:
        player, computer, wagered = games[str(userid)]
        return {
            "status": "exists",
            "message": "*Game already in progress*",
            "player": player,
            "computer": computer,
            "wager": wagered,
        }

    player = random.randint(2, 21)
    computer = random.randint(2, 21)

    games[userid] = [player, computer, wager]
    save_games()

    return {
        "status": "ok",
        "message": "*New Game!*",
        "player": player,
        "computer": computer,
        "wager": wager,
    }


def bjhit(userid: str):
    global games

    if str(userid) not in games:
        return {"status": "error"}

    games[str(userid)][0] += random.randint(1, 11)
    player_score = games[str(userid)][0]
    computer_score = games[str(userid)][1]
    wager = games[str(userid)][2]

    if player_score > 21:
        del games[str(userid)]
        save_games()
        update_earnings(str(userid), float(-wager))
        return {
            "status": "bust",
            "player": player_score,
            "computer": computer_score,
            "wager": wager,
        }

    # elif player_score == 21:
    #     return {
    #         "status": "blackjack",
    #         "player": player_score,
    #         "computer": computer_score,
    #         "wager": wager,
    #     }

    else:
        save_games()
        return {
            "status": "continue",
            "player": player_score,
            "computer": computer_score,
            "wager": wager,
        }



def bjstand(userid: str):
    global games

    if userid not in games:
        return {"status": "error"}

    player_score, computer_score, wager = games[userid]

    # Computer draws until >= 17
    while computer_score < 17:
        computer_score += random.randint(1, 11)

    outcome = None
    if computer_score > 21 or player_score > computer_score:
        update_earnings(str(userid), float(wager))
        outcome = "win"
    elif player_score < computer_score:
        update_earnings(str(userid), float(-wager))
        outcome = "lose"
    elif player_score == computer_score:
        games[userid] = [random.randint(2, 21), random.randint(2, 21), wager]
        save_games()
        return {
            "status": "tie",
            "message": "New round started with same wager",
            "player": games[userid][0],
            "computer": games[userid][1],
            "wager": wager,
        }

    del games[userid]
    save_games()

    return {
        "status": outcome,
        "player": player_score,
        "computer": computer_score,
        "wager": wager,
    }
