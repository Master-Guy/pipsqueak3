def extractFlags(_input: str):
    double_flags = []
    single_flags = []
    other_words = []

    for word in _input:
        if word.startswith('--'):
            double_flags.append(word[2:])
        elif word.startswith('-'):
            single_flags.append(word[1:])
        else:
            other_words.append(word)

    single_flags = "".join(set("".join(single_flags)))
    return double_flags, single_flags, other_words
