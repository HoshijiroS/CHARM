import re

class RegexRule:

    EXCEPTION = 0
    GENERIC = 1
    DEFAULT = 2

    leftHandSide = None
    leftHandString = ""
    offset = 0
    suffix = ""

    def __init__(self, regex, truncate, suff, notused=0):
        self.leftHandSide = re.compile(regex)
        self.leftHandString = regex
        self.offset = truncate
        self.suffix = suff

    def to_string(self):
        return "RE: " + self.leftHandString + "->" + self.suffix

    def applies(self, word):
        word = word.strip()
        return len(self.leftHandSide.findall(word)) > 0

    def fire(self, word):
        word = word.strip()
        return word[0:len(word)-self.offset] + self.suffix

    def analyze(self, word):
        if self.suffix != "" and word.endswith(self.suffix):
            return True
        return False