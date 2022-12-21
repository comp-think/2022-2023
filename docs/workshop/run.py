from group import do_move

board = [
            [
                {
                    "x": 0,
                    "y": 0,
                    "type": "free"
                },
                {
                    "x": 1,
                    "y": 0,
                    "type": "rock"
                },
                {
                    "x": 2,
                    "y": 0,
                    "type": "free"
                },
                {
                    "x": 3,
                    "y": 0,
                    "type": "free"
                }
            ],
            [
                {
                    "x": 0,
                    "y": 1,
                    "type": "free"
                },
                {
                    "x": 1,
                    "y": 1,
                    "type": "free"
                },
                {
                    "x": 2,
                    "y": 1,
                    "type": "free"
                },
                {
                    "x": 3,
                    "y": 1,
                    "type": "free"
                }
            ],
            [
                {
                    "x": 0,
                    "y": 2,
                    "type": "free"
                },
                {
                    "x": 1,
                    "y": 2,
                    "type": "free"
                },
                {
                    "x": 2,
                    "y": 2,
                    "type": "free"
                },
                {
                    "x": 3,
                    "y": 2,
                    "type": "free"
                }
            ],
            [
                {
                    "x": 0,
                    "y": 3,
                    "type": "free"
                },
                {
                    "x": 1,
                    "y": 3,
                    "type": "free"
                },
                {
                    "x": 2,
                    "y": 3,
                    "type": "free"
                },
                {
                    "x": 3,
                    "y": 3,
                    "type": "bishop"
                }
            ]
        ]

start = (1, 3)
exit = (2, 0)

current_position = start
my_notebook = {}

while current_position != exit:
    current_position, my_notebook = do_move(board, current_position, exit, my_notebook)

print("I've found the exit!")