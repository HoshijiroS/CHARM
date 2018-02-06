import model.Relations as rel
import model.Scene as scene
import model.story_world.Entities as ent
import model.story_world.Rules as rule

lookup = []

scene_1 = scene.Scene("Scene 1", "Monday")
scene_2 = scene.Scene("Scene 2", "Tuesday")
scene_3 = scene.Scene("Scene 3", "Wednesday")
scene_4 = scene.Scene("Scene 4", "Wednesday")
scene_5 = scene.Scene("Scene 5", "Wednesday")
scene_6 = scene.Scene("Scene 6", "Wednesday")
scene_7 = scene.Scene("Scene 7", "Wednesday")
scene_8 = scene.Scene("Scene 8", "Wednesday")
scene_9 = scene.Scene("Scene 9", "Wednesday")
scene_10 = scene.Scene("Scene 10", "Thursday")
scene_11 = scene.Scene("Scene 11", "Thursday")
scene_12 = scene.Scene("Scene 12", "Thursday")
scene_13 = scene.Scene("Scene 13", "Thursday")
scene_14 = scene.Scene("Scene 14", "Thursday")
scene_15 = scene.Scene("Scene 15", "Thursday")
scene_16 = scene.Scene("Scene 16", "Friday")
scene_17 = scene.Scene("Scene 17", "Christmas Time")
scene_18 = scene.Scene("Scene 18", "Christmas Time")


def startScene1():
    scene_1.hasLocation([ent.locList["school"], ent.locList["rm13"]])
    scene_1.hasCharacter([ent.charList["wanda"], ent.charList["students"]])

    rel_for_sc_1 = rel.Relations("Relation for Scene 1")

    ####
    ent.charList["students"].hasAction(rule.getVerbList("notice", negator="not"), ent.charList["wanda"].name,
                                       scene_1.time + "ev1")
    lookup.append([scene_1.time + "ev1", ent.charList["students"].name, "action"])

    ent.charList["wanda"].hasState(rule.getAdjList("absent"), scene_1.time)
    lookup.append([scene_1.time, ent.charList["wanda"].name, "state"])

    rel_for_sc_1.causedBy(scene_1.time + "ev1", scene_1.time)

    ent.charList["wanda"].hasAttribute(ent.itemList["friend"], rule.getVerbList("have"),
                                       scene_1.time + "inf1").hasProperty("no", scene_1.time + "inf1ext")
    lookup.append([scene_1.time + "inf1", ent.charList["wanda"].name, "attribute"])

    rel_for_sc_1.elaborationFor(scene_1.time + "ev1", scene_1.time + "inf1")
    ####

    ####
    ent.charList["wanda"].hasLocation(ent.locList["corner of room"], rule.getVerbList("sit"), scene_1.time + "ev2")
    lookup.append([scene_1.time + "ev2", ent.charList["wanda"].name, "location"])

    ent.locList["boggins heights"].hasAttribute(ent.locList["boggins heights road"],
                                                rule.getVerbList("have"), scene_1.time + "inf4")

    lookup.append([scene_1.time + "inf4", ent.locList["boggins heights"].name, "attribute"])

    rule.assignPropBySeating(ent.charList["wanda"], scene_1.time + "inf2")
    lookup.append([scene_1.time + "inf2", ent.charList["wanda"].name, "property"])

    rel_for_sc_1.causedBy(scene_1.time + "ev2", scene_1.time + "inf2")
    ####

    ####
    ent.charList["wanda"].hasLocation(ent.locList["boggins heights"], rule.getVerbList("live"), scene_1.time + "inf3")
    lookup.append([scene_1.time + "inf3", ent.charList["wanda"].name, "location"])

    ent.charList["wanda"].hasAttribute(ent.itemList["shoes"], rule.getVerbList("wear"),
                                       scene_1.time + "inf5").hasProperty("muddy", scene_1.time + "inf5ext")

    lookup.append([scene_1.time + "inf5", ent.charList["wanda"].name, "attribute"])

    rel_for_sc_1.causedBy(scene_1.time + "inf5", [scene_1.time + "inf3", scene_1.time + "inf4"])
    ####


def startScene2():
    scene_2.hasLocation([ent.locList["school"], ent.locList["rm13"]])
    scene_2.hasCharacter([ent.charList["wanda"], ent.charList["bill byron"]])

    rel_for_sc_2 = rel.Relations("Relation for Scene 2")

    ####
    ent.charList["bill byron"].hasAction(rule.getVerbList("notice"), ent.charList["wanda"].name, scene_2.time + "ev1")
    lookup.append([scene_2.time + "ev1", ent.charList["bill byron"].name, "action"])

    ent.charList["wanda"].hasState(rule.getAdjList("absent"), scene_2.time)
    lookup.append([scene_2.time, ent.charList["wanda"].name, "state"])

    rel_for_sc_2.sequence(scene_2.time, scene_2.time + "ev1")

    ent.charList["bill byron"].hasLocation("behind " + ent.charList["wanda"].name, rule.getVerbList("sit"),
                                           scene_2.time + "inf1")
    lookup.append([scene_2.time + "inf1", ent.charList["bill byron"].name, "location"])

    rel_for_sc_2.causedBy(scene_2.time + "ev1", scene_2.time + "inf1")
    # rel_for_sc_2.sequence(startScene1.scene_1.time + "ev2", scene_2.time + "ev1")
    ####


def startScene3():
    scene_3.hasLocation([ent.locList["school"], ent.locList["rm13"]])
    scene_3.hasCharacter([ent.charList["wanda"], ent.charList["maddie"], ent.charList["peggy"]])

    rel_for_sc_3 = rel.Relations("Relation for Scene 3")

    ####
    ent.charList["maddie"].hasState("late to school", scene_3.time + "ev1a")
    lookup.append([scene_3.time + "ev1a", ent.charList["maddie"].name, "state"])

    ent.charList["peggy"].hasState("late to school", scene_3.time + "ev1b")
    lookup.append([scene_3.time + "ev1b", ent.charList["peggy"].name, "state"])

    ent.charList["maddie"].hasAction(rule.getVerbList("wait"), ent.charList["wanda"].name, scene_3.time + "inf1a")
    lookup.append([scene_3.time + "inf1a", ent.charList["maddie"].name, "action"])

    ent.charList["peggy"].hasAction(rule.getVerbList("wait"), ent.charList["wanda"].name, scene_3.time + "inf1b")
    lookup.append([scene_3.time + "inf1b", ent.charList["peggy"].name, "action"])

    ent.charList["wanda"].hasState(rule.getVerbList("absent"), scene_3.time + "inf2")
    lookup.append([scene_3.time + "inf2", ent.charList["wanda"].name, "state"])

    ent.charList["peggy"].hasDesire(rule.getVerbList("bully"), ent.charList["wanda"].name, scene_3.time + "ev2")
    lookup.append([scene_3.time + "ev2", ent.charList["peggy"].name, "desire"])

    rel_for_sc_3.causedBy(scene_3.time + "ev1", [scene_3.time + "inf1", scene_3.time + "inf2"])
    rel_for_sc_3.causedBy(scene_3.time + "inf1", scene_3.time + "ev2")
    ####

    ####
    ent.charList["peggy"].hasLocation(ent.locList["front row"], rule.getVerbList("sit"), scene_3.time + "inf4")
    lookup.append([scene_3.time + "inf4", ent.charList["peggy"].name, "location"])

    ent.charList["maddie"].hasLocation(ent.locList["front row"], rule.getVerbList("sit"), scene_3.time + "inf5")
    lookup.append([scene_3.time + "inf5", ent.charList["maddie"].name, "location"])

    rule.assignPropBySeating(ent.charList["maddie"], scene_3.time + "inf6")
    lookup.append([scene_3.time + "inf6", ent.charList["maddie"].name, "property"])

    rule.assignPropBySeating(ent.charList["peggy"], scene_3.time + "inf7")
    lookup.append([scene_3.time + "inf7", ent.charList["peggy"].name, "property"])

    ent.charList["peggy"].hasProperty("pretty", scene_3.time + "inf8")
    lookup.append([scene_3.time + "inf8", ent.charList["peggy"].name, "property"])

    ent.charList["peggy"].hasAttribute(ent.itemList["clothes"], rule.getVerbList("wear"),
                                       scene_3.time + "inf9").hasProperty(
        ["many", "pretty"], scene_3.time + "inf9ext")
    lookup.append([scene_3.time + "inf9", ent.charList["peggy"].name, "attribute"])

    ent.charList["peggy"].hasProperty("popular", scene_3.time + "inf10")
    lookup.append([scene_3.time + "inf10", ent.charList["peggy"].name, "property"])

    rel_for_sc_3.causedBy(scene_3.time + "inf10", [scene_3.time + "inf8", scene_3.time + "inf9"])

    # ent.itemList["friend"]_peg = item("ent.charList["maddie"]")
    # ent.itemList["friend"]_mad = item("ent.charList["peggy"]")
    # ent.itemList["friend"]_peg.hasProperty("best ent.itemList["friend"]")
    # ent.itemList["friend"]_mad.hasProperty("best ent.itemList["friend"]")
    # ent.charList["maddie"].hasAttribute(ent.itemList["friend"]_mad, "has")
    # ent.charList["peggy"].hasAttribute(ent.itemList["friend"]_peg, "has")("behind " + ent.charList["wanda"].name, "sit", scene_2.time + "inf1")
    ####


def startScene4():
    scene_4.hasLocation([ent.locList["school"], ent.locList["rm13"]])
    scene_4.hasCharacter([ent.charList["wanda"], ent.charList["maddie"], ent.charList["peggy"], ent.charList["people"],
                          ent.charList["svenson"]])

    rel_for_sc_4 = rel.Relations("Relation for Scene 4")

    ####
    ent.charList["wanda"].hasLocation(ent.itemList["frame house"], rule.getVerbList("live"), scene_4.time + "ev1")
    lookup.append([scene_4.time + "ev1", ent.charList["wanda"].name, "location"])

    rule.checkIfPersonIsPoor(ent.charList["wanda"], scene_4.time + "inf2")
    lookup.append([scene_4.time + "inf2", ent.charList["wanda"].name, "property"])

    rel_for_sc_4.causedBy(scene_4.time + "ev1", scene_4.time + "inf2")
    ####

    ####
    ent.charList["wanda"].hasAttribute(ent.itemList["mother"], rule.getVerbList("have"),
                                       scene_4.time + "inf3").hasProperty("no", scene_4.time + "inf3ext")
    lookup.append([scene_4.time + "inf3", ent.charList["wanda"].name, "attribute"])

    ent.charList["svenson"].hasLocation(ent.locList["svenson house"], "live",
                                        scene_4.time + "inf6").hasProperty("yellow", scene_4.time + "inf6ext")
    lookup.append([scene_4.time + "inf6", ent.charList["svenson"].name, "location"])

    ent.charList["people"].hasAction("avoid", ent.locList["svenson house"].name, scene_4.time + "inf4")
    lookup.append([scene_4.time + "inf4", ent.charList["people"].name, "action"])

    ent.charList["people"].hasAction("gossip", ent.charList["svenson"].name, scene_4.time + "inf5")
    lookup.append([scene_4.time + "inf5", ent.charList["people"].name, "action"])

    rel_for_sc_4.causedBy(scene_4.time + "inf4", scene_4.time + "inf5")
    ####


def startScene5():
    scene_5.hasLocation([ent.locList["school"], ent.locList["rm13"]])
    scene_5.hasCharacter([ent.charList["wanda"], ent.charList["maddie"], ent.charList["peggy"], ent.charList["girls"]])

    rel_for_sc_5 = rel.Relations("Relation for Scene 5")

    ####
    ent.charList["wanda"].hasAttribute(ent.itemList["name"],
                                       "has", scene_5.time + "inf1").hasProperty(["weird", "not easy to say"],
                                                                                 scene_5.time + "inf1ext")
    lookup.append([scene_5.time + "inf1", ent.charList["wanda"].name, "attribute"])

    rel_for_sc_5.causedBy(scene_1.time + "inf1", scene_5.time + "inf1")
    ####

    ####
    ent.charList["wanda"].hasAttribute(ent.itemList["dress"],
                                       "wear", scene_5.time + "inf2").hasProperty(["blue", "not ironed properly"],
                                                                                  scene_5.time + "inf2ext")
    lookup.append([scene_5.time + "inf2", ent.charList["wanda"].name, "attribute"])

    rel_for_sc_5.causedBy(scene_5.time + "inf2", scene_4.time + "inf3")
    ####

    ####
    ent.charList["girls"].hasLocation(ent.locList["oliver street"], rule.getVerbList("wait"), scene_5.time + "ev1")
    lookup.append([scene_5.time + "ev1", ent.charList["girls"].name, "location"])

    ent.charList["girls"].hasAction("bully", ent.charList["wanda"].name, scene_5.time + "ev2")
    lookup.append([scene_5.time + "ev2", ent.charList["girls"].name, "action"])

    rel_for_sc_5.causedBy(scene_5.time + "ev1", scene_5.time + "ev2")
    rel_for_sc_5.causedBy(scene_5.time + "ev2",
                          [scene_5.time + "inf1", scene_5.time + "inf2", scene_1.time + "inf3"])
    ####

    ####
    ent.charList["wanda"].hasAction(rule.getVerbList("say"), "something", scene_5.time + "ev3")
    lookup.append([scene_5.time + "ev3", ent.charList["wanda"].name, "action"])

    ent.charList["wanda"].hasAttribute(ent.itemList["hun dresses"], rule.getVerbList("have"), scene_5.time)
    lookup.append([scene_5.time, ent.charList["wanda"].name, "attribute"])

    rel_for_sc_5.causedBy(scene_5.time + "ev3", scene_5.time)

    ent.charList["girls"].hasAction(rule.getVerbList("believe", negator="not"), "Wanda's statement",
                                    scene_5.time + "ev4")
    lookup.append([scene_5.time + "ev4", ent.charList["girls"].name, "action"])

    ent.charList["wanda"].hasAttribute(ent.itemList["hun dresses"], rule.getVerbList("have"), scene_5.time)
    lookup.append([scene_5.time, ent.charList["wanda"].name, "attribute"])
    rel_for_sc_5.causedBy(scene_5.time + "ev4", [scene_5.time + "ev3", scene_5.time])

    rel_for_sc_5.causedBy(scene_5.time + "ev2", [scene_5.time + "ev3", scene_5.time + "ev4"])
    ####


def startScene6():
    scene_6.hasLocation([ent.locList["school"], ent.locList["rm13"]])
    scene_6.hasCharacter([ent.charList["wanda"], ent.charList["maddie"], ent.charList["girls"]])

    rel_for_sc_6 = rel.Relations("Relation for Scene 6")

    ####
    ent.charList["maddie"].hasState(rule.getAdjList("guilty"), scene_6.time + "ev1")
    lookup.append([scene_6.time + "ev1", ent.charList["maddie"].name, "state"])

    rel_for_sc_6.causedBy(scene_6.time + "ev1", scene_5.time + "ev2")
    ####

    ####
    ent.charList["maddie"].hasProperty("poor", scene_6.time + "inf1")
    lookup.append([scene_6.time + "inf1", ent.charList["maddie"].name, "property"])

    ent.charList["maddie"].hasAttribute(ent.itemList["clothes"],
                                        rule.getVerbList("wear"), scene_6.time + "inf2").hasProperty(
        "peggy's hand-me-down", scene_6.time + "inf2ext")
    lookup.append([scene_6.time + "inf2", ent.charList["maddie"].name, "attribute"])

    ent.charList["maddie"].hasAction(rule.getVerbList("sympathize"), ent.charList["wanda"].name, scene_6.time + "ev2")
    lookup.append([scene_6.time + "ev2", ent.charList["maddie"].name, "action"])

    rel_for_sc_6.causedBy(scene_6.time + "ev1", scene_6.time + "ev2")
    rel_for_sc_6.causedBy(scene_6.time + "ev2", [scene_6.time + "inf1", scene_6.time + "inf2"])
    ####

    ####
    ent.charList["girls"].hasAction(rule.getVerbList("bully", negator="not"), ent.charList["maddie"].name,
                                    scene_6.time + "ev3")
    lookup.append([scene_6.time + "ev3", ent.charList["girls"].name, "action"])

    ent.charList["maddie"].hasAttribute(
        ent.itemList["name"], rule.getVerbList("have"), scene_6.time + "inf3").hasProperty(
        ["not weird", "not hard to say"], scene_6.time + "inf3ext")
    lookup.append([scene_6.time + "inf3", ent.charList["maddie"].name, "attribute"])

    ent.charList["maddie"].hasLocation("not Boggins Heights", rule.getVerbList("live"), scene_6.time + "inf4")
    lookup.append([scene_6.time + "inf4", ent.charList["maddie"].name, "location"])

    rel_for_sc_6.causedBy(scene_6.time + "ev3", [scene_6.time + "inf3", scene_6.time + "inf4"])
    ####

    ####
    ent.charList["maddie"].hasState(rule.getAdjList("guilty"), scene_6.time + "ev4")
    lookup.append([scene_6.time + "ev4", ent.charList["maddie"].name, "state"])

    ent.charList["maddie"].hasAction(rule.getVerbList("defend", negator="not"), ent.charList["wanda"].name,
                                     scene_6.time + "inf5")
    lookup.append([scene_6.time + "inf5", ent.charList["maddie"].name, "action"])

    rel_for_sc_6.causedBy(scene_6.time + "ev4", scene_6.time + "inf5")
    ####


def startScene7():
    scene_7.hasLocation([ent.locList["school"], ent.locList["rm13"]])
    scene_7.hasCharacter([ent.charList["wanda"], ent.charList["maddie"], ent.charList["cecile"], ent.charList["peggy"],
                          ent.charList["girls"]])

    rel_for_sc_7 = rel.Relations("Relation for Scene 7")

    ####
    ent.charList["maddie"].hasState(rule.getAdjList("troubled"), scene_7.time + "ev1")
    lookup.append([scene_7.time + "ev1", ent.charList["maddie"].name, "state"])

    rel_for_sc_7.causedBy(scene_7.time + "ev1", [scene_3.time + "ev1", scene_6.time + "ev1"])
    ####

    ####
    ent.charList["maddie"].hasAction(rule.getVerbList("think"), ent.charList["wanda"].name, scene_7.time + "ev2")
    lookup.append([scene_7.time + "ev2", ent.charList["maddie"].name, "action"])

    ent.charList["maddie"].hasAction(rule.getVerbList("think"), ent.itemList["game"].name, scene_7.time + "ev3")
    lookup.append([scene_7.time + "ev3", ent.charList["maddie"].name, "action"])

    rel_for_sc_7.causedBy(scene_7.time + "ev1", [scene_7.time + "ev2", scene_7.time + "ev3"])
    ####

    ####
    ent.itemList["game"].hasState(rule.getAdjList("start"), scene_7.time + "ev4")
    lookup.append([scene_7.time + "ev4", ent.itemList["game"].name, "state"])

    ent.charList["cecile"].hasAction(rule.getVerbList("wear"),
                                     ent.itemList["dress"].hasProperty(["pretty", "red"], scene_7.time),
                                     scene_7.time + "ev5")
    lookup.append([scene_7.time + "ev5", ent.charList["cecile"].name, "action"])

    ent.charList["girls"].hasAction(rule.getVerbList("admire"), ent.charList["cecile"].name, scene_7.time + "ev6")
    lookup.append([scene_7.time + "ev6", ent.charList["girls"].name, "action"])

    ent.charList["cecile"].hasAttribute(ent.itemList["clothes"],
                                        rule.getVerbList("wear"), scene_7.time + "inf1").hasProperty(
        "prettier than others", scene_7.time + "inf1ext")
    lookup.append([scene_7.time + "inf1", ent.charList["cecile"].name, "attribute"])

    ent.charList["cecile"].hasProperty(["tall", "slender"], scene_7.time + "inf2")
    lookup.append([scene_7.time + "inf2", ent.charList["cecile"].name, "property"])

    rel_for_sc_7.causedBy(scene_7.time + "ev4", [scene_7.time + "ev5", scene_7.time + "ev6"])
    rel_for_sc_7.causedBy(scene_7.time + "ev6", [scene_7.time + "inf1", scene_7.time + "inf2"])
    ####

    ####
    ent.charList["wanda"].hasDesire(rule.getVerbList("join"), ent.charList["girls"].name, scene_7.time + "ev8")
    lookup.append([scene_7.time + "ev8", ent.charList["wanda"].name, "desire"])

    rel_for_sc_7.causedBy(scene_5.time + "ev3", scene_7.time + "ev8")

    ent.charList["peggy"].hasAction(rule.getVerbList("tease"), ent.charList["wanda"].name, scene_7.time + "ev9")
    lookup.append([scene_7.time + "ev9", ent.charList["peggy"].name, "action"])

    rel_for_sc_7.causedBy(scene_7.time + "ev9", scene_5.time + "ev3")
    ####


def startScene8():
    scene_8.hasLocation([ent.locList["school"], ent.locList["rm13"]])
    scene_8.hasCharacter([ent.charList["wanda"], ent.charList["maddie"], ent.charList["peggy"]])

    rel_for_sc_8 = rel.Relations("Relation for Scene 8")

    ####
    ent.charList["maddie"].hasDesire(rule.getVerbList("wish"), "stop" + ent.charList["peggy"].name,
                                     scene_8.time + "ev1")
    lookup.append([scene_8.time + "ev1", ent.charList["maddie"].name, "desire"])

    ent.charList["peggy"].hasAction(rule.getVerbList("bully"), ent.charList["wanda"].name, scene_8.time + "ev1a")
    lookup.append([scene_8.time + "ev1a", ent.charList["peggy"].name, "action"])

    rel_for_sc_8.causedBy(scene_8.time + "ev1", scene_8.time + "ev1a")

    ent.charList["maddie"].hasAction(rule.getVerbList("write"), ent.itemList["note"].name, scene_8.time + "ev2")
    lookup.append([scene_8.time + "ev2", ent.charList["maddie"].name, "action"])

    rel_for_sc_8.causedBy(scene_8.time + "ev2", scene_8.time + "ev1")
    ####

    ####
    ent.charList["maddie"].hasAction(rule.getVerbList("destroy"), ent.itemList["note"].name, scene_8.time + "ev3")
    lookup.append([scene_8.time + "ev3", ent.charList["maddie"].name, "action"])

    ent.charList["maddie"].hasDesire(rule.getVerbList("want", negator="not"),
                                     "argue with " + ent.charList["peggy"].name, scene_8.time + "ev4")
    lookup.append([scene_8.time + "ev4", ent.charList["maddie"].name, "desire"])

    ent.charList["peggy"].hasAction("hate", ent.charList["maddie"].name, scene_8.time + "ev4a")
    lookup.append([scene_8.time + "ev4a", ent.charList["peggy"].name, "action"])

    rel_for_sc_8.causedBy(scene_8.time + "ev3", [scene_8.time + "ev4", scene_8.time + "ev4a"])
    ####


def startScene9():
    scene_9.hasLocation([ent.locList["school"], ent.locList["rm13"]])
    scene_9.hasCharacter([ent.charList["wanda"], ent.charList["maddie"]])

    rel_for_sc_9 = rel.Relations("Relation for Scene 9")

    ####
    ent.charList["wanda"].hasAction(rule.getVerbList("struggle"), "read paragraphs",
                                    scene_9.time + "ev1")

    lookup.append([scene_9.time + "", ent.charList["wanda"].name, "action"])

    ent.charList["wanda"].hasProperty("timid", scene_9.time + "inf1")
    lookup.append([scene_9.time + "inf1", ent.charList["wanda"].name, "property"])

    ent.charList["wanda"].hasProperty("not smart", scene_9.time + "inf2")
    lookup.append([scene_9.time + "inf2", ent.charList["wanda"].name, "property"])

    rel_for_sc_9.causedBy(scene_9.time + "ev1", [scene_9.time + "inf1", scene_9.time + "inf2"])
    ####

    # ent.charList["wanda"].hasAction("describe", ent.itemList["dress"].hasProperty(["pale blue", "with cerise-colored trimmings"]), scene_9.time + "ev2")
    # ent.charList["wanda"].hasAction("describe", ent.itemList["dress"].hasProperty(["jungle green", "with red sash"]), scene_9.time + "ev3")

    ####
    ent.charList["peggy"].hasProperty("artistic", scene_9.time + "ev2")
    lookup.append([scene_9.time + "ev2", ent.charList["peggy"].name, "property"])

    ent.charList["maddie"].hasAction(rule.getAdjList("know"), "winner", scene_9.time + "ev3")
    lookup.append([scene_9.time + "ev3", ent.charList["maddie"].name, "action"])

    ent.charList["peggy"].hasAction(rule.getVerbList("win"), ent.itemList["drawing contest"].name, scene_9.time + "ev4")
    lookup.append([scene_9.time, ent.charList["peggy"].name, "action"])

    rel_for_sc_9.causedBy(scene_9.time + "ev3", [scene_9.time + "ev4", scene_9.time + "ev2"])
    ####


def startScene10():
    scene_10.hasLocation([ent.locList["school"], ent.locList["rm13"]])
    scene_10.hasCharacter(
        [ent.charList["wanda"], ent.charList["maddie"], ent.charList["peggy"], ent.charList["miss mason"]])

    rel_for_sc_10 = rel.Relations("Relation for Scene 10")

    ####
    ent.charList["maddie"].hasState(rule.getAdjList("shocked"), scene_10.time + "ev1a")
    lookup.append([scene_10.time + "ev1a", ent.charList["maddie"].name, "state"])

    ent.charList["peggy"].hasState(rule.getAdjList("shocked"), scene_10.time + "ev1b")
    lookup.append([scene_10.time + "ev1b", ent.charList["peggy"].name, "state"])

    ent.locList["rm13"].hasAttribute(ent.itemList["drawing"].hasProperty(["100 pieces", "pretty"],
                                                                         scene_10.time + "inf1ext"),
                                     rule.getVerbList("post"), scene_10.time + "inf1")
    lookup.append([scene_10.time + "inf1", ent.locList["rm13"].name, "attribute"])

    rel_for_sc_10.causedBy(scene_10.time + "ev1", scene_10.time + "inf1")
    ####

    ####
    ent.charList["miss mason"].hasAction(rule.getVerbList("announce"), "winner", scene_10.time + "ev2")
    lookup.append([scene_10.time + "ev2", ent.charList["miss mason"].name, "action"])

    ent.charList["wanda"].hasAction(rule.getVerbList("win"), ent.itemList["drawing contest"].name, scene_10.time + "ev6")
    lookup.append([scene_10.time + "ev6", ent.charList["wanda"].name, "action"])

    rel_for_sc_10.sequence(scene_10.time + "ev2", scene_10.time + "ev6")

    ent.charList["wanda"].hasAction(rule.getVerbList("submit"),
                                    ent.itemList["drawing"].hasProperty(["100 pieces", "pretty"],
                                                                        scene_10.time + "ev3ext"),
                                    scene_10.time + "ev3")
    lookup.append([scene_10.time + "ev3", ent.charList["wanda"].name, "action"])

    rel_for_sc_10.causedBy(scene_10.time + "ev2", scene_10.time + "ev3")
    ####

    ####
    ent.charList["wanda"].hasAction(rule.getVerbList("receive", negator="not"), ent.itemList["medal"].name,
                                    scene_10.time + "ev4")
    lookup.append([scene_10.time + "ev4", ent.charList["wanda"].name, "action"])

    ent.charList["wanda"].hasState(rule.getAdjList("absent"), scene_10.time + "ev5")
    lookup.append([scene_10.time + "ev5", ent.charList["wanda"].name, "state"])

    rel_for_sc_10.causedBy(scene_10.time + "ev4", scene_10.time + "ev5")
    ####


def startScene11():
    scene_11.hasLocation([ent.locList["school"], ent.locList["rm13"]])
    scene_11.hasCharacter([ent.charList["wanda"], ent.charList["students"], ent.charList["miss mason"]])

    rel_for_sc_11 = rel.Relations("Relation for Scene 11")

    ####
    ent.charList["miss mason"].hasAction(rule.getVerbList("receive"), ent.itemList["note"].name, scene_11.time + "ev1")
    lookup.append([scene_11.time + "ev1", ent.charList["miss mason"].name, "action"])

    ent.charList["miss mason"].hasState(rule.getAdjList("serious"), scene_11.time + "ev2")
    lookup.append([scene_11.time + "ev2", ent.charList["miss mason"].name, "state"])

    ent.charList["wanda"].hasState(rule.getAdjList("hurt"), scene_11.time + "inf1")
    lookup.append([scene_11.time + "inf1", ent.charList["wanda"].name, "state"])

    ent.itemList["note"].hasPurpose(rule.getVerbList("say"), ent.charList["wanda"].name + "'s wherabouts",
                                    scene_11.time + "ev3")
    lookup.append([scene_11.time + "ev3", ent.itemList["note"].name, "action"])

    ent.charList["wanda"].hasAction(rule.getVerbList("move"), "town", scene_11.time)
    lookup.append([scene_11.time, ent.charList["wanda"].name, "action"])

    rel_for_sc_11.sequence(scene_11.time + "ev3", scene_11.time)

    rel_for_sc_11.causedBy(scene_11.time + "ev3", scene_11.time + "inf1")
    rel_for_sc_11.causedBy(scene_11.time + "inf1", scene_5.time + "ev2")
    rel_for_sc_11.causedBy(scene_11.time + "ev2", [scene_11.time + "ev1", scene_11.time + "ev3"])
    rel_for_sc_11.causedBy(scene_11.time + "ev3", scene_5.time + "ev2")
    ####

    ####
    ent.charList["miss mason"].hasAction(rule.getVerbList("defend"), ent.charList["students"].name, scene_11.time + "ev4")
    lookup.append([scene_11.time + "ev4", ent.charList["miss mason"].name, "action"])

    ent.charList["miss mason"].hasAction("state", ent.charList["students"].name + "' defense", scene_11.time + "ev6")
    lookup.append([scene_11.time + "ev6", ent.charList["miss mason"].name, "action"])

    ent.charList["students"].hasAction(rule.getVerbList("desire", negator="not"), "sadden " + ent.charList["wanda"].name, scene_11.time + "ev7")
    lookup.append([scene_11.time + "ev7", ent.charList["students"].name, "action"])

    rel_for_sc_11.causedBy(scene_11.time + "ev6", scene_11.time + "ev7")

    ent.charList["miss mason"].hasAction(rule.getVerbList("talk"), ent.charList["students"].name, scene_11.time + "ev5")
    lookup.append([scene_11.time + "ev5", ent.charList["miss mason"].name, "action"])

    ent.charList["students"].hasAction(rule.getVerbList("reflect"), ent.itemList["note"].name, scene_11.time + "ev7"),
    lookup.append([scene_11.time + "ev6", ent.charList["students"].name, "action"])

    rel_for_sc_11.sequence(scene_11.time + "ev5", scene_11.time + "ev7")

    rel_for_sc_11.causedBy(scene_11.time + "ev4", scene_11.time + "ev6")
    rel_for_sc_11.causedBy(scene_11.time + "ev5", scene_11.time + "ev3")
    ####


def startScene12():
    scene_12.hasLocation([ent.locList["school"], ent.locList["rm13"]])
    scene_12.hasCharacter([ent.charList["wanda"], ent.charList["maddie"]])

    rel_for_sc_12 = rel.Relations("Relation for Scene 12")

    ####
    ent.charList["maddie"].hasState(rule.getAdjList("distracted"), scene_12.time + "ev1")
    lookup.append([scene_12.time + "ev1", ent.charList["maddie"].name, "state"])

    ent.charList["maddie"].hasState(rule.getAdjList("sick"), scene_12.time + "ev2")
    lookup.append([scene_12.time + "ev2", ent.charList["maddie"].name, "state"])

    rel_for_sc_12.causedBy(scene_11.time + "ev3", [scene_12.time + "ev1", scene_12.time + "ev2"])
    ####

    ####
    ent.charList["maddie"].hasAction(rule.getVerbList("defend", negator="not"), ent.charList["wanda"].name, scene_12.time + "ev4")
    lookup.append([scene_12.time + "ev4", ent.charList["maddie"].name, "action"])

    ent.charList["maddie"].hasAction(rule.getAdjList("sorry"), "actions", scene_12.time + "ev5")
    lookup.append([scene_12.time + "ev5", ent.charList["maddie"].name, "state"])

    rel_for_sc_12.causedBy(scene_12.time + "ev5", scene_11.time + "ev4")

    ent.charList["girls"].hasAction(rule.getVerbList("bully"), ent.charList["wanda"].name,
                                    scene_12.time),

    ent.charList["maddie"].hasAction(rule.getVerbList("condone", negator="not"), "bullying", scene_12.time + "inf1")
    lookup.append([scene_12.time + "inf1", ent.charList["maddie"].name, "action"])

    rel_for_sc_12.contradiction(scene_12.time + "ev5", scene_12.time + "ev4")
    rel_for_sc_12.causedBy(scene_12.time + "ev4", scene_8.time + "ev4")
    rel_for_sc_12.causedBy([scene_12.time + "ev1", scene_12.time + "ev2"], scene_12.time + "ev4")
    rel_for_sc_12.causedBy(scene_12.time + "inf1", scene_11.time + "inf1")
    ####


def startScene13():
    scene_13.hasLocation([ent.locList["school"], ent.locList["rm13"]])
    scene_13.hasCharacter([ent.charList["wanda"], ent.charList["maddie"], ent.charList["peggy"]])

    rel_for_sc_13 = rel.Relations("Relation for Scene 13")

    ####
    ent.charList["maddie"].hasDesire(rule.getVerbList("apologize"), ent.charList["wanda"].name, scene_13.time + "ev1")
    lookup.append([scene_13.time + "ev1", ent.charList["maddie"].name, "desire"])

    ent.charList["maddie"].hasDesire(rule.getVerbList("visit"), ent.charList["wanda"].name, scene_13.time + "ev2")
    lookup.append([scene_13.time + "ev2", ent.charList["maddie"].name, "desire"])

    rel_for_sc_13.causedBy(scene_13.time + "ev2", scene_13.time + "ev1")
    rel_for_sc_13.causedBy(scene_13.time + "ev1",
                           [scene_6.time + "ev1", scene_12.time + "ev5"])
    ####

    ####
    ent.charList["peggy"].hasAction(rule.getVerbList("say"), "request", scene_13.time + "ev3")
    lookup.append([scene_13.time + "ev3", ent.charList["peggy"].name, "action"])

    ent.charList["peggy"].hasDesire(rule.getVerbList("visit"), ent.charList["wanda"].name, scene_13.time),
    lookup.append([scene_13.time, ent.charList["peggy"].name, "desire"])

    rel_for_sc_13.sequence(scene_13.time  + "ev3", scene_13.time)

    ent.charList["maddie"].hasState(rule.getAdjList("overjoyed"), scene_13.time + "ev5")
    lookup.append([scene_13.time + "ev5", ent.charList["maddie"].name, "state"])

    rel_for_sc_13.causedBy(scene_13.time + "ev5", [scene_13.time + "ev3", scene_13.time + "ev2"])
    ####


def startScene14():
    scene_14.hasLocation([ent.locList["school"], ent.locList["boggins heights"]])
    scene_14.hasCharacter([ent.charList["wanda"], ent.charList["maddie"], ent.charList["peggy"]])

    rel_for_sc_14 = rel.Relations("Relation for Scene 14")

    ####
    ent.charList["maddie"].hasDesire(rule.getVerbList("go_back"), "time", scene_14.time + "ev1")
    lookup.append([scene_14.time + "ev1", ent.charList["maddie"].name, "desire"])

    ent.itemList["game"].hasState(rule.getVerbList("exist", negator="not"), scene_14.time + "inf1")
    lookup.append([scene_14.time + "inf1", ent.itemList["game"].name, "state"])

    rel_for_sc_14.causedBy(scene_14.time + "ev1", scene_14.time + "inf1")
    rel_for_sc_14.causedBy(scene_14.time + "inf1", scene_11.time + "ev3")
    ####

    ####
    ent.charList["peggy"].hasAction(rule.getVerbList("avoid"), ent.locList["svenson house"].name, scene_14.time + "ev5")
    lookup.append([scene_14.time + "ev5", ent.charList["peggy"].name, "action"])

    ent.charList["maddie"].hasAction(rule.getVerbList("avoid"), ent.locList["svenson house"].name, scene_14.time + "ev6")
    lookup.append([scene_14.time + "ev6", ent.charList["maddie"].name, "action"])

    ent.charList["peggy"].hasDesire(rule.getVerbList("meet", negator="not"), ent.charList["svenson"].name,
                                    scene_14.time + "ev7")
    lookup.append([scene_14.time + "ev7", ent.charList["peggy"].name, "desire"])

    ent.charList["maddie"].hasDesire(rule.getVerbList("meet", negator="not"), ent.charList["svenson"].name,
                                     scene_14.time + "ev8")
    lookup.append([scene_14.time + "ev8", ent.charList["maddie"].name, "desire"])

    rel_for_sc_14.causedBy(scene_14.time + "ev5", scene_14.time + "ev7")
    rel_for_sc_14.causedBy(scene_14.time + "ev6", scene_14.time + "ev8")
    rel_for_sc_14.causedBy(scene_14.time + "ev7", scene_4.time + "inf5")
    rel_for_sc_14.causedBy(scene_14.time + "ev8", scene_4.time + "inf5")
    ####

    ####
    ent.charList["maddie"].hasState(rule.getVerbList("worry"), scene_14.time + "ev9")
    lookup.append([scene_14.time + "ev9", ent.charList["maddie"].name, "state"])

    ent.charList["maddie"].hasAction(rule.getVerbList("meet", negator="might not"), ent.charList["wanda"].name,
                                     scene_14.time + "inf3")
    lookup.append([scene_14.time + "inf3", ent.charList["maddie"].name, "action"])

    ent.charList["maddie"].hasAction(rule.getVerbList("apologize", negator="might not"), ent.charList["wanda"].name,
                                     scene_14.time + "inf1")
    lookup.append([scene_14.time + "inf1", ent.charList["maddie"].name, "action"])

    rel_for_sc_14.causedBy(scene_14.time + "ev9", scene_14.time + "inf3")
    rel_for_sc_14.causedBy(scene_14.time + "inf1", scene_14.time + "inf3")
    ####


def startScene15():
    scene_15.hasLocation([ent.locList["school"], ent.locList["boggins heights"]])
    scene_15.hasCharacter([ent.charList["wanda"], ent.charList["maddie"], ent.charList["peggy"]])

    rel_for_sc_15 = rel.Relations("Relation for Scene 15")

    ####
    ent.charList["peggy"].hasState([rule.getAdjList("downcast"), rule.getAdjList("discouraged")], scene_15.time + "ev1")
    lookup.append([scene_15.time + "ev1", ent.charList["peggy"].name, "state"])

    ent.charList["maddie"].hasState([rule.getAdjList("downcast"), rule.getAdjList("discouraged")],
                                    scene_15.time + "ev2")
    lookup.append([scene_15.time + "ev2", ent.charList["maddie"].name, "state"])

    ent.itemList["frame house"].hasState(rule.getAdjList("empty"), scene_15.time + "inf1")
    lookup.append([scene_15.time + "inf1", ent.itemList["frame house"].name, "state"])

    ent.charList["peggy"].hasAction(rule.getVerbList("meet", negator="not"), ent.charList["wanda"].name,
                                    scene_15.time + "ev3")
    lookup.append([scene_15.time + "ev3", ent.charList["peggy"].name, "action"])

    ent.charList["maddie"].hasAction(rule.getVerbList("meet", negator="not"), ent.charList["wanda"].name,
                                     scene_15.time + "ev4")
    lookup.append([scene_15.time + "ev4", ent.charList["maddie"].name, "action"])

    rel_for_sc_15.causedBy(scene_15.time + "ev1", [scene_15.time + "inf1", scene_15.time + "ev3"])
    rel_for_sc_15.causedBy(scene_15.time + "ev2", [scene_15.time + "inf1", scene_15.time + "ev4"])
    ####

    ####
    ent.charList["peggy"].hasAction(rule.getVerbList("write"), ent.itemList["friendly letter"].name, scene_15.time + "ev5")
    lookup.append([scene_15.time + "ev5", ent.charList["peggy"].name, "action"])

    ent.charList["maddie"].hasAction(rule.getVerbList("write"), ent.itemList["friendly letter"].name, scene_15.time + "ev6")
    lookup.append([scene_15.time + "ev6", ent.charList["maddie"].name, "action"])

    ent.charList["peggy"].hasDesire(rule.getVerbList("apologize"), ent.charList["wanda"].name, scene_15.time + "ev7")
    lookup.append([scene_15.time + "ev7", ent.charList["peggy"].name, "desire"])

    ent.charList["maddie"].hasDesire(rule.getVerbList("apologize"), ent.charList["wanda"].name, scene_15.time + "ev8")
    lookup.append([scene_15.time + "ev8", ent.charList["maddie"].name, "desire"])

    rel_for_sc_15.causedBy(scene_15.time + "ev5", [scene_15.time + "ev3", scene_15.time + "ev7"])
    rel_for_sc_15.causedBy(scene_15.time + "ev6", [scene_15.time + "ev4", scene_15.time + "ev8"])
    # ent.charList["peggy"].hasAction("hurry", ent.charList["peggy"].hasAction("reach", ent.locList["boggins heights"], scene_15.time), scene_15.time + "ev5")
    # ent.charList["maddie"].hasAction("hurry", ent.charList["maddie"].hasAction("reach", ent.locList["boggins heights"], scene_15.time), scene_15.time + "ev6")
    # ent.charList["peggy"].hasAction("not find", frame_ent.itemList["house"], scene_15.time + "ev7")
    # ent.charList["maddie"].hasAction("not find", frame_ent.itemList["house"], scene_15.time + "ev8")
    ####


def startScene16():
    scene_16.hasLocation([ent.locList["school"], ent.locList["rm13"]])
    scene_16.hasCharacter([ent.charList["wanda"], ent.charList["maddie"], ent.charList["peggy"]])

    rel_for_sc_16 = rel.Relations("Relation for Scene 16")

    ####
    ent.charList["peggy"].hasState([rule.getAdjList("carefree"), rule.getAdjList("happy")], scene_16.time + "ev1")
    lookup.append([scene_16.time + "ev1", ent.charList["peggy"].name, "state"])

    ent.charList["maddie"].hasState([rule.getAdjList("carefree"), rule.getAdjList("happy")], scene_16.time + "ev2")
    lookup.append([scene_16.time + "ev2", ent.charList["maddie"].name, "state"])

    ent.charList["peggy"].hasAction(rule.getVerbList("send"), ent.itemList["friendly letter"].name, scene_16.time + "ev3")
    lookup.append([scene_16.time + "ev3", ent.charList["peggy"].name, "action"])

    ent.charList["maddie"].hasAction(rule.getVerbList("send"), ent.itemList["friendly letter"].name, scene_16.time + "ev4")
    lookup.append([scene_16.time + "ev4", ent.charList["maddie"].name, "action"])

    ent.charList["peggy"].hasAction(rule.getVerbList("reconcile"), ent.charList["wanda"].name, scene_16.time + "ev5")
    lookup.append([scene_16.time + "ev5", ent.charList["peggy"].name, "action"])

    ent.charList["maddie"].hasAction(rule.getVerbList("reconcile"), ent.charList["wanda"].name, scene_16.time + "ev6")
    lookup.append([scene_16.time + "ev6", ent.charList["maddie"].name, "action"])

    rel_for_sc_16.causedBy(scene_16.time + "ev1", scene_16.time + "ev3")
    rel_for_sc_16.causedBy(scene_16.time + "ev2", scene_16.time + "ev4")
    rel_for_sc_16.consequence(scene_16.time + "ev3", [scene_16.time + "ev5", scene_15.time + "ev7"])
    rel_for_sc_16.consequence(scene_16.time + "ev4", [scene_16.time + "ev6", scene_15.time + "ev8"])
    ####

    ####
    ent.charList["peggy"].hasAction(rule.getVerbList("understand"), ent.charList["wanda"].name, scene_16.time + "ev7")
    lookup.append([scene_16.time + "ev7", ent.charList["peggy"].name, "action"])

    ent.charList["maddie"].hasAction(rule.getVerbList("understand"), ent.charList["wanda"].name, scene_16.time + "ev8")
    lookup.append([scene_16.time + "ev8", ent.charList["maddie"].name, "action"])

    ent.charList["wanda"].hasAttribute(ent.itemList["clothes"], rule.getVerbList("have"),
                                       scene_16.time + "inf1").hasProperty("only one", scene_16.time + "inf1ext")
    lookup.append([scene_16.time + "inf1", ent.charList["wanda"].name, "attribute"])
    # ent.charList["wanda"].hasAction("iron", ent.itemList["clothes"], scene_16.time + "inf2")

    rel_for_sc_16.causedBy(scene_16.time + "ev7", scene_16.time + "inf1")
    rel_for_sc_16.causedBy(scene_16.time + "ev8", scene_16.time + "inf1")
    rel_for_sc_16.causedBy(scene_16.time + "inf1", scene_4.time + "inf2")
    rel_for_sc_16.causedBy(scene_5.time + "inf2", scene_16.time + "inf1")
    # rel_for_sc_16.causedBy(startScene5.scene_5.time + "inf2", startScene4.scene_4.time + "inf3")
    # rel_for_sc_16.causedBy(scene_16.time + "inf1", startScene5.scene_5.time + "inf2")
    ####


def startScene17():
    scene_17.hasLocation([ent.locList["school"], ent.locList["rm13"]])
    scene_17.hasCharacter(
        [ent.charList["wanda"], ent.charList["maddie"], ent.charList["peggy"], ent.charList["miss mason"]])

    rel_for_sc_17 = rel.Relations("Relation for Scene 17")

    ####
    ent.charList["miss mason"].hasAction(rule.getVerbList("receive"),
                                         ent.itemList["letter"].hasProperty("wanda's", scene_17.time + "ev1ext"),
                                         scene_17.time + "ev1")
    lookup.append([scene_17.time + "", ent.charList["miss mason"].name, "action"])

    ent.charList["miss mason"].hasAction(rule.getVerbList("know"), ent.charList["wanda"].name + " new house", scene_17.time + "inf1")
    lookup.append([scene_17.time + "inf1", ent.charList["miss mason"].name, "action"])

    ent.charList["miss mason"].hasAction(rule.getVerbList("send", negator="can"), ent.itemList["medal"].name,
                                         scene_17.time + "ev2")
    lookup.append([scene_17.time + "", ent.charList["students"].name, "action"])

    rel_for_sc_17.consequence(scene_17.time + "ev1", scene_17.time + "inf1")
    rel_for_sc_17.consequence(scene_17.time + "inf1", scene_17.time + "ev2")
    rel_for_sc_17.causedBy(scene_17.time + "ev2", scene_10.time + "ev4")
    ####

    ####
    ent.charList["wanda"].hasAction(rule.getVerbList("forgive"), [ent.charList["peggy"].name, ent.charList["maddie"].name],
                                    scene_17.time + "ev3")
    lookup.append([scene_17.time + "ev3", ent.charList["wanda"].name, "action"])

    ent.charList["wanda"].hasAction(rule.getVerbList("give"),
                                    ent.itemList["dress"].hasProperty(["pale blue", "with cerise-colored trimmings"],
                                                                      scene_17.time + "ev4ext"),
                                    scene_17.time + "ev4")
    lookup.append([scene_17.time + "ev4", ent.charList["wanda"].name, "action"])

    ent.charList["wanda"].hasAction(rule.getVerbList("give"),
                                    ent.itemList["dress"].hasProperty(["jungle green", "with red sash"], scene_17.time + "ev5ext"),
                                    scene_17.time + "ev5")
    lookup.append([scene_17.time + "ev5", ent.charList["wanda"].name, "action"])

    ent.charList["wanda"].hasAction(rule.getVerbList("receive"), ent.itemList["friendly letter"].name,
                                    scene_17.time + "ev6")
    lookup.append([scene_17.time + "ev6", ent.charList["wanda"].name, "action"])

    rel_for_sc_17.contradiction(scene_17.time + "ev3", scene_5.time + "ev2")
    rel_for_sc_17.causedBy([scene_17.time + "ev4", scene_17.time + "ev5"], scene_17.time + "ev3")
    rel_for_sc_17.causedBy(scene_17.time + "ev3", scene_17.time + "ev6")
    rel_for_sc_17.causedBy(scene_17.time + "ev6",
                           [scene_16.time + "ev3", scene_16.time + "ev4"])
    ####


def startScene18():
    scene_18.hasLocation([ent.locList["school"], ent.locList["rm13"]])
    scene_18.hasCharacter([ent.charList["wanda"], ent.charList["maddie"], ent.charList["peggy"]])

    rel_for_sc_18 = rel.Relations("Relation for Scene 18")

    ####
    ent.charList["maddie"].hasState(rule.getAdjList("sad"), scene_18.time + "ev1")
    lookup.append([scene_18.time + "", ent.charList["maddie"].name, "state"])

    ent.charList["peggy"].hasState(rule.getAdjList("guilty", negator="not"), scene_18.time + "ev2")
    lookup.append([scene_18.time + "ev2", ent.charList["peggy"].name, "state"])

    rel_for_sc_18.causedBy(scene_18.time + "ev1", scene_17.time + "ev4")
    rel_for_sc_18.causedBy(scene_18.time + "ev2", scene_17.time + "ev5")
    ####

    ####
    ent.charList["maddie"].hasState(rule.getVerbList("cry"), scene_17.time + "ev3")
    lookup.append([scene_18.time + "ev3", ent.charList["maddie"].name, "state"])

    rel_for_sc_18.causedBy(scene_18.time + "ev3",
                           [scene_6.time + "inf5", scene_17.time + "ev3"])
    ####

    ####
    ent.charList["peggy"].hasAction(rule.getVerbList("understand"), ent.itemList["hun dresses"].name, scene_18.time + "ev4")
    lookup.append([scene_18.time + "ev4", ent.charList["peggy"].name, "action"])

    ent.charList["maddie"].hasAction(rule.getVerbList("understand"), ent.itemList["hun dresses"].name, scene_18.time + "ev5")
    lookup.append([scene_18.time + "ev5", ent.charList["maddie"].name, "action"])

    rel_for_sc_18.causedBy(scene_18.time + "ev4", scene_10.time + "ev3")
    rel_for_sc_18.causedBy(scene_18.time + "ev5", scene_10.time + "ev3")
    ####

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