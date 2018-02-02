class Location:
    name = ""
    prop = []
    attr = []

    def __init__(self, name):
        self.name = name
        self.prop = []
        self.attr = []

    def hasProperty(self, prop, scene):
        propPair = [prop, scene]
        self.prop.append(propPair)

    def hasAttribute(self, attribute, action, scene):
        attrPair = [action, attribute, scene]
        self.attr.append(attrPair)

    def queryProperty(self, prop_name, scene_name):
        # entity[0] = property
        # entity[1] = scene

        if prop_name is not None:
            for entity in self.prop:
                if entity[0] == prop_name:
                    return entity[1]

        if scene_name is not None:
            for entity in self.prop:
                if entity[1] == scene_name:
                    return entity[0]

        return None

    def queryAttribute(self, act_name, attr_name):
        # entity[0] = actions
        # entity[1] = attribute
        # entity[2] = scene

        for entity in self.attr:
            if entity[1] == attr_name:
                for action in entity[0]:
                    if action == act_name:
                        return entity[1], entity[2]
        return None