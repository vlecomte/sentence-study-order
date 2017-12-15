import pymorphy2

morph = pymorphy2.MorphAnalyzer()

def generate(rules):
    return {inflected: normalForm
        for (normalForm, inflectedList) in rules.items()
        for inflected in inflectedList}

customRules = generate({
    "знать": ["знаешь", "знаете"],
    "ночь": ["ночью"],
    "цвет": ["цвет", "цветы"],
    "любой": ["любой"],
    "сильный": ["силён"],
    "третий": ["третьего", "третьем"],
    "слушать": ["слушай"],
    "вода": ["вода"],
    "низкий": ["низкой"],
    "казаться": ["казалось"],
    "любить": ["любим"],
    "триста": ["трёхсот"],
    "нибудь": ["нибудь"],
    "светлый": ["светлую"],
    "голова": ["голове", "головы"],
    "англо": ["англо"],
    "час": ["часами"],
    "снимок": ["снимок"],
    "давний": ["давным"],
    "сахар": ["сахара"],
    "часть": ["частью"],
    "холодный": ["холодным", "холодного"],
    "великий": ["великим", "великие"],
    "ожерелье": ["ожерелье"],
    "пожилой": ["пожилого"],
    "дешёвый": ["дёшев"],
    "цыпочки": ["цыпочках"],
    "проливной": ["проливной"],
    "нар": ["наре"],
    "белый": ["белые", "белых"],
    "ось": ["ось"],
    "короткий": ["короче"],
    "она": ["нею"],
    "похудеть": ["похудел"],
    "небезопасный": ["небезопасно"],
    "риск": ["риски"],
    "ныть": ["ною"],
    "дитё": ["дитём"],
    "унизительный": ["унизительно"],
    "тень": ["тени"],
    "любимый": ["любимом"],
    "намерен": ["намерены"],
    "впечатлённый": ["впечатлён"],
    "побежать": ["побежал"],
    "планета": ["планета", "планетах"],
    "каруйзава": ["каруйзаве"],
    "нерешённый": ["нерешённой"],
    "фудзи": ["фудзи"],
    "бива": ["бива"],
    "электротехника": ["электротехник"],
    "гувер": ["гувер"],
    "хокку": ["хокку"],
    "мини": ["мини"],
    "эверетт": ["эверетт"],
    "игра": ["видеоигра", "видеоигры"],
    "вещь": ["вещи", "вещей"],
})

stricterRules = generate({
    "я": ["я", "ты", "он", "она", "мы", "вы", "они"],
})

def lemmatize(word):
    word = word.lower()
    return customRules.get(word, morph.parse(word)[0].normal_form)

def lemmatizeZealous(word):
    word = lemmatize(word)
    return stricterRules.get(word, word)
