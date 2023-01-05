# -*- coding: utf-8 -*-
# Copyright (c) 2019, Silvio Peroni <essepuntato@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.

import the_master
from json import load
from collections import OrderedDict
from os.path import exists, sep
from os import remove
from collections import Counter

def load_room(room_file_path):
    with open(room_file_path, encoding="utf-8") as f:
        room_json = load(f)
        
        return room_json["structure"], (room_json["start"]["x"], room_json["start"]["y"]), (room_json["exit"]["x"], room_json["exit"]["y"])

def is_in_room(pos, room):
    dimension = len(room)
    return pos[0] >= 0 and pos[1] >= 0 and pos[0] < dimension and pos[1] < dimension

def is_valid_move(current_position, new_position, room):
    # The new position must be different from the current one
    if current_position == new_position:
        return False

    # The current position must be in the board
    if not is_in_room(current_position, room):
        return False
    
    # The new position must refer to an adjacent of current position
    x, y = current_position[0], current_position[1]
    valid_moves = set()
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            move = (x + dx, y + dy)
            if is_in_room(move, room):
                valid_moves.add(move)
    if new_position not in valid_moves:
        return False
    
    # The new position must not be in a cell controlled by bishops and rocks
    rocks = set()
    bishops = set()
    safe_cells = set()

    for row in room:
        for cell in row:
            position = (cell["x"], cell["y"])
            if cell["type"] == "bishop":
                bishops.add(position)
            elif cell["type"] == "rock":
                rocks.add(position)
            else:
                safe_cells.add(position)
    
    for x, y in rocks:
        for diff in [-1, 1]:
            try:
                safe_cells.remove((x + diff, y))
            except KeyError:
                pass
            try:
                safe_cells.remove((x, y + diff))
            except KeyError:
                pass

    for x, y in bishops:
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                try:
                    safe_cells.remove((x + dx, y + dy))
                except KeyError:
                    pass
    
    return new_position in safe_cells

def play(players, status, notebooks, current_turn,
         exit, room, final_results, cheaters, winners):

    for player in players:
        player_name = player.__name__
        
        if player_name not in cheaters and player_name not in winners:
            current_position = status[player_name]
            
            new_position, updated_notebook = \
                player.do_move(room, current_position, exit, notebooks[player_name])
            
            if is_valid_move(current_position, new_position, room):
                status[player_name] = new_position
                notebooks[player_name] = updated_notebook
                if is_winner(player_name, new_position, exit, current_turn, final_results):
                    winners.add(player_name)
            else:
                del status[player_name]
                del notebooks[player_name]
                cheaters.add(player_name)
            
    return len(cheaters) + len(winners) == len(players)
    
def is_winner(player_name, move, exit, current_turn, final_result):
    result = False
    
    if move == exit:
        result = True
        winners = final_result.get(current_turn)
        
        if winners is None:
            winners = []
            final_result[current_turn] = winners

        winners.append(player_name)
    
    return result

if __name__ == "__main__":
    all_players = [the_master]

    final_results = {
        "cheaters": set(),
        "best_rank": [],
        "found_exit": []
    }

    if exists("00_results.txt"):
        remove("00_results.txt")

    all_players_name = set()

    for idx in range(1, 101):
        cur_room, cur_entrance, cur_exit = load_room("boards" + sep + str(idx) + ".json")
        edge_size = len(cur_room)
        final_rank = OrderedDict()
        cur_status = {}
        notebooks = {}

        for player in all_players:
            player_name = player.__name__
            all_players_name.add(player_name)
            cur_status[player_name] = cur_entrance
            notebooks[player_name] = {}
        
        cheaters = set()
        winners = set()
        for current_turn in range(1, (edge_size * edge_size) + 1):
            all_players_out = play(all_players, cur_status, notebooks, current_turn,
                                   cur_exit, cur_room, final_rank, 
                                   cheaters, winners)
            
            if all_players_out:
                break
        
        final_results["cheaters"].update(cheaters)
        final_results["best_rank"].extend(list(final_rank.values())[0] if final_rank else set())
        final_results["found_exit"].extend(winners)

        final_rank_list = ["\n\n## Room " + str(idx) + " ##", "FINAL RANKS"]
        for rank, info in enumerate(final_rank.items(), 1):
            final_rank_list.append("Rank " + str(rank))
            final_rank_list.append(
                "\t" + ", ".join(info[1]) + " at turn " + str(info[0]))
        
        with open("00_results.txt", "a", encoding="utf-8") as f:
            f.write("\n".join(final_rank_list))
    
    final_results_str = "\n\n## FINAL RESULTS ##\nAvoiding non-permitted moves: " +  " ".join(all_players_name.difference(final_results["cheaters"])) + "\nFind exit of at least 30 boards: " + " ".join(Counter({k: v for k, v in Counter(final_results["found_exit"]).items() if v >= 30}).keys()) + "\nFind exit of at least 90 boards: " + " ".join(Counter({k: v for k, v in Counter(final_results["found_exit"]).items() if v >= 90})) + "\nBest winner: " + " ".join({k: v for k, v in Counter(final_results["best_rank"]).items() if v == max(Counter(final_results["best_rank"]).values())})

    with open("00_results.txt", "a", encoding="utf-8") as f:
        f.write(final_results_str)
    
    print(final_results_str)
