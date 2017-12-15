import re

def isInt(word):
    try:
        int(word)
        return True
    except ValueError:
        return False

def isLatin(word):
    for char in word:
        if ord(char) < ord('a') or ord('z') < ord(char):
            return False
    return True

# Extract words made of letters and dashes from a string
def getRawWords(s):
    return re.compile("[\w-]+").findall(s)

# Same but lowercase
def getWords(s):
    return [word.lower() for word in getRawWords(s)]

# Bold the first non-bolded occurrence of word sub in s
# (actually just checks if it's surrounded by non-word, non-angle brackets characters)
def boldWord(s, word):
    bolded = re.sub(r"(^|[^\w<>])" + word + r"($|[^\w<>])", r"\1<b>" + word + r"</b>\2", s, 1)
    assert(bolded != word)
    return bolded
