def valid_date(date):
    if date == '':
        return False
    else:
        date = date.split('-')
        if len(date)!= 3:
            return False
        else:
            if date[0] == '':
                return False
            else:
                if date[1] == '':
                    return False
                else:
                    if date[2] == '':
                        return False
                    else:
                        if int(date[0]) > 12 or int(date[0]) < 1:
                            return False
                        else:
                            if int(date[0]) in [1, 3, 5, 7, 8, 10, 12] and (int(date[1]) > 31 or int(date[1]) < 1):
                                return False
                            elif int(date[0]) in [4, 6, 9, 11] and (int(date[1]) > 30 or int(date[1]) < 1):
                                return False
                            elif int(date[0]) == 2 and (int(date[1]) > 29 or int(date[1]) < 1):
                                return False
                            else:
                                if int(date[2]) > 2020 or int(date[2]) < 1900:
                                    return False
                                return True