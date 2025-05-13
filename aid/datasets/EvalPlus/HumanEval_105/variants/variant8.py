def by_length(arr):
    if not arr:
        return []
    
    arr = sorted([num for num in arr if 1 <= num <= 9], reverse=True)
    
    number_names = {
        0: "Zero",
        1: "One",
        2: "Two",
        3: "Three",
        4: "Four",
        5: "Five",
        6: "Six",
        7: "Seven",
        8: "Eight",
        9: "Nine"
    }
    
    res = [number_names[num] for num in arr]
    
    return res