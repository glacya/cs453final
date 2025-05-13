
def words_string(s):

    words = (s.replace(",", " ")).split()
    return [word for word in words if word != ""]

