#!/usr/bin/env python3

'''
Canvas application launcher
'''

from commands import (
    ExitCommand,
    CreateCanvasCommand,
    DrawLineCommand,
    DrawRectangleCommand,
    BucketFillCommand,
    DeleteCommand,
    UndoCommand
)

canvas = None

def main():
    '''
    Canvas application entry point
    '''
    commands = _create_commands_dictionary()

    while True:
        user_input = input()
        input_items = user_input.split(' ')
        cmd_name = input_items[0]
        cmd_args = input_items[1:]
        try:
            cmd = commands[cmd_name]
            cmd.execute(*cmd_args)
        except KeyError:
            print("Unknown command")
        except (ValueError, TypeError) as ex:
            print(str(ex))
        else:
            print(str(canvas))


def _create_commands_dictionary():
    def assign_canvas_fn(new_canvas):
        #pylint: disable=missing-docstring
        global canvas
        canvas = new_canvas

    return {
        'C': CreateCanvasCommand(assign_canvas_fn),
        'L': DrawLineCommand(lambda: canvas),
        'R': DrawRectangleCommand(lambda: canvas),
        'B': BucketFillCommand(lambda: canvas),
        'D': DeleteCommand(lambda: canvas),
        'U': UndoCommand(lambda: canvas),
        'Q': ExitCommand()
    }


if __name__ == "__main__":
    main()
