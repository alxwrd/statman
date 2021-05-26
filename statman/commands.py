
class CommandHandler:

    registered_commands = {}

    def __init__(self):
        pass


def command(string):
    def decorator(func):
        CommandHandler.registered_commands[string] = func
        return lambda: None
    return decorator
