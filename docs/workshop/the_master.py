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
    