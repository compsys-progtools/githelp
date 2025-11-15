def make_greeting(name, shout = False):
    if(shout):
        suffix = "!"
    else:
        suffix = "."
    return f"Hello, {name}{suffix}"