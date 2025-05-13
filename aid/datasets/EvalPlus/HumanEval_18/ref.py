

def how_many_times(string: str, substring: str) -> int:


    occurences = 0
    for i in range(len(string)):
        if string[i:].startswith(substring):
            occurences += 1
    return occurences

