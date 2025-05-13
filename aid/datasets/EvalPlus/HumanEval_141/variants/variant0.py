def file_name_check(file_name):
    import re
    # check if there are more than three digits in the file's name
    if len(re.findall('\d', file_name)) > 3:
        return 'No'
    # check if there is exactly one dot '.' in the file's name
    if file_name.count('.') != 1:
        return 'No'
    # check if the substring before the dot is not empty and starts with a letter
    if not re.match('^[a-zA-Z]', file_name.split('.')[0]):
        return 'No'
    # check if the substring after the dot is one of these: ['txt', 'exe', 'dll']
    if not re.match('(txt|exe|dll)$', file_name.split('.')[1]):
        return 'No'
    return 'Yes'