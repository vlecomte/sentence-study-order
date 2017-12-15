from collections import Counter
from lemmatizer import lemmatize, lemmatizeZealous
from util import *

ngram = 6
freqList = []
freqId = {}
    
def getFreqId(word):
    if isInt(word) or isLatin(word):
        return 0
    return freqId[word]

class Card:
    def __init__(self, original, audio, translation, freq):
        self.original = original
        self.audio = audio
        self.translation = translation
        self.freq = freq
    def makeBold(self):
        self.bold = self.original
        for word in getRawWords(self.original):
            if getFreqId(lemmatize(word)) == self.freq:
                self.bold = boldWord(self.bold, word)
    def __repr__(self):
        return self.original + "\t" + freqList[self.freq] + " (rank " + str(self.freq) + ")"
    def __str__(self):
        return self.original + "\t" + self.bold + "\t" + self.audio + "\t" + self.translation

# Selects a subset of the cards that teach a "new word" to avoid redundancy
# - will select at least one card for every form of the new word that appears
# - if this results in less than 3 cards, add arbitrary cards to reach 3 (if possible)
def selection(freq, cards):
    used = set()
    choice = []
    
    # First pass through the cards
    for card in cards:
        ok = False
        for word in getWords(card.original):
            # If the card has a form that was not seen before, take it
            if getFreqId(lemmatize(word)) == freq and word not in used:
                used.add(word)
                ok = True
        if ok:
            choice.append(card)
    
    # While there are too few cards, try and add some
    while len(choice) < min(3, len(cards)):
        for card in cards:
            if card not in choice:
                choice.append(card)
                break
    
    return choice

allF = "all-sentences.txt"
tenF = "only-10.txt"
thousandF = "only-1000.txt"
with open(allF) as f:
    # Read the original sentences
    cards = []
    cnt = Counter()
    byNGram = {}
    sentences = [] # just for debugging purposes
    removed = 0
    for (num,line) in enumerate(f):
        audio, original, translation = line.split("\t")[:3]
        sentences.append(original)
        
        # Keep track of the occurrences of each lexeme
        cnt.update([lemmatize(word) for word in getWords(original)])
        
        # Get rid of overly similar sentences
        lemmas = [lemmatizeZealous(word) for word in getWords(original)]
        ok = True
        for i in range(len(lemmas)-ngram+1):
            gram = tuple(sorted(lemmas[i:i+ngram]))
            # The sentence is deleted if it has an n-gram of lexemes which is
            # equal (up to permutation) to another sentence
            if gram in byNGram and byNGram[gram] != num:
                ok = False
                #print("Too similar:")
                #print(sentences[byNGram[gram]])
                #print(original)
                break
            else:
                byNGram[gram] = num
        if ok:
            cards.append(Card(original, audio, translation, 0))
        else:
            removed += 1
    #print(removed)
    
    freqList = [word for (word,occ) in cnt.most_common()]
    freqId = {word: rank for (rank,word) in enumerate(freqList)}
    
    # Isolate the least frequent word in each card (the "new word")
    # and sort them by decreasing frequency of the "new word"
    for card in cards:
        for word in getWords(card.original):
            card.freq = max(card.freq, getFreqId(lemmatize(word)))
        card.makeBold()
    cards.sort(key = lambda card: card.freq)
    
    # Limit the number of sentences that teach the same "new word"
    last = -1
    finalChoice = []
    curPart = []
    for card in cards:
        # Run selection() every time we switch to another "new word"
        if card.freq != last:
            finalChoice.extend(selection(last, curPart))
            curPart = []
        last = card.freq
        curPart.append(card)
    finalChoice.extend(selection(last, curPart))
    cards = finalChoice
    
    # Print out the cards
    for card in cards:
        print(card)
