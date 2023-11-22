def saved_char_replacement(string):

    return (str(string)
            .replace('"', '&#34;')
            .replace("'", "\'")
            # .replace("'", '&#39;')
            .replace('&', '&#38;')
            .replace('<', '&#60;')
            .replace('>', '&#62;')
            ) if string else None

