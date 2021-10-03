"""This program reads the mobypron.unc file, then can split any text into pronounceable text."""

import re


def main():
    """This main program calls all other methods."""
    with open("data/mobypron.unc", encoding="ISO-8859-1") as mobypron_file:
        mobypron = mobypron_file.read()

    map_word_moby = split(mobypron)
    map_word_ipa = [
        (
            remove_underlines(word),
            convert_moby_to_ipa(moby, word),
            convert_word_to_pos(word),
        )
        for word, moby in map_word_moby.items()
    ]

    with open("data/word_to_ipa.csv", "w") as word_to_ipa:
        for (word, ipa, part_of_speech) in map_word_ipa:
            print(f'"{word}", "{ipa}", "{part_of_speech}"', file=word_to_ipa)


def split(text):
    """Turns the mobypron.unc file into a dictionary"""
    map_word_moby = {}
    try:
        lines = text.split("\n")
        for line in lines:
            (word, moby) = line.split(" ", 1)
            map_word_moby[word] = moby

    except IOError as error:
        print(f"Failed due to IOError: {error}")

    return map_word_moby


def remove_underlines(word):
    """Removes both underlines and the occasional grammar mark from words"""
    return re.sub("/.*$", "", word).replace("_", " ")


def convert_moby_to_ipa(moby, word):
    """Turns an individual moby expression into an IPA expression."""
    return combine_moby(convert_moby_array_to_ipa_array(parse_moby(moby), word))


def convert_word_to_pos(word):
    """Retrieves the part of speech, if given, from the word."""
    match = re.search("(/.*$)", word)
    if match:
        return match.group(1).replace("/", "")

    return ""


# Input: A Moby string
# Output: An array of the underlying characters.


def parse_moby(moby):
    """Turns a moby word into an array of moby characters."""
    moby_array = []
    in_expression = False
    current_char = ""
    for mobychar in moby:
        if not in_expression and mobychar != "/":
            moby_array.append(mobychar)
            continue

        if not in_expression and mobychar == "/":
            in_expression = True
            current_char = mobychar
            continue

        if in_expression:
            current_char += mobychar

            if mobychar == "/":
                moby_array.append(current_char)
                current_char = ""
                in_expression = False

    return moby_array


def convert_moby_array_to_ipa_array(moby_array, word):
    """Changes an array of moby characters to an array of IPA characters"""
    return [convert_moby_char_to_ipa(moby_char, word) for moby_char in moby_array]


moby_to_ipa = {
    "/&/": "æ",
    "/(@)/": "ɛ",
    "/[@]/": "ɛ",
    "/A/": "ɑ",
    "/eI/": "eɪ",
    "/@/": "ə",
    "@": "ə",
    "/-/": "ə",
    "b": "b",
    "/b/": "b",
    "/tS/": "ʧ",
    "d": "d",
    "/d/": "d",
    "/E/": "ɛ",
    "i": "i",
    "/i/": "i",
    "f": "f",
    "g": "g",
    "h": "h",
    "/hw/": "w",
    "/I/": "ɪ",
    "/aI/": "aɪ",
    "/dZ/": "ʤ",
    "k": "k",
    "l": "l",
    "m": "m",
    "/N/": "ŋ",
    "n": "n",
    "/Oi/": "ɔɪ",
    "/AU/": "aʊ",
    "/O/": "ɔ",
    "O": "ɔ",
    "o": "ɔ",
    "/oU/": "oʊ",
    "u": "u",
    "/u/": "u",
    "/U/": "ʊ",
    "p": "p",
    "r": "r",
    "/S/": "ʃ",
    "s": "s",
    "/T/": "θ",
    "/D/": "ð",
    "t": "t",
    "/@r/": "ɜr",
    "v": "v",
    "V": "v",
    "w": "w",
    "j": "j",
    "/j/": "j",
    "/Z/": "ʒ",
    "z": "z",
    "'": "ˈ",
    ",": "ˌ",
    "_": " ",
    "A": "ɑ",
    "N": "n",
    "R": "r",
    "/x/": "k",
    "/y/": "u",
    "Y": "u",
    "/ju/": "ju",
    "a": "æ",
    "e": "ɛ",
    "/z/": "z",
    "c": "s",
    "W": "w",
    "Z": "ʐ",
    "S": "s",
    " ": " ",
    "U": "ʌ",
    "-": " ",
    "x": "x",
    "/Ou/": "ɔ",
    "0": "œ",
    "/OE/": "œ",
    "3": "ɜ",
}


def convert_moby_char_to_ipa(moby_char, word):
    """Converts a moby character into an IPA character."""
    if moby_char in moby_to_ipa:
        return moby_to_ipa[moby_char]

    print(f"Unknown moby character: {moby_char} in {word}")
    return "?"


def combine_moby(list_ipa):
    """Turns an IPA list into an IPA string."""
    return "".join(list_ipa)


if __name__ == "__main__":
    main()
