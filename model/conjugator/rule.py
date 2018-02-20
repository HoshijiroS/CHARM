class Rule:
    default_rule = None
    rules = []
    name = ""
    doubling = True

    def __init__(self, name, default_rule, rules):
        self.default_rule = default_rule
        self.name = name
        self.rules = rules
        if name is "PRESENT_TENSE":
            self.doubling = False

    def string(self):
        return self.name
