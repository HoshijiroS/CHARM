import model.externals.wordnet as WordNet
import model.story_world.classes.Item as Item
import model.story_world.classes.Location as Location
import model.story_world.classes.Relations as Rel
import model.story_world.classes.Scene as Scene
import model.story_world.entities as Entity
import model.story_world.rules as Rule
import random

lookup = []

wan_friend = Item.Item("friend")
peg_clothes = Item.Item("clothes")
mad_clothes = Item.Item("clothes")
wan_name = Item.Item("name")
wan_dress = Item.Item("dress")
mad_name = Item.Item("name")
cec_clothes = Item.Item("dress")
giv_mad_dress = Item.Item("dress")
giv_peg_dress = Item.Item("dress")

scene_1 = Scene.Scene("Scene 1", "Monday1")
scene_2 = Scene.Scene("Scene 2", "Tuesday2")
scene_3 = Scene.Scene("Scene 3", "Wednesday3")
scene_4 = Scene.Scene("Scene 4", "Wednesday4")
scene_5 = Scene.Scene("Scene 5", "Wednesday5")
scene_6 = Scene.Scene("Scene 6", "Wednesday6")
scene_7 = Scene.Scene("Scene 7", "Wednesday7")
scene_8 = Scene.Scene("Scene 8", "Wednesday8")
scene_9 = Scene.Scene("Scene 9", "Wednesday9")
scene_10 = Scene.Scene("Scene 10", "Thursday10")
scene_11 = Scene.Scene("Scene 11", "Thursday11")
scene_12 = Scene.Scene("Scene 12", "Thursday12")
scene_13 = Scene.Scene("Scene 13", "Thursday13")
scene_14 = Scene.Scene("Scene 14", "Thursday14")
scene_15 = Scene.Scene("Scene 15", "Thursday15")
scene_16 = Scene.Scene("Scene 16", "Friday16")
scene_17 = Scene.Scene("Scene 17", "Christmas Time17")
scene_18 = Scene.Scene("Scene 18", "Christmas Time18")

relations = Rel.Relations("Relations for All Scenes")


def formatMultipleItems(listAnswer):
    if len(listAnswer) > 1 and type(listAnswer) is not str:
        out = ", ".join(listAnswer[:-1]) + " and " + listAnswer[len(listAnswer) - 1]
    elif type(listAnswer) is str:
        out = listAnswer
    else:
        out = listAnswer[0]

    return out


def assembleSentence():
    sentences = {}

    for entry in lookup:
        time, actor, entryType = entry
        actor = actor.lower()

        if entryType == "action":
            try:
                act, obj, scene = Entity.charList[actor].queryAction(None, time)
            except Exception as e:
                # print("Error: ", e, " on ", time, " charAction")
                a = 1

            try:
                act, obj, scene = Entity.itemList[actor].queryAction(None, time)
            except Exception as e:
                # print("Error: ", e, " on ", time, " itemAction")
                a = 1

            if obj:
                if type(obj) is str:
                    out_obj = obj

                elif type(obj) is list:
                    temp = []
                    for entries in obj:
                        if type(entries) is str:
                            temp.append(entries)
                        else:
                            temp.append(entries.name)

                    out_obj = formatMultipleItems(temp)

                else:
                    out_obj = obj.name

                    #print("appearance properties: ", obj.appProp)
                    prop, scene = obj.queryProperty(None, "appearance", time + "ext")
                    if prop:
                        #print("property: ", prop)
                        out_app = formatMultipleItems(prop)
                        out_obj = out_app + obj.name

                    #print("amount properties: ", obj.amtProp)
                    prop, scene = attr.queryProperty(None, "amount", time + "ext")
                    if prop:
                        #print("property: ", prop)
                        out_amt = formatMultipleItems(prop)
                        out_obj = out_amt + obj.name

                    #print("personality properties: ", obj.perProp)
                    prop, scene = attr.queryProperty(None, "personality", time + "ext")
                    if prop:
                        #print("property: ", prop)
                        out_per = formatMultipleItems(prop)
                        out_obj = out_per + obj.name

                # print("action: ", act[0])
                sentences["sentence for " + time] = actor + " " + act[0] + " " + out_obj

        elif entryType == "state":
            try:
                state, scene = Entity.charList[actor].queryState(None, time)
            except Exception as e:
                # print("Error: ", e, " on ", time, " actorState")
                a = 1

            try:
                state, scene = Entity.itemList[actor].queryState(None, time)
            except Exception as e:
                # print("Error: ", e, " on ", time, " itemState")
                a = 1

            if state:
                state = state[0]

                if type(state) is str:
                    sentences["sentence for " + time] = actor + " " + state
                else:
                    out_state = []

                    for entries in state:
                        out_state.append(entries)

                    out_state = formatMultipleItems(out_state)

                    sentences["sentence for " + time] = actor + " " + out_state

        elif entryType == "location":
            try:
                act, loc, scene = Entity.charList[actor].queryLocation(None, None, time)
            except Exception as e:
                # print("Error: ", e, " on ", time, " actorLocation")
                a = 1

            if loc:
                if type(loc) is str:
                    out_loc = loc
                else:
                    out_loc = loc.name

                sentences["sentence for " + time] = actor + " " + act[0] + " " + out_loc

        elif entryType == "desire":
            act, obj, scene = Entity.charList[actor].queryDesire(None, time)

            if type(obj) is str:
                out_obj = obj
            else:
                out_obj = obj.name

            sentences["sentence for " + time] = actor + " desires to " + act[0] + " " + out_obj

        elif entryType == "appProperty":
            try:
                prop, scene = Entity.charList[actor].queryProperty(None, "appearance", time)
            except Exception as e:
                # print("Error: ", e, " on ", time, "charAppearance")
                a = 1

            try:
                prop, scene = Entity.itemList[actor].queryProperty(None, "appearance", time)
            except Exception as e:
                a = 1
                # print("Error: ", e, " on ", time, " itemAppearance")

            try:
                prop, scene = Entity.locList[actor].queryProperty(None, "appearance", time)
            except Exception as e:
                a = 1
                # print("Error: ", e, " on ", time, "locationAppearance")

            if prop:
                out_prop = formatMultipleItems(prop)
                sentences["sentence for " + time] = actor + " is " + out_prop

        elif entryType == "perProperty":
            try:
                prop, scene = Entity.charList[actor].queryProperty(None, "personality", time)
            except Exception as e:
                a = 1
                # print("Error: ", e, " on ", time, " actorPersonality")

            try:
                prop, scene = Entity.itemList[actor].queryProperty(None, "personality", time)
            except Exception as e:
                a = 1
                # print("Error: ", e, " on ", time, " itemPersonality")

            try:
                prop, scene = Entity.locList[actor].queryProperty(None, "personality", time)
            except Exception as e:
                a = 1
                # print("Error: ", e, " on ", time, "locationPersonality")

            if prop:
                out_prop = formatMultipleItems(prop)
                sentences["sentence for " + time] = actor + " is " + out_prop

        elif entryType == "purpose":
            try:
                act, obj, scene = Entity.itemList[actor].queryPurpose(None, None, time)
            except Exception as e:
                a = 1
                # print("Error: ", e, " on ", time, " itemPurpose")

            sentences["sentence for " + time] = actor + " " + act[0] + " " + obj

        elif entryType == "attribute":
            try:
                act, attr, scene = Entity.charList[actor].queryAttribute(None, None, time)
            except Exception as e:
                a = 1
                # print("Error: ", e, " on ", time, " actorAttr")

            try:
                act, attr, scene = Entity.itemList[actor].queryAttribute(None, None, time)
            except Exception as e:
                a = 1
                # print("Error: ", e, " on ", time, " itemAttr")

            try:
                act, attr, scene = Entity.locList[actor].queryAttribute(None, None, time)
            except Exception as e:
                a = 1
                # print("Error: ", e, " on ", time, " locationAttr")

            if attr:
                sentences["sentence for " + time] = actor + " " + act[0] + " " + attr.name

                #print("appearanceProp: ", attr.appProp)
                prop, scene = attr.queryProperty(None, "appearance", time+"ext")
                if prop:
                    out_app = formatMultipleItems(prop)
                    # print("action: ", act[0])
                    sentences["sentence for " + time] = actor + " " + act[0] + " " + attr.name + " is " + out_app

                #print("amountProp: ", attr.amtProp)
                prop, scene = attr.queryProperty(None, "amount", time+"ext")
                if prop:
                    out_amt = formatMultipleItems(prop)
                    # print("action: ", act[0])
                    sentences["sentence for " + time] = actor + " " + act[0] + " " + out_amt + " " + attr.name

                #print("personalityProp: ", attr.perProp)
                prop, scene = attr.queryProperty(None, "personality", time+"ext")
                if prop:
                    out_per = formatMultipleItems(prop)
                    # print("action: ", act[0])
                    sentences["sentence for " + time] = actor + " " + act[0] + " " + attr.name + " is " + out_per

                # print("action: ", act[0])

    return sentences


def printSentences():
    output_sentences = []
    sentences = assembleSentence()

    # for key in sentences.keys():
    #     print(key, sentences[key])

    for entries in relations.causeList:
        a, b = entries
        comp_sent_a = []
        comp_sent_b = []

        if type(a) is str:
            comp_sent_a = sentences["sentence for " + a]

        elif type(a) is list:
            temp = []
            for sent in a:
                temp.append(sentences["sentence for " + sent])

            comp_sent_a = formatMultipleItems(temp)

        if type(b) is str:
            comp_sent_b = sentences["sentence for " + b]

        elif type(b) is list:
            temp = []
            for sent in b:
                temp.append(sentences["sentence for " + sent])

            comp_sent_b = formatMultipleItems(temp)

        output_sentences.append(comp_sent_a + ", because " + comp_sent_b + ".")

    for entries in relations.elabList:
        a, b = entries
        comp_sent_a = []
        comp_sent_b = []

        if type(a) is str:
            comp_sent_a = sentences["sentence for " + a]

        elif type(a) is list:
            temp = []
            for sent in a:
                temp.append(sentences["sentence for " + sent])

            comp_sent_a = formatMultipleItems(temp)

        if type(b) is str:
            comp_sent_b = sentences["sentence for " + b]

        elif type(b) is list:
            temp = []
            for sent in b:
                temp.append(sentences["sentence for " + sent])

            comp_sent_b = formatMultipleItems(temp)

        output_sentences.append(comp_sent_a + ", that " + comp_sent_b + ".")

    for entries in relations.summary:
        a, b = entries
        comp_sent_a = []
        comp_sent_b = []

        if type(a) is str:
            comp_sent_a = sentences["sentence for " + a]

        elif type(a) is list:
            temp = []
            for sent in a:
                temp.append(sentences["sentence for " + sent])

            comp_sent_a = formatMultipleItems(temp)

        if type(b) is str:
            comp_sent_b = sentences["sentence for " + b]

        elif type(b) is list:
            temp = []
            for sent in b:
                temp.append(sentences["sentence for " + sent])

            comp_sent_b = formatMultipleItems(temp)

        output_sentences.append(comp_sent_a + ", then " + comp_sent_b + ".")

    for entries in relations.contList:
        a, b = entries
        comp_sent_a = []
        comp_sent_b = []

        if type(a) is str:
            comp_sent_a = sentences["sentence for " + a]

        elif type(a) is list:
            temp = []
            for sent in a:
                temp.append(sentences["sentence for " + sent])

            comp_sent_a = formatMultipleItems(temp)

        if type(b) is str:
            comp_sent_b = sentences["sentence for " + b]

        elif type(b) is list:
            temp = []
            for sent in b:
                temp.append(sentences["sentence for " + sent])

            comp_sent_b = formatMultipleItems(temp)

        output_sentences.append(comp_sent_a + ", but " + comp_sent_b + ".")

    for entries in relations.consList:
        a, b = entries
        comp_sent_a = []
        comp_sent_b = []

        if type(a) is str:
            comp_sent_a = sentences["sentence for " + a]

        elif type(a) is list:
            temp = []
            for sent in a:
                temp.append(sentences["sentence for " + sent])

            comp_sent_a = formatMultipleItems(temp)

        if type(b) is str:
            comp_sent_b = sentences["sentence for " + b]

        elif type(b) is list:
            temp = []
            for sent in b:
                temp.append(sentences["sentence for " + sent])

            comp_sent_b = formatMultipleItems(temp)

        output_sentences.append(comp_sent_a + ", so " + comp_sent_b + ".")

    for sent in output_sentences:
        print(sent)


def startScene1():
    scene_1.hasLocation([Entity.locList["school"], Entity.locList["room 13"]])
    scene_1.hasCharacter([Entity.charList["wanda"], Entity.charList["students"]])

    ####
    Entity.charList["students"].hasAction(("not notice", WordNet.getVerbList("notice", negator="not")), Entity.charList["wanda"].name, scene_1.time + "ev1")
    lookup.append([scene_1.time + "ev1", Entity.charList["students"].name, "action"])

    Entity.charList["wanda"].hasState(("absent", WordNet.getAdjList("absent")), scene_1.time)
    lookup.append([scene_1.time, Entity.charList["wanda"].name, "state"])

    relations.causedBy(scene_1.time + "ev1", scene_1.time)

    Entity.charList["wanda"].hasAttribute(wan_friend, ("have", WordNet.getVerbList("have")), scene_1.time + "inf1")
    lookup.append([scene_1.time + "inf1", Entity.charList["wanda"].name, "attribute"])

    wan_friend.hasAmtProperty(["no"], scene_1.time + "inf1ext")
    lookup.append([scene_1.time + "inf1ext", wan_friend.name, "amtProperty"])

    relations.causedBy(scene_1.time + "ev1", scene_1.time + "inf1")
    ####

    ####
    Entity.charList["wanda"].hasLocation(Entity.locList["corner of the room"], ("sit", WordNet.getVerbList("sit")), scene_1.time + "ev2")
    lookup.append([scene_1.time + "ev2", Entity.charList["wanda"].name, "location"])

    Entity.locList["boggins heights"].hasAttribute(Entity.locList["boggins heights road"], ("have", WordNet.getVerbList("have")), scene_1.time + "inf4")
    lookup.append([scene_1.time + "inf4", Entity.locList["boggins heights"].name, "attribute"])

    Rule.assignPropBySeating(Entity.charList["wanda"], scene_1.time + "inf2")
    lookup.append([scene_1.time + "inf2", Entity.charList["wanda"].name, "attribute"])
    lookup.append([scene_1.time + "inf2ext", "shoes", "appProperty"])

    relations.causedBy(scene_1.time + "ev2", scene_1.time + "inf2")
    ####

    ####
    Entity.charList["wanda"].hasLocation(Entity.locList["boggins heights"], ("live", WordNet.getVerbList("live")), scene_1.time + "inf3")
    lookup.append([scene_1.time + "inf3", Entity.charList["wanda"].name, "location"])

    relations.causedBy(scene_1.time + "inf2", scene_1.time + "inf3")
    ####


def startScene2():
    scene_2.hasLocation([Entity.locList["school"], Entity.locList["room 13"]])
    scene_2.hasCharacter([Entity.charList["wanda"], Entity.charList["bill byron"]])

    ####
    Entity.charList["bill byron"].hasAction(("notice", WordNet.getVerbList("notice")), Entity.charList["wanda"].name, scene_2.time + "ev1")
    lookup.append([scene_2.time + "ev1", Entity.charList["bill byron"].name, "action"])

    Entity.charList["wanda"].hasState(("absent", WordNet.getAdjList("absent")), scene_2.time)
    lookup.append([scene_2.time, Entity.charList["wanda"].name, "state"])

    relations.sequence(scene_2.time, scene_2.time + "ev1")

    Entity.charList["bill byron"].hasLocation("behind Wanda", ("sit", WordNet.getVerbList("sit")), scene_2.time + "inf1")
    lookup.append([scene_2.time + "inf1", Entity.charList["bill byron"].name, "location"])

    Entity.charList["bill byron"].hasLocation(Entity.locList["corner of the room"], ("sit", WordNet.getVerbList("sit")), scene_2.time + "inf2")
    lookup.append([scene_2.time + "inf2", Entity.charList["bill byron"].name, "location"])

    Rule.assignPropBySeating(Entity.charList["bill byron"], scene_2.time + "inf3")
    lookup.append([scene_2.time + "inf3", Entity.charList["bill byron"].name, "perProperty"])

    relations.causedBy(scene_2.time + "ev1", [scene_2.time + "inf1", scene_2.time + "inf2"])
    # relations.sequence(startScene1.scene_1.time + "ev2", scene_2.time + "ev1")
    ####


def startScene3():
    scene_3.hasLocation([Entity.locList["school"], Entity.locList["room 13"]])
    scene_3.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"]])

    ####
    Entity.charList["maddie"].hasState(["late to school"], scene_3.time + "ev1a")
    lookup.append([scene_3.time + "ev1a", Entity.charList["maddie"].name, "state"])

    Entity.charList["peggy"].hasState(["late to school"], scene_3.time + "ev1b")
    lookup.append([scene_3.time + "ev1b", Entity.charList["peggy"].name, "state"])

    Entity.charList["maddie"].hasAction(("wait", WordNet.getVerbList("wait")), Entity.charList["wanda"].name, scene_3.time + "inf1a")
    lookup.append([scene_3.time + "inf1a", Entity.charList["maddie"].name, "action"])

    Entity.charList["peggy"].hasAction(("wait", WordNet.getVerbList("wait")), Entity.charList["wanda"].name, scene_3.time + "inf1b")
    lookup.append([scene_3.time + "inf1b", Entity.charList["peggy"].name, "action"])

    Entity.charList["wanda"].hasState(("absent", WordNet.getVerbList("absent")), scene_3.time + "inf2")
    lookup.append([scene_3.time + "inf2", Entity.charList["wanda"].name, "state"])

    Entity.charList["peggy"].hasDesire(("bully", WordNet.getVerbList("bully")), Entity.charList["wanda"].name, scene_3.time + "ev2")
    lookup.append([scene_3.time + "ev2", Entity.charList["peggy"].name, "desire"])

    relations.causedBy(scene_3.time + "ev1a", [scene_3.time + "inf1a", scene_3.time + "inf2"])
    relations.causedBy(scene_3.time + "ev1b", [scene_3.time + "inf1b", scene_3.time + "inf2"])
    relations.causedBy(scene_3.time + "inf1a", scene_3.time + "ev2")
    relations.causedBy(scene_3.time + "inf1b", scene_3.time + "ev2")
    ####

    ####
    Entity.charList["peggy"].hasLocation(Entity.locList["front row"], ("sit", WordNet.getVerbList("sit")), scene_3.time + "inf4")
    lookup.append([scene_3.time + "inf4", Entity.charList["peggy"].name, "location"])

    Entity.charList["maddie"].hasLocation(Entity.locList["front row"], ("sit", WordNet.getVerbList("sit")), scene_3.time + "inf5")
    lookup.append([scene_3.time + "inf5", Entity.charList["maddie"].name, "location"])

    mad_grades, mad_shoes = Rule.assignPropBySeating(Entity.charList["maddie"], scene_3.time + "inf6")
    lookup.append([scene_3.time + "inf6", Entity.charList["maddie"].name, "attribute"])

    lookup.append([scene_3.time + "inf6aext", mad_grades.name, "perProperty"])
    lookup.append([scene_3.time + "inf6bext", mad_shoes.name, "appProperty"])

    peg_grades, peg_shoes = Rule.assignPropBySeating(Entity.charList["peggy"], scene_3.time + "inf7")
    lookup.append([scene_3.time + "inf7", Entity.charList["peggy"].name, "attribute"])

    lookup.append([scene_3.time + "inf6aext", peg_grades.name, "perProperty"])
    lookup.append([scene_3.time + "inf6bext", peg_shoes.name, "appProperty"])

    Entity.charList["peggy"].hasAppProperty(["pretty"], scene_3.time + "inf8")
    lookup.append([scene_3.time + "inf8", Entity.charList["peggy"].name, "appProperty"])

    Entity.charList["peggy"].hasAttribute(peg_clothes, ("wear", WordNet.getVerbList("wear")), scene_3.time + "inf9")
    lookup.append([scene_3.time + "inf9", Entity.charList["peggy"].name, "attribute"])

    peg_clothes.hasAppProperty(["pretty"], scene_3.time + "inf9ext")
    lookup.append([scene_3.time + "inf9ext", peg_clothes.name, "appProperty"])

    Entity.charList["peggy"].hasAttribute(mad_clothes, ("wear", WordNet.getVerbList("wear")), scene_3.time + "inf11")
    lookup.append([scene_3.time + "inf11", Entity.charList["peggy"].name, "attribute"])

    mad_clothes.hasAmtProperty("many", scene_3.time + "inf11ext")
    lookup.append([scene_3.time + "inf11ext", mad_clothes.name, "amtProperty"])

    Entity.charList["peggy"].hasPerProperty("popular", scene_3.time + "inf10")
    lookup.append([scene_3.time + "inf10", Entity.charList["peggy"].name, "perProperty"])

    relations.causedBy(scene_3.time + "inf10", [scene_3.time + "inf8", scene_3.time + "inf9"])
    ####


def startScene4():
    scene_4.hasLocation([Entity.locList["school"], Entity.locList["room 13"]])
    scene_4.hasCharacter(
        [Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"], Entity.charList["townspeople"],
         Entity.charList["svenson"]])

    ####
    Entity.charList["wanda"].hasLocation(Entity.locList["frame house"], ("live", WordNet.getVerbList("live")), scene_4.time + "ev1")
    lookup.append([scene_4.time + "ev1", Entity.charList["wanda"].name, "location"])

    Rule.checkIfPersonIsPoor(Entity.charList["wanda"], scene_4.time + "inf2")
    lookup.append([scene_4.time + "inf2", Entity.charList["wanda"].name, "perProperty"])

    relations.causedBy(scene_4.time + "ev1", scene_4.time + "inf2")
    ####

    ####
    Entity.charList["wanda"].hasAttribute(Entity.itemList["mother"], ("have", WordNet.getVerbList("have")), scene_4.time + "inf3")
    lookup.append([scene_4.time + "inf3", Entity.charList["wanda"].name, "attribute"])

    Entity.itemList["mother"].hasAmtProperty("no", scene_4.time + "inf3ext")
    lookup.append([scene_4.time + "inf3ext", Entity.itemList["mother"].name, "amtProperty"])

    Entity.charList["svenson"].hasLocation(Entity.locList["svenson's house"], ("live", WordNet.getVerbList("live")), scene_4.time + "inf6")
    lookup.append([scene_4.time + "inf6", Entity.charList["svenson"].name, "location"])

    Entity.locList["svenson's house"].hasAppProperty(["yellow"], scene_4.time + "inf6ext")
    lookup.append([scene_4.time + "inf6ext", Entity.locList["svenson's house"].name, "appProperty"])

    Entity.charList["townspeople"].hasAction(("avoid", WordNet.getVerbList("avoid")), Entity.locList["svenson's house"].name, scene_4.time + "inf4")
    lookup.append([scene_4.time + "inf4", Entity.charList["townspeople"].name, "action"])

    Entity.charList["townspeople"].hasAction(("gossip about", WordNet.getVerbList("gossip")), Entity.charList["svenson"].name, scene_4.time + "inf5")
    lookup.append([scene_4.time + "inf5", Entity.charList["townspeople"].name, "action"])

    relations.causedBy(scene_4.time + "inf4", scene_4.time + "inf5")
    ####


def startScene5():
    scene_5.hasLocation([Entity.locList["school"], Entity.locList["room 13"]])
    scene_5.hasCharacter(
        [Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"], Entity.charList["girls"]])

    ####
    Entity.charList["wanda"].hasAttribute(wan_name, ("have", WordNet.getVerbList("have")), scene_5.time + "inf1")
    lookup.append([scene_5.time + "inf1", Entity.charList["wanda"].name, "attribute"])

    wan_name.hasPerProperty(["weird", "not easy to say"], scene_5.time + "inf1ext")
    lookup.append([scene_5.time + "inf1ext", wan_name.name, "perProperty"])

    relations.causedBy(scene_1.time + "inf1", scene_5.time + "inf1")
    ####

    ####
    Entity.charList["wanda"].hasAttribute(wan_dress, ("wear", WordNet.getVerbList("wear")), scene_5.time + "inf2")
    lookup.append([scene_5.time + "inf2", Entity.charList["wanda"].name, "attribute"])

    wan_dress.hasAppProperty(["blue", "not ironed properly"], scene_5.time + "inf2ext")
    lookup.append([scene_5.time + "inf2ext", wan_dress.name, "appProperty"])

    relations.causedBy(scene_5.time + "inf2", scene_4.time + "inf3")
    ####

    ####
    Entity.charList["girls"].hasLocation(Entity.locList["oliver street"], ("wait", WordNet.getVerbList("wait")), scene_5.time + "ev1")
    lookup.append([scene_5.time + "ev1", Entity.charList["girls"].name, "location"])

    Entity.charList["girls"].hasDesire(("bully", WordNet.getVerbList("bully")), Entity.charList["wanda"].name, scene_5.time + "ev2")
    lookup.append([scene_5.time + "ev2", Entity.charList["girls"].name, "desire"])

    relations.causedBy(scene_5.time + "ev1", scene_5.time + "ev2")
    relations.causedBy(scene_5.time + "ev2", [scene_5.time + "inf1", scene_5.time + "inf2", scene_1.time + "inf3"])
    ####

    ####
    Entity.charList["wanda"].hasAction(("say", WordNet.getVerbList("say")), "something", scene_5.time + "ev3")
    lookup.append([scene_5.time + "ev3", Entity.charList["wanda"].name, "action"])

    Entity.charList["wanda"].hasAttribute(Entity.itemList["100 dresses"], ("have", WordNet.getVerbList("have")), scene_5.time + "ev5")
    lookup.append([scene_5.time + "ev5", Entity.charList["wanda"].name, "attribute"])

    relations.elaborationFor(scene_5.time + "ev3", scene_5.time + "ev5")

    Entity.charList["girls"].hasAction(("not believe", WordNet.getVerbList("believe", negator="not")), "Wanda's statement", scene_5.time + "ev4")
    lookup.append([scene_5.time + "ev4", Entity.charList["girls"].name, "action"])

    relations.elaborationFor(scene_5.time + "ev4", scene_5.time + "ev5")

    relations.causedBy(scene_5.time + "ev2", scene_5.time + "ev4")
    ####


def startScene6():
    scene_6.hasLocation([Entity.locList["school"], Entity.locList["room 13"]])
    scene_6.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["girls"]])

    ####
    Entity.charList["maddie"].hasState(("guilty", WordNet.getAdjList("guilty")), scene_6.time + "ev1")
    lookup.append([scene_6.time + "ev1", Entity.charList["maddie"].name, "state"])

    relations.causedBy(scene_6.time + "ev1", scene_5.time + "ev2")
    ####

    ####
    Entity.charList["maddie"].hasPerProperty("poor", scene_6.time + "inf1")
    lookup.append([scene_6.time + "inf1", Entity.charList["maddie"].name, "perProperty"])

    Entity.charList["maddie"].hasAttribute(mad_clothes, ("wear", WordNet.getVerbList("wear")), scene_6.time + "inf2")
    lookup.append([scene_6.time + "inf2", Entity.charList["maddie"].name, "attribute"])

    mad_clothes.hasPerProperty("peggy's hand-me-down", scene_6.time + "inf2ext")
    lookup.append([scene_6.time + "inf2ext", mad_clothes.name, "perProperty"])

    Entity.charList["maddie"].hasAction(("sympathize", WordNet.getVerbList("sympathize")), Entity.charList["wanda"].name,
                                        scene_6.time + "ev2")
    lookup.append([scene_6.time + "ev2", Entity.charList["maddie"].name, "action"])

    relations.causedBy(scene_6.time + "ev1", scene_6.time + "ev2")
    relations.causedBy(scene_6.time + "ev2", [scene_6.time + "inf1", scene_6.time + "inf2"])
    ####

    ####
    Entity.charList["girls"].hasAction(("not bully", WordNet.getVerbList("bully", negator="not")), Entity.charList["maddie"].name,
                                       scene_6.time + "ev3")
    lookup.append([scene_6.time + "ev3", Entity.charList["girls"].name, "action"])

    Entity.charList["maddie"].hasAttribute(mad_name, ("have", WordNet.getVerbList("have")), scene_6.time + "inf3")
    lookup.append([scene_6.time + "inf3", Entity.charList["maddie"].name, "attribute"])

    mad_name.hasPerProperty(["not weird", "not hard to say"], scene_6.time + "inf3ext")
    lookup.append([scene_6.time + "inf3ext", mad_name.name, "perProperty"])

    Entity.charList["maddie"].hasLocation("Boggins Heights", ("not live", WordNet.getVerbList("live", negator="not")), scene_6.time + "inf4")
    lookup.append([scene_6.time + "inf4", Entity.charList["maddie"].name, "location"])

    relations.causedBy(scene_6.time + "ev3", [scene_6.time + "inf3", scene_6.time + "inf4"])
    ####

    ####
    Entity.charList["maddie"].hasState(("guilty", WordNet.getAdjList("guilty")), scene_6.time + "ev4")
    lookup.append([scene_6.time + "ev4", Entity.charList["maddie"].name, "state"])

    Entity.charList["maddie"].hasAction(("not defend", WordNet.getVerbList("defend", negator="not")), Entity.charList["wanda"].name,
                                        scene_6.time + "inf5")
    lookup.append([scene_6.time + "inf5", Entity.charList["maddie"].name, "action"])

    relations.causedBy(scene_6.time + "ev4", scene_6.time + "inf5")
    ####


def startScene7():
    scene_7.hasLocation([Entity.locList["school"], Entity.locList["room 13"]])
    scene_7.hasCharacter(
        [Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["cecile"], Entity.charList["peggy"],
         Entity.charList["girls"]])

    ####
    Entity.charList["maddie"].hasState(("troubled", WordNet.getAdjList("troubled")), scene_7.time + "ev1")
    lookup.append([scene_7.time + "ev1", Entity.charList["maddie"].name, "state"])

    relations.causedBy(scene_7.time + "ev1", [scene_3.time + "ev1a", scene_6.time + "ev1"])
    ####

    ####
    Entity.charList["maddie"].hasAction(("think", WordNet.getVerbList("think")), Entity.charList["wanda"].name,
                                        scene_7.time + "ev2")
    lookup.append([scene_7.time + "ev2", Entity.charList["maddie"].name, "action"])

    Entity.charList["maddie"].hasAction(("think", WordNet.getVerbList("think")), Entity.itemList["dresses game"].name, scene_7.time + "ev3")
    lookup.append([scene_7.time + "ev3", Entity.charList["maddie"].name, "action"])

    relations.causedBy(scene_7.time + "ev1", [scene_7.time + "ev2", scene_7.time + "ev3"])
    ####

    ####
    Entity.itemList["dresses game"].hasState(("start", WordNet.getAdjList("start")), scene_7.time + "ev4")
    lookup.append([scene_7.time + "ev4", Entity.itemList["dresses game"].name, "state"])

    Entity.charList["cecile"].hasAction(("wear", WordNet.getVerbList("wear")), cec_clothes, scene_7.time + "ev5")
    cec_clothes.hasAppProperty(["pretty", "red"], scene_7.time + "ev5ext")

    lookup.append([scene_7.time + "ev5", Entity.charList["cecile"].name, "action"])
    lookup.append([scene_7.time + "ev5ext", cec_clothes.name, "appProperty"])

    Entity.charList["girls"].hasAction(("admire", WordNet.getVerbList("admire")), Entity.charList["cecile"].name,scene_7.time + "ev6")
    lookup.append([scene_7.time + "ev6", Entity.charList["girls"].name, "action"])

    Entity.charList["cecile"].hasAttribute(cec_clothes, ("wear", WordNet.getVerbList("wear")), scene_7.time + "inf1")
    lookup.append([scene_7.time + "inf1", Entity.charList["cecile"].name, "attribute"])

    cec_clothes.hasAppProperty(["prettier than others"], scene_7.time + "inf1ext")
    lookup.append([scene_7.time + "inf1ext", cec_clothes.name, "appProperty"])

    Entity.charList["cecile"].hasAppProperty(["tall", "slender"], scene_7.time + "inf2")
    lookup.append([scene_7.time + "inf2", Entity.charList["cecile"].name, "appProperty"])

    relations.causedBy(scene_7.time + "ev4", [scene_7.time + "ev5", scene_7.time + "ev6"])
    relations.causedBy(scene_7.time + "ev6", [scene_7.time + "inf1", scene_7.time + "inf2"])
    ####

    ####
    Entity.charList["wanda"].hasDesire(("join", WordNet.getVerbList("join")), Entity.charList["girls"].name, scene_7.time + "ev8")
    lookup.append([scene_7.time + "ev8", Entity.charList["wanda"].name, "desire"])

    relations.causedBy(scene_5.time + "ev3", scene_7.time + "ev8")

    Entity.charList["peggy"].hasAction(("tease", WordNet.getVerbList("tease")), Entity.charList["wanda"].name,
                                       scene_7.time + "ev9")
    lookup.append([scene_7.time + "ev9", Entity.charList["peggy"].name, "action"])

    relations.causedBy(scene_7.time + "ev9", scene_5.time + "ev3")
    ####


def startScene8():
    scene_8.hasLocation([Entity.locList["school"], Entity.locList["room 13"]])
    scene_8.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"]])

    relations = Rel.Relations("Relation for Scene 8")

    ####
    Entity.charList["maddie"].hasDesire(("wish", WordNet.getVerbList("wish")), "stop " + Entity.charList["peggy"].name, scene_8.time + "ev1")
    lookup.append([scene_8.time + "ev1", Entity.charList["maddie"].name, "desire"])

    Entity.charList["peggy"].hasAction(("bully", WordNet.getVerbList("bully")), Entity.charList["wanda"].name,
                                       scene_8.time + "ev1a")
    lookup.append([scene_8.time + "ev1a", Entity.charList["peggy"].name, "action"])

    relations.causedBy(scene_8.time + "ev1", scene_8.time + "ev1a")

    Entity.charList["maddie"].hasAction(("write", WordNet.getVerbList("write")), Entity.itemList["note"].name,
                                        scene_8.time + "ev2")
    lookup.append([scene_8.time + "ev2", Entity.charList["maddie"].name, "action"])

    relations.causedBy(scene_8.time + "ev2", scene_8.time + "ev1")
    ####

    ####
    Entity.charList["maddie"].hasAction(("destroy", WordNet.getVerbList("destroy")), Entity.itemList["note"].name, scene_8.time + "ev3")
    lookup.append([scene_8.time + "ev3", Entity.charList["maddie"].name, "action"])

    Entity.charList["maddie"].hasDesire(("not want", WordNet.getVerbList("want", negator="not")), "argue with " + Entity.charList["peggy"].name, scene_8.time + "ev4")
    lookup.append([scene_8.time + "ev4", Entity.charList["maddie"].name, "desire"])

    Entity.charList["peggy"].hasAction(("hate", WordNet.getVerbList("hate")), Entity.charList["maddie"].name, scene_8.time + "ev4a")
    lookup.append([scene_8.time + "ev4a", Entity.charList["peggy"].name, "action"])

    relations.causedBy(scene_8.time + "ev3", [scene_8.time + "ev4", scene_8.time + "ev4a"])
    ####


def startScene9():
    scene_9.hasLocation([Entity.locList["school"], Entity.locList["room 13"]])
    scene_9.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"]])

    ####
    Entity.charList["wanda"].hasAction(("struggle", WordNet.getVerbList("struggle")), "read paragraphs",
                                       scene_9.time + "ev1")

    lookup.append([scene_9.time + "ev1", Entity.charList["wanda"].name, "action"])

    Entity.charList["wanda"].hasPerProperty("timid", scene_9.time + "inf1")
    lookup.append([scene_9.time + "inf1", Entity.charList["wanda"].name, "perProperty"])

    Entity.charList["wanda"].hasPerProperty("not smart", scene_9.time + "inf2")
    lookup.append([scene_9.time + "inf2", Entity.charList["wanda"].name, "perProperty"])

    relations.causedBy(scene_9.time + "ev1", [scene_9.time + "inf1", scene_9.time + "inf2"])
    ####

    # ent.charList["wanda"].hasAction("describe", ent.itemList["dress"].hasProperty(["pale blue", "with cerise-colored trimmings"]), scene_9.time + "ev2")
    # ent.charList["wanda"].hasAction("describe", ent.itemList["dress"].hasProperty(["jungle green", "with red sash"]), scene_9.time + "ev3")

    ####
    Entity.charList["peggy"].hasPerProperty("artistic", scene_9.time + "ev2")
    lookup.append([scene_9.time + "ev2", Entity.charList["peggy"].name, "perProperty"])

    Entity.charList["maddie"].hasAction(("know", WordNet.getAdjList("know")), "winner", scene_9.time + "ev3")
    lookup.append([scene_9.time + "ev3", Entity.charList["maddie"].name, "action"])

    Entity.charList["peggy"].hasAction(("win", WordNet.getVerbList("win")), Entity.itemList["drawing contest"].name,
                                       scene_9.time + "ev4")
    lookup.append([scene_9.time + "ev4", Entity.charList["peggy"].name, "action"])

    relations.elaborationFor(scene_9.time + "ev3", [scene_9.time + "ev4", scene_9.time + "ev2"])
    ####


def startScene10():
    scene_10.hasLocation([Entity.locList["school"], Entity.locList["room 13"]])
    scene_10.hasCharacter(
        [Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"], Entity.charList["miss mason"]])

    ####
    Entity.charList["maddie"].hasState(("shocked", WordNet.getAdjList("shocked")), scene_10.time + "ev1a")
    lookup.append([scene_10.time + "ev1a", Entity.charList["maddie"].name, "state"])

    Entity.charList["peggy"].hasState(("shocked", WordNet.getAdjList("shocked")), scene_10.time + "ev1b")
    lookup.append([scene_10.time + "ev1b", Entity.charList["peggy"].name, "state"])

    Entity.locList["room 13"].hasAttribute(Entity.itemList["drawing"], ("post", WordNet.getVerbList("post")), scene_10.time + "inf1")
    lookup.append([scene_10.time + "inf1", Entity.locList["room 13"].name, "attribute"])

    Entity.itemList["drawing"].hasAmtProperty("100 pieces", scene_10.time + "inf1ext")
    lookup.append([scene_10.time + "inf1ext", Entity.itemList["drawing"].name, "amtProperty"])

    Entity.itemList["drawing"].hasAppProperty(["pretty"], scene_10.time + "inf2")
    lookup.append([scene_10.time + "inf2", Entity.itemList["drawing"].name, "appProperty"])

    relations.causedBy(scene_10.time + "ev1a", [scene_10.time + "inf1", scene_10.time + "inf2"])
    relations.causedBy(scene_10.time + "ev1b", [scene_10.time + "inf1", scene_10.time + "inf2"])
    ####

    ####
    Entity.charList["miss mason"].hasAction(("announce", WordNet.getVerbList("announce")), "winner", scene_10.time + "ev2")
    lookup.append([scene_10.time + "ev2", Entity.charList["miss mason"].name, "action"])

    Entity.charList["wanda"].hasAction(("win", WordNet.getVerbList("win")), Entity.itemList["drawing contest"].name,
                                       scene_10.time + "ev6")
    lookup.append([scene_10.time + "ev6", Entity.charList["wanda"].name, "action"])

    relations.sequence(scene_10.time + "ev2", scene_10.time + "ev6")

    Entity.charList["wanda"].hasAttribute(Entity.itemList["drawing"], ("submit", WordNet.getVerbList("submit")), scene_10.time + "ev3")
    lookup.append([scene_10.time + "ev3", Entity.charList["wanda"].name, "attribute"])
    lookup.append([scene_10.time + "ev3ext", Entity.itemList["drawing"].name, "amtProperty"])
    lookup.append([scene_10.time + "ev3ext", Entity.itemList["drawing"].name, "appProperty"])

    relations.causedBy(scene_10.time + "ev6", scene_10.time + "ev3")
    ####

    ####
    Entity.charList["wanda"].hasAction(("not receive", WordNet.getVerbList("receive", negator="not")), Entity.itemList["medal"].name,
                                       scene_10.time + "ev4")
    lookup.append([scene_10.time + "ev4", Entity.charList["wanda"].name, "action"])

    Entity.charList["wanda"].hasState(("absent", WordNet.getAdjList("absent")), scene_10.time + "ev5")
    lookup.append([scene_10.time + "ev5", Entity.charList["wanda"].name, "state"])

    relations.causedBy(scene_10.time + "ev4", scene_10.time + "ev5")
    ####


def startScene11():
    scene_11.hasLocation([Entity.locList["school"], Entity.locList["room 13"]])
    scene_11.hasCharacter([Entity.charList["wanda"], Entity.charList["students"], Entity.charList["miss mason"]])

    ####
    Entity.charList["miss mason"].hasAction(("receive", WordNet.getVerbList("receive")), Entity.itemList["note"].name, scene_11.time + "ev1")
    lookup.append([scene_11.time + "ev1", Entity.charList["miss mason"].name, "action"])

    Entity.charList["miss mason"].hasState(("serious", WordNet.getAdjList("serious")), scene_11.time + "ev2")
    lookup.append([scene_11.time + "ev2", Entity.charList["miss mason"].name, "state"])

    Entity.charList["wanda"].hasState(("hurt", WordNet.getAdjList("hurt")), scene_11.time + "inf1")
    lookup.append([scene_11.time + "inf1", Entity.charList["wanda"].name, "state"])

    Entity.itemList["note"].hasAction(("say", WordNet.getVerbList("say")), "Wanda's wherabouts", scene_11.time + "ev3")
    lookup.append([scene_11.time + "ev3", Entity.itemList["note"].name, "action"])

    Entity.charList["wanda"].hasAction(("move", WordNet.getVerbList("move")), "town", scene_11.time + "ev8")
    lookup.append([scene_11.time + "ev8", Entity.charList["wanda"].name, "action"])

    relations.sequence(scene_11.time + "ev3", scene_11.time + "ev8")

    relations.causedBy(scene_11.time + "ev3", scene_11.time + "inf1")
    relations.causedBy(scene_11.time + "inf1", scene_5.time + "ev2")
    relations.causedBy(scene_11.time + "ev2", [scene_11.time + "ev1", scene_11.time + "ev3"])
    relations.causedBy(scene_11.time + "ev3", scene_5.time + "ev2")
    ####

    ####
    Entity.charList["miss mason"].hasAction(("defend", WordNet.getVerbList("defend")), Entity.charList["students"].name,
                                            scene_11.time + "ev4")
    lookup.append([scene_11.time + "ev4", Entity.charList["miss mason"].name, "action"])

    Entity.charList["miss mason"].hasAction(("state", WordNet.getVerbList("state")), Entity.charList["students"].name + "' defense",
                                            scene_11.time + "ev6")
    lookup.append([scene_11.time + "ev6", Entity.charList["miss mason"].name, "action"])

    Entity.charList["students"].hasAction(("not want", WordNet.getVerbList("want", negator="not")),
                                          "sadden " + Entity.charList["wanda"].name, scene_11.time + "ev7")
    lookup.append([scene_11.time + "ev7", Entity.charList["students"].name, "action"])

    relations.causedBy(scene_11.time + "ev6", scene_11.time + "ev7")

    Entity.charList["miss mason"].hasAction(("talk", WordNet.getVerbList("talk")), Entity.charList["students"].name,
                                            scene_11.time + "ev5")
    lookup.append([scene_11.time + "ev5", Entity.charList["miss mason"].name, "action"])

    Entity.charList["students"].hasAction(("reflect", WordNet.getVerbList("reflect")), Entity.itemList["note"].name,
                                          scene_11.time + "ev7"),
    lookup.append([scene_11.time + "ev6", Entity.charList["students"].name, "action"])

    relations.sequence(scene_11.time + "ev5", scene_11.time + "ev7")

    relations.causedBy(scene_11.time + "ev4", scene_11.time + "ev6")
    relations.causedBy(scene_11.time + "ev5", scene_11.time + "ev3")
    ####


def startScene12():
    scene_12.hasLocation([Entity.locList["school"], Entity.locList["room 13"]])
    scene_12.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"]])

    ####
    Entity.charList["maddie"].hasState(("distracted", WordNet.getAdjList("distracted")), scene_12.time + "ev1")
    lookup.append([scene_12.time + "ev1", Entity.charList["maddie"].name, "state"])

    Entity.charList["maddie"].hasState(("feel sick", WordNet.getAdjList("sick")), scene_12.time + "ev2")
    lookup.append([scene_12.time + "ev2", Entity.charList["maddie"].name, "state"])

    relations.causedBy(scene_11.time + "ev3", [scene_12.time + "ev1", scene_12.time + "ev2"])
    ####

    ####
    Entity.charList["maddie"].hasAction(("not defend", WordNet.getVerbList("defend", negator="not")), Entity.charList["wanda"].name, scene_12.time + "ev4")
    lookup.append([scene_12.time + "ev4", Entity.charList["maddie"].name, "action"])

    Entity.charList["maddie"].hasAction(("sorry", WordNet.getAdjList("sorry")), "actions", scene_12.time + "ev5")
    lookup.append([scene_12.time + "ev5", Entity.charList["maddie"].name, "action"])

    relations.causedBy(scene_12.time + "ev5", scene_11.time + "ev4")

    Entity.charList["maddie"].hasAction(("not condone", WordNet.getVerbList("condone", negator="not")), "bullying", scene_12.time + "inf1")
    lookup.append([scene_12.time + "inf1", Entity.charList["maddie"].name, "action"])

    relations.contradiction(scene_12.time + "ev5", scene_12.time + "ev4")
    relations.causedBy(scene_12.time + "ev4", scene_8.time + "ev4")
    relations.causedBy([scene_12.time + "ev1", scene_12.time + "ev2"], scene_12.time + "ev4")
    relations.causedBy(scene_12.time + "inf1", scene_11.time + "inf1")
    ####


def startScene13():
    scene_13.hasLocation([Entity.locList["school"], Entity.locList["room 13"]])
    scene_13.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"]])

    ####
    Entity.charList["maddie"].hasDesire(("apologize", WordNet.getVerbList("apologize")), Entity.charList["wanda"].name, scene_13.time + "ev1")
    lookup.append([scene_13.time + "ev1", Entity.charList["maddie"].name, "desire"])

    Entity.charList["maddie"].hasDesire(("visit", WordNet.getVerbList("visit")), Entity.charList["wanda"].name, scene_13.time + "ev2")
    lookup.append([scene_13.time + "ev2", Entity.charList["maddie"].name, "desire"])

    relations.causedBy(scene_13.time + "ev2", scene_13.time + "ev1")
    relations.causedBy(scene_13.time + "ev1", [scene_6.time + "ev1", scene_12.time + "ev5"])
    ####

    ####
    Entity.charList["peggy"].hasAction(("say", WordNet.getVerbList("say")), "request", scene_13.time + "ev3")
    lookup.append([scene_13.time + "ev3", Entity.charList["peggy"].name, "action"])

    Entity.charList["peggy"].hasDesire(("visit", WordNet.getVerbList("visit")), Entity.charList["wanda"].name, scene_13.time),
    lookup.append([scene_13.time, Entity.charList["peggy"].name, "desire"])

    relations.sequence(scene_13.time + "ev3", scene_13.time)

    Entity.charList["maddie"].hasState(("overjoyed", WordNet.getAdjList("overjoyed")), scene_13.time + "ev5")
    lookup.append([scene_13.time + "ev5", Entity.charList["maddie"].name, "state"])

    relations.causedBy(scene_13.time + "ev5", [scene_13.time + "ev3", scene_13.time + "ev2"])
    ####


def startScene14():
    scene_14.hasLocation([Entity.locList["school"], Entity.locList["boggins heights"]])
    scene_14.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"]])

    ####
    Entity.charList["maddie"].hasDesire(("go back", WordNet.getVerbList("go_back")), "time", scene_14.time + "ev1")
    lookup.append([scene_14.time + "ev1", Entity.charList["maddie"].name, "desire"])

    Entity.itemList["dresses game"].hasState(("not exist", WordNet.getVerbList("exist", negator="not")), scene_14.time + "inf1")
    lookup.append([scene_14.time + "inf1", Entity.itemList["dresses game"].name, "state"])

    relations.causedBy(scene_14.time + "ev1", scene_14.time + "inf1")
    relations.causedBy(scene_14.time + "inf1", scene_11.time + "ev3")
    ####

    ####
    Entity.charList["peggy"].hasAction(("avoid", WordNet.getVerbList("avoid")), Entity.locList["svenson's house"].name, scene_14.time + "ev5")
    lookup.append([scene_14.time + "ev5", Entity.charList["peggy"].name, "action"])

    Entity.charList["maddie"].hasAction(("avoid", WordNet.getVerbList("avoid")), Entity.locList["svenson's house"].name, scene_14.time + "ev6")
    lookup.append([scene_14.time + "ev6", Entity.charList["maddie"].name, "action"])

    Entity.charList["peggy"].hasDesire(("not meet", WordNet.getVerbList("meet", negator="not")), Entity.charList["svenson"].name, scene_14.time + "ev7")
    lookup.append([scene_14.time + "ev7", Entity.charList["peggy"].name, "desire"])

    Entity.charList["maddie"].hasDesire(("not meet", WordNet.getVerbList("meet", negator="not")), Entity.charList["svenson"].name, scene_14.time + "ev8")
    lookup.append([scene_14.time + "ev8", Entity.charList["maddie"].name, "desire"])

    relations.causedBy(scene_14.time + "ev5", scene_14.time + "ev7")
    relations.causedBy(scene_14.time + "ev6", scene_14.time + "ev8")
    relations.causedBy(scene_14.time + "ev7", scene_4.time + "inf5")
    relations.causedBy(scene_14.time + "ev8", scene_4.time + "inf5")
    ####

    ####
    Entity.charList["maddie"].hasState(("worry", WordNet.getVerbList("worry")), scene_14.time + "ev9")
    lookup.append([scene_14.time + "ev9", Entity.charList["maddie"].name, "state"])

    Entity.charList["maddie"].hasAction(("might not meet", WordNet.getVerbList("meet", negator="might not")), Entity.charList["wanda"].name, scene_14.time + "inf3")
    lookup.append([scene_14.time + "inf3", Entity.charList["maddie"].name, "action"])

    Entity.charList["maddie"].hasAction(("might not apologize", WordNet.getVerbList("apologize", negator="might not")), Entity.charList["wanda"].name, scene_14.time + "inf1")
    lookup.append([scene_14.time + "inf1", Entity.charList["maddie"].name, "action"])

    relations.causedBy(scene_14.time + "ev9", scene_14.time + "inf3")
    relations.causedBy(scene_14.time + "inf1", scene_14.time + "inf3")
    ####


def startScene15():
    scene_15.hasLocation([Entity.locList["school"], Entity.locList["boggins heights"]])
    scene_15.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"]])

    ####
    Entity.charList["peggy"].hasState((["downcast", "discouraged"], [WordNet.getAdjList("downcast"), WordNet.getAdjList("discouraged")]), scene_15.time + "ev1")
    lookup.append([scene_15.time + "ev1", Entity.charList["peggy"].name, "state"])

    Entity.charList["maddie"].hasState((["downcast", "discouraged"], [WordNet.getAdjList("downcast"), WordNet.getAdjList("discouraged")]), scene_15.time + "ev2")
    lookup.append([scene_15.time + "ev2", Entity.charList["maddie"].name, "state"])

    Entity.locList["frame house"].hasPerProperty(("empty", WordNet.getAdjList("empty")), scene_15.time + "inf1")
    lookup.append([scene_15.time + "inf1", Entity.locList["frame house"].name, "state"])

    Entity.charList["peggy"].hasAction(("not meet", WordNet.getVerbList("meet", negator="not")), Entity.charList["wanda"].name, scene_15.time + "ev3")
    lookup.append([scene_15.time + "ev3", Entity.charList["peggy"].name, "action"])

    Entity.charList["maddie"].hasAction(("not meet", WordNet.getVerbList("meet", negator="not")), Entity.charList["wanda"].name, scene_15.time + "ev4")
    lookup.append([scene_15.time + "ev4", Entity.charList["maddie"].name, "action"])

    relations.causedBy(scene_15.time + "ev1", [scene_15.time + "inf1", scene_15.time + "ev3"])
    relations.causedBy(scene_15.time + "ev2", [scene_15.time + "inf1", scene_15.time + "ev4"])
    ####

    ####
    Entity.charList["peggy"].hasAction(("write", WordNet.getVerbList("write")), Entity.itemList["friendly letter"].name, scene_15.time + "ev5")
    lookup.append([scene_15.time + "ev5", Entity.charList["peggy"].name, "action"])

    Entity.charList["maddie"].hasAction(("write", WordNet.getVerbList("write")), Entity.itemList["friendly letter"].name, scene_15.time + "ev6")
    lookup.append([scene_15.time + "ev6", Entity.charList["maddie"].name, "action"])

    Entity.charList["peggy"].hasDesire(("apologize", WordNet.getVerbList("apologize")), Entity.charList["wanda"].name, scene_15.time + "ev7")
    lookup.append([scene_15.time + "ev7", Entity.charList["peggy"].name, "desire"])

    Entity.charList["maddie"].hasDesire(("apologize", WordNet.getVerbList("apologize")), Entity.charList["wanda"].name, scene_15.time + "ev8")
    lookup.append([scene_15.time + "ev8", Entity.charList["maddie"].name, "desire"])

    relations.causedBy(scene_15.time + "ev5", [scene_15.time + "ev3", scene_15.time + "ev7"])
    relations.causedBy(scene_15.time + "ev6", [scene_15.time + "ev4", scene_15.time + "ev8"])
    ####


def startScene16():
    scene_16.hasLocation([Entity.locList["school"], Entity.locList["room 13"]])
    scene_16.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"]])

    ####
    Entity.charList["peggy"].hasState((["carefree", "happy"], [WordNet.getAdjList("carefree"), WordNet.getAdjList("happy")]), scene_16.time + "ev1")
    lookup.append([scene_16.time + "ev1", Entity.charList["peggy"].name, "state"])

    Entity.charList["maddie"].hasState((["carefree", "happy"], [WordNet.getAdjList("carefree"), WordNet.getAdjList("happy")]), scene_16.time + "ev2")
    lookup.append([scene_16.time + "ev2", Entity.charList["maddie"].name, "state"])

    Entity.charList["peggy"].hasAction(("send", WordNet.getVerbList("send")), Entity.itemList["friendly letter"].name, scene_16.time + "ev3")
    lookup.append([scene_16.time + "ev3", Entity.charList["peggy"].name, "action"])

    Entity.charList["maddie"].hasAction(("send", WordNet.getVerbList("send")), Entity.itemList["friendly letter"].name, scene_16.time + "ev4")
    lookup.append([scene_16.time + "ev4", Entity.charList["maddie"].name, "action"])

    Entity.charList["peggy"].hasAction(("reconcile", WordNet.getVerbList("reconcile")), Entity.charList["wanda"].name, scene_16.time + "ev5")
    lookup.append([scene_16.time + "ev5", Entity.charList["peggy"].name, "action"])

    Entity.charList["maddie"].hasAction(("reconcile", WordNet.getVerbList("reconcile")), Entity.charList["wanda"].name, scene_16.time + "ev6")
    lookup.append([scene_16.time + "ev6", Entity.charList["maddie"].name, "action"])

    relations.causedBy(scene_16.time + "ev1", scene_16.time + "ev3")
    relations.causedBy(scene_16.time + "ev2", scene_16.time + "ev4")
    relations.consequence(scene_16.time + "ev3", [scene_16.time + "ev5", scene_15.time + "ev7"])
    relations.consequence(scene_16.time + "ev4", [scene_16.time + "ev6", scene_15.time + "ev8"])
    ####

    ####
    Entity.charList["peggy"].hasAction(("understand", WordNet.getVerbList("understand")), Entity.charList["wanda"].name, scene_16.time + "ev7")
    lookup.append([scene_16.time + "ev7", Entity.charList["peggy"].name, "action"])

    Entity.charList["maddie"].hasAction(("understand", WordNet.getVerbList("understand")), Entity.charList["wanda"].name, scene_16.time + "ev8")
    lookup.append([scene_16.time + "ev8", Entity.charList["maddie"].name, "action"])

    Entity.charList["wanda"].hasAttribute(wan_dress, ("have", WordNet.getVerbList("have")), scene_16.time + "inf1")
    lookup.append([scene_16.time + "inf1", Entity.charList["wanda"].name, "attribute"])

    wan_dress.hasAmtProperty("only one", scene_16.time + "inf1ext")
    lookup.append([scene_16.time + "inf1ext", wan_dress.name, "amtProperty"])
    # ent.charList["wanda"].hasAction("iron", ent.itemList["clothes"], scene_16.time + "inf2")

    relations.causedBy(scene_16.time + "ev7", scene_16.time + "inf1")
    relations.causedBy(scene_16.time + "ev8", scene_16.time + "inf1")
    relations.causedBy(scene_16.time + "inf1", scene_4.time + "inf2")
    relations.causedBy(scene_5.time + "inf2", scene_16.time + "inf1")
    # relations.causedBy(startScene5.scene_5.time + "inf2", startScene4.scene_4.time + "inf3")
    # relations.causedBy(scene_16.time + "inf1", startScene5.scene_5.time + "inf2")
    ####


def startScene17():
    scene_17.hasLocation([Entity.locList["school"], Entity.locList["room 13"]])
    scene_17.hasCharacter(
        [Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"], Entity.charList["miss mason"]])

    ####
    Entity.charList["miss mason"].hasAction(("receive", WordNet.getVerbList("receive")), Entity.itemList["letter"], scene_17.time + "ev1")
    lookup.append([scene_17.time + "ev1", Entity.charList["miss mason"].name, "action"])

    Entity.itemList["letter"].hasPerProperty("from Wanda", scene_17.time + "ev1ext")
    lookup.append([scene_17.time + "ev1ext", Entity.itemList["letter"].name, "perProperty"])

    Entity.charList["miss mason"].hasAction(("know", WordNet.getVerbList("know")), Entity.charList["wanda"].name + " new house", scene_17.time + "inf1")
    lookup.append([scene_17.time + "inf1", Entity.charList["miss mason"].name, "action"])

    Entity.charList["miss mason"].hasAction(("can send", WordNet.getVerbList("send", negator="can")), Entity.itemList["medal"].name, scene_17.time + "ev2")
    lookup.append([scene_17.time + "ev2", Entity.charList["miss mason"].name, "action"])

    relations.consequence(scene_17.time + "ev1", scene_17.time + "inf1")
    relations.consequence(scene_17.time + "inf1", scene_17.time + "ev2")
    relations.causedBy(scene_17.time + "ev2", scene_10.time + "ev4")
    ####

    ####
    Entity.charList["wanda"].hasAction(("forgive", WordNet.getVerbList("forgive")), [Entity.charList["peggy"].name, Entity.charList["maddie"].name], scene_17.time + "ev3")
    lookup.append([scene_17.time + "ev3", Entity.charList["wanda"].name, "action"])

    Entity.charList["wanda"].hasAction(("give", WordNet.getVerbList("give")), giv_mad_dress, scene_17.time + "ev4")
    lookup.append([scene_17.time + "ev4", Entity.charList["wanda"].name, "action"])

    giv_mad_dress.hasAppProperty(["pale blue", "with cerise-colored trimmings"], scene_17.time + "ev4ext")
    lookup.append([scene_17.time + "ev4ext", giv_mad_dress.name, "appProperty"])

    Entity.charList["wanda"].hasAction(("give", WordNet.getVerbList("give")), giv_peg_dress, scene_17.time + "ev5")
    lookup.append([scene_17.time + "ev5", Entity.charList["wanda"].name, "action"])

    giv_peg_dress.hasAppProperty(["jungle green", "with red sash"], scene_17.time + "ev5ext")
    lookup.append([scene_17.time + "ev5", giv_peg_dress.name, "appProperty"])

    Entity.charList["wanda"].hasAction(("receive", WordNet.getVerbList("receive")), Entity.itemList["friendly letter"].name, scene_17.time + "ev6")
    lookup.append([scene_17.time + "ev6", Entity.charList["wanda"].name, "action"])

    relations.contradiction(scene_17.time + "ev3", scene_5.time + "ev2")
    relations.causedBy([scene_17.time + "ev4", scene_17.time + "ev5"], scene_17.time + "ev3")
    relations.causedBy(scene_17.time + "ev3", scene_17.time + "ev6")
    relations.causedBy(scene_17.time + "ev6", [scene_16.time + "ev3", scene_16.time + "ev4"])
    ####


def startScene18():
    scene_18.hasLocation([Entity.locList["school"], Entity.locList["room 13"]])
    scene_18.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"]])

    ####
    Entity.charList["maddie"].hasState(("sad", WordNet.getAdjList("sad")), scene_18.time + "ev1")
    lookup.append([scene_18.time + "ev1", Entity.charList["maddie"].name, "state"])

    Entity.charList["peggy"].hasState(("not guilty", WordNet.getAdjList("guilty", negator="not")), scene_18.time + "ev2")
    lookup.append([scene_18.time + "ev2", Entity.charList["peggy"].name, "state"])

    relations.causedBy(scene_18.time + "ev1", scene_17.time + "ev4")
    relations.causedBy(scene_18.time + "ev2", scene_17.time + "ev5")
    ####

    ####
    Entity.charList["maddie"].hasState(("cry", WordNet.getVerbList("cry")), scene_18.time + "ev3")
    lookup.append([scene_18.time + "ev3", Entity.charList["maddie"].name, "state"])

    relations.causedBy(scene_18.time + "ev3", [scene_6.time + "inf5", scene_17.time + "ev3"])
    ####

    ####
    Entity.charList["peggy"].hasAction(("understand", WordNet.getVerbList("understand")), Entity.itemList["100 dresses"].name, scene_18.time + "ev4")
    lookup.append([scene_18.time + "ev4", Entity.charList["peggy"].name, "action"])

    Entity.charList["maddie"].hasAction(("understand", WordNet.getVerbList("understand")), Entity.itemList["100 dresses"].name, scene_18.time + "ev5")
    lookup.append([scene_18.time + "ev5", Entity.charList["maddie"].name, "action"])

    relations.causedBy(scene_18.time + "ev4", scene_10.time + "ev3")
    relations.causedBy(scene_18.time + "ev5", scene_10.time + "ev3")
    ####


def queryLookup(event):
    count = [lookup.index(x) for x in lookup if x[0] == event][0]
    return lookup[count]


def queryRelations(event, relType):
    if relType == "cause":
        for entries in relations.causeList:
            a, b = entries

            if type(a) is str and a == event:
                return b

            elif type(a) is list:
                for items in a:
                    if items == event:
                        return b

    return None


def executeAll():
    startScene1()
    startScene2()
    startScene3()
    startScene4()
    startScene5()
    startScene6()
    startScene7()
    startScene8()
    startScene9()
    startScene10()
    startScene11()
    startScene12()
    startScene13()
    startScene14()
    startScene15()
    startScene16()
    startScene17()
    startScene18()
