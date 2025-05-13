from typing import List


def parse_music(music_string: str) -> List[int]:


    def count_beats(note: str) -> int:
        if note == "o": return 4
        elif note == "o|": return 2
        elif note == ".|": return 1
    
    if music_string == "": return []
    return list(map(count_beats, music_string.split(" ")))

