def replace_last(s, old, new):
    last_index = s.rfind(old)
    if last_index != -1:
        return s[:last_index] + new + s[last_index + len(old) :]
    return s
