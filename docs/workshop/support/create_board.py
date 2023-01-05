from random import shuffle, choice
from networkx import Graph, NetworkXError, shortest_path
from collections import defaultdict
from argparse import ArgumentParser
from os import makedirs
from os.path import exists, sep
from json import dump

def get_edge_cells(set_of_cells, edge_size):
    result = defaultdict(list)

    for x, y in set_of_cells:
        if 0 <= x < edge_size - 1 and y == 0:
            result["top"].append((x, y))
        elif x == 0 and 1 <= y < edge_size:
            result["left"].append((x, y))
        elif 0 < x < edge_size and y == edge_size - 1:
            result["bottom"].append((x, y))
        elif x == edge_size - 1 and 0 <= y < edge_size - 1:
            result["right"].append((x, y))
    
    return result


def find_start_and_exit(board, edge_size):
    g = Graph()
    board_len = len(board)
    bishops = set()
    rocks = set()
    
    for row in board:
        for cell in row:
            x = cell["x"]
            y = cell["y"]
            t = cell["type"]
            cur_cell = (x, y)

            if t == "rock":
                rocks.add(cur_cell)
            elif t == "bishop":
                bishops.add(cur_cell)
            
            if x > 0:
                g.add_edge((x-1,y), cur_cell)
                if y > 0:
                    g.add_edge((x-1,y-1), cur_cell)
            if y > 0:
                g.add_edge((x,y-1), cur_cell)
                if x < board_len - 1:
                    g.add_edge((x+1,y-1), cur_cell)

    for x, y in rocks:
        try:
            g.remove_node((x, y))
        except NetworkXError:
            pass
        for diff in [-1, 1]:
            try:
                g.remove_node((x + diff, y))
            except NetworkXError:
                pass
            try:
                g.remove_node((x, y + diff))
            except NetworkXError:
                pass

    for x, y in bishops:
        try:
            g.remove_node((x, y))
        except NetworkXError:
            pass
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                try:
                    g.remove_node((x + dx, y + dy))
                except NetworkXError:
                    pass

    candidates = list()
    s_paths = shortest_path(g)
    for s in s_paths:
        for t in s_paths[s]:
            if s != t:
                candidates.append((s, t))

    if candidates:
        return choice(candidates)
    else:
        return None, None

def get_number_of_cells(total, p_free, p_rook, p_bishop):
    n_free = round((total / 100) * p_free)
    n_rook = round((total / 100) * p_rook)
    n_bishop = round((total / 100) * p_bishop)

    diff = total - (n_free + n_rook + n_bishop)
    while diff != 0:
        if diff > 0:
            val = 1
            diff -= 1
        else:
            val = -1
            diff += 1
        n_free += val
    
    return n_free, n_rook, n_bishop

def create_board(edge_size, p_free, p_rook, p_bishop):
    free, rook, bishop = get_number_of_cells(edge_size * edge_size, 
                                             p_free, p_rook, p_bishop)
    cell_list = free * ["free"] + rook * ["rock"] + bishop * ["bishop"]
    shuffle(cell_list)

    structure = []
    for y in range(edge_size):
        row = []
        for x in range(edge_size):
            cell = cell_list.pop(0)
            row.append({
                "x": x,
                "y": y,
                "type": cell
            })
        structure.append(row)
                
    start, exit = find_start_and_exit(structure, edge_size)

    if start is not None and exit is not None:
        return {
            "structure": structure,
            "start":{
                "x": start[0],
                "y": start[1]
            } ,
            "exit" : {
                "x": exit[0],
                "y": exit[1]
            }
        }

if __name__ == "__main__":
    arg_parser = ArgumentParser("Create Board")

    arg_parser.add_argument("-o", "--outdir", required=True,
                            help="The folder where to store the 100 boards.")
    
    args = arg_parser.parse_args()

    if not exists(args.outdir):
        makedirs(args.outdir)
    
    count_board = 1
    base_edge = 4
    edge_size = base_edge
    multiplier = 0
    divider = 4

    while count_board < 101:
        board = None

        while board is None:
            p_free = 0
            while p_free < 50:
                p_free = choice(range(101))
                p_bishop = choice(range(101 - p_free))
                p_rook = 100 - p_free - p_bishop

            board = create_board(edge_size, p_free, p_rook, p_bishop)
            if board is not None:
                print(count_board, 
                    f"- Generated board {edge_size}x{edge_size} with {p_free}% "
                    f"free cells, {p_bishop}% bishops and {p_rook}% rooks")
        
        with open(args.outdir + sep + str(count_board) + ".json", "w", encoding="utf-8") as f:
            dump(board, f)
        
        multiplier += 1
        edge_size = base_edge * ((multiplier % divider) + 1)
        count_board += 1
