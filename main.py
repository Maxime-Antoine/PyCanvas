#!/usr/bin/env python3

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
    commands = create_commands_dictionary()

    while True:
        user_input = input()
        input_items = user_input.split(' ')
        cmd_name = input_items[0]
        cmd_args = input_items[1:]
        try:
            cmd = commands[cmd_name]
        except KeyError:
            print("Unknown command")
        else:
            try:
                cmd.execute(*cmd_args)
            except (ValueError, TypeError) as ex:
                print(str(ex))
            else:
                print(str(canvas))


def create_commands_dictionary():
    def assign_canvas_fn(x):
        global canvas
        canvas = x

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
