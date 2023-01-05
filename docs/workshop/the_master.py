from networkx import Graph, shortest_path, NetworkXError

def do_move(board, current, exit, notebook):
    
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

    s_path = shortest_path(g, source=current, target=exit)
    return s_path[1], notebook
    