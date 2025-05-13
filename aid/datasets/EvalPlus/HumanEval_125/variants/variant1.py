def split_words(txt):
    # Check if there is whitespace in the input text
    if ' ' in txt:
        return txt.split() # Split the text on whitespaces and return the list of words
    # Check if there is a comma in the input text
    elif ',' in txt:
        return txt.split(',')  # Split the text on commas and return the list of words
    else:
        # If no whitespaces or commas, count the number of lower-case letters with odd order in the alphabet
        return len([i for i in txt if ord(i) >= ord('a') and ord(i) <= ord('z') and (ord(i) - ord('a')) % 2 != 0]) # Count the number of lowercase letters with odd order in the alphabet