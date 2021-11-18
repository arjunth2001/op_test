import re


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def removePattern(text, pattern):

    r = re.findall(pattern, text)

    for i in r:

        text = re.sub(i, '', text)

    return text


def remove_urls(vTEXT):
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b',
                   '', vTEXT, flags=re.MULTILINE)
    return(vTEXT)


def sum_clean_text(text):
    if type(text) != str:
        return " "
    text = remove_urls(text)
    text = cleanhtml(text)
    text = removePattern(text, "@[\w]*")  # remove handles
    text = removePattern(text, "&[\w]*")  # remove &amp
    return text


def clean_text(text):
    if type(text) != str:
        return text
    text = text.lower()  # lower case
    text = remove_urls(text)
    text = cleanhtml(text)
    text = removePattern(text, "@[\w]*")  # remove handles
    text = removePattern(text, "&[\w]*")  # remove &amp
    # remove special characters, punctuations
    text = re.sub('[!@$:);/#,.*$?।&"]', '', text)
    return text
