# Copyright (c) 2025 TURRNUT
# Under the MIT license

import json
import random
import os
import discord

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
        json.dump({str(k): v for k, v in games.items()}, f, indent=4)

def save_earnings():
    with open(earnings_file, "w") as f:
        json.dump({str(k): v for k, v in earnings.items()}, f, indent=4)

def pathify(path):
	return path.replace('|', os.sep)


def update_earnings(userid: str, amount: float):
    global earnings

    userid = str(userid)

    if userid not in earnings:
        earnings[userid] = 0.0

    earnings[userid] += amount
    save_earnings()

def bj(userid: str, wager: int, gamecontinue: bool):
    global games
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                games = json.load(f)
            except json.JSONDecodeError:
                games = {}

    if str(userid) in games:
        if gamecontinue:
            wager = games[str(userid)][3]
        elif games[str(userid)][0] != 0: 
            player, computer_actual, computer_showing, wagered = games[str(userid)]
            return {
                "status": "exists",
                "message": "*Game already in progress*",
                "player": player,
                "computer_actual": computer_actual,
                "computer_showing": computer_showing,
                "wager": wagered,
            }
        
    # there are 4 cards in a deck worth 10, hence 13
    player_card1 = random.randint(1, 13)
    player_card2 = random.randint(1, 13)

    if player_card1 == 1:
        player_card1 = 11
    elif player_card1 > 9:
        player_card1 = 10

    if player_card2 == 1:
        if player_card1 < 11:
            player_card2 = 11
        else:
            player_card2 = 1
    elif player_card2 > 9:
        player_card2 = 10

    computer_card1 = random.randint(1, 13)
    computer_card2 = random.randint(1, 13)

    if computer_card1 == 1:
        computer_card1 = 11
    elif computer_card1 > 9:
        computer_card1 = 10

    if computer_card2 == 1:
        if computer_card1 < 11:
            computer_card2 = 11
        else:
            computer_card2 = 1
    elif computer_card2 > 9:
        computer_card2 = 10

    player = player_card1 + player_card2
    computer_actual = computer_card1 + computer_card2

    computer_showing = computer_card2

    print("computer drew a " + str(computer_card1) + " and a " + str(computer_card2))
    print(str(userid) + " drew a " + str(player_card1) + " and a " + str(player_card2))

    games[userid] = [player, computer_actual, computer_showing, wager]
    save_games()

    if player == 21:
        return {
            "status": "blackjack",
            "player": player,
            "computer_actual": computer_actual,
            "computer_showing": computer_showing,
            "wager": wager,
        }
    
    else:
        return {
            "status": "ok",
            "message": "*New Game!*",
            "player": player,
            "computer_actual": computer_actual,
            "computer_showing": computer_showing,
            "wager": wager,
        }


def bjhit(userid: str):
    global games

    if str(userid) not in games:
        return {"status": "error"}

    player_card = random.randint(1, 13)

    if player_card == 1:
        if games[str(userid)][0] < 11:
            player_card = 11
        else:
            player_card = 1
    elif player_card > 9:
        player_card = 10

    games[str(userid)][0] += player_card
    player_score = games[str(userid)][0]
    computer_actual = games[str(userid)][1]
    computer_showing = games[str(userid)][2]
    wager = games[str(userid)][3]

    print(str(userid) + " drew a " + str(player_card))

    if player_score > 21:
        games[userid] = [0, 0, 0, wager]
        save_games()
        update_earnings(str(userid), float(-wager))
        return {
            "status": "bust",
            "player": player_score,
            "computer_actual": computer_actual,
            "computer_showing": computer_showing,
            "wager": wager,
        }

    elif player_score == 21:
        return {
            "status": "blackjack",
            "player": player_score,
            "computer_actual": computer_actual,
            "computer_showing": computer_showing,
            "wager": wager,
        }

    else:
        save_games()
        return {
            "status": "continue",
            "player": player_score,
            "computer_actual": computer_actual,
            "computer_showing": computer_showing,
            "wager": wager,
        }



def bjstand(userid: str):
    global games

    if userid not in games:
        return {"status": "error"}

    player_score, computer_actual, computer_showing, wager = games[userid]

    # Computer draws until >= 17
    while computer_actual < 17:
        computer_draw = random.randint(1, 14)
        if computer_actual < 11 and computer_draw == 1:
            computer_draw = 11
        elif computer_draw == 1:
            computer_draw = 1
        elif computer_draw > 9:
            computer_draw = 10
        
        computer_actual += computer_draw
        computer_showing += computer_draw
        print("computer drew a " + str(computer_draw))

    outcome = None
    if computer_actual > 21 or player_score > computer_actual:
        update_earnings(str(userid), float(wager))
        outcome = "win"
    elif player_score < computer_actual:
        update_earnings(str(userid), float(-wager))
        outcome = "lose"
    elif player_score == computer_actual:
        update_earnings(str(userid), float(0))
        outcome = "tie"

    games[userid] = [0, 0, 0, wager]
    save_games()

    return {
        "status": outcome,
        "player": player_score,
        "computer_actual": computer_actual,
        "computer_showing": computer_showing,
        "wager": wager,
    }
