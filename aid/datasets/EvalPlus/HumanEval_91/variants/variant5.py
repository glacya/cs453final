def is_bored(S):
    count = 0
    sentences = re.split("[.?!]", S)
    for sentence in sentences:
        words = sentence.strip().split()
        if words and words[0] == "I":
            count += 1
    return count