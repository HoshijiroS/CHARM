import model.story_world.classes.Relations as Rel
import model.story_world.classes.Scene as Scene
import model.story_world.entities as Entity
import model.story_world.rules as Rule

lookup = []

scene_1 = Scene.Scene("Scene 1", "Monday")
scene_2 = Scene.Scene("Scene 2", "Tuesday")
scene_3 = Scene.Scene("Scene 3", "Wednesday")
scene_4 = Scene.Scene("Scene 4", "Wednesday")
scene_5 = Scene.Scene("Scene 5", "Wednesday")
scene_6 = Scene.Scene("Scene 6", "Wednesday")
scene_7 = Scene.Scene("Scene 7", "Wednesday")
scene_8 = Scene.Scene("Scene 8", "Wednesday")
scene_9 = Scene.Scene("Scene 9", "Wednesday")
scene_10 = Scene.Scene("Scene 10", "Thursday")
scene_11 = Scene.Scene("Scene 11", "Thursday")
scene_12 = Scene.Scene("Scene 12", "Thursday")
scene_13 = Scene.Scene("Scene 13", "Thursday")
scene_14 = Scene.Scene("Scene 14", "Thursday")
scene_15 = Scene.Scene("Scene 15", "Thursday")
scene_16 = Scene.Scene("Scene 16", "Friday")
scene_17 = Scene.Scene("Scene 17", "Christmas Time")
scene_18 = Scene.Scene("Scene 18", "Christmas Time")


def startScene1():
    scene_1.hasLocation([Entity.locList["school"], Entity.locList["rm13"]])
    scene_1.hasCharacter([Entity.charList["wanda"], Entity.charList["students"]])

    rel_for_sc_1 = Rel.Relations("Relation for Scene 1")

    ####
    Entity.charList["students"].hasAction(Rule.getVerbList("notice", negator="not"), Entity.charList["wanda"].name,
                                          scene_1.time + "ev1")
    lookup.append([scene_1.time + "ev1", Entity.charList["students"].name, "action"])

    Entity.charList["wanda"].hasState(Rule.getAdjList("absent"), scene_1.time)
    lookup.append([scene_1.time, Entity.charList["wanda"].name, "state"])

    rel_for_sc_1.causedBy(scene_1.time + "ev1", scene_1.time)

    Entity.charList["wanda"].hasAttribute(Entity.itemList["friend"], Rule.getVerbList("have"),
                                          scene_1.time + "inf1").hasProperty("no", scene_1.time + "inf1ext")
    lookup.append([scene_1.time + "inf1", Entity.charList["wanda"].name, "attribute"])

    rel_for_sc_1.elaborationFor(scene_1.time + "ev1", scene_1.time + "inf1")
    ####

    ####
    Entity.charList["wanda"].hasLocation(Entity.locList["corner of room"], Rule.getVerbList("sit"),
                                         scene_1.time + "ev2")
    lookup.append([scene_1.time + "ev2", Entity.charList["wanda"].name, "location"])

    Entity.locList["boggins heights"].hasAttribute(Entity.locList["boggins heights road"],
                                                   Rule.getVerbList("have"), scene_1.time + "inf4")

    lookup.append([scene_1.time + "inf4", Entity.locList["boggins heights"].name, "attribute"])

    Rule.assignPropBySeating(Entity.charList["wanda"], scene_1.time + "inf2")
    lookup.append([scene_1.time + "inf2", Entity.charList["wanda"].name, "property"])

    rel_for_sc_1.causedBy(scene_1.time + "ev2", scene_1.time + "inf2")
    ####

    ####
    Entity.charList["wanda"].hasLocation(Entity.locList["boggins heights"], Rule.getVerbList("live"),
                                         scene_1.time + "inf3")
    lookup.append([scene_1.time + "inf3", Entity.charList["wanda"].name, "location"])

    Entity.charList["wanda"].hasAttribute(Entity.itemList["shoes"], Rule.getVerbList("wear"),
                                          scene_1.time + "inf5").hasProperty("muddy", scene_1.time + "inf5ext")

    lookup.append([scene_1.time + "inf5", Entity.charList["wanda"].name, "attribute"])

    rel_for_sc_1.causedBy(scene_1.time + "inf5", [scene_1.time + "inf3", scene_1.time + "inf4"])
    ####


def startScene2():
    scene_2.hasLocation([Entity.locList["school"], Entity.locList["rm13"]])
    scene_2.hasCharacter([Entity.charList["wanda"], Entity.charList["bill byron"]])

    rel_for_sc_2 = Rel.Relations("Relation for Scene 2")

    ####
    Entity.charList["bill byron"].hasAction(Rule.getVerbList("notice"), Entity.charList["wanda"].name,
                                            scene_2.time + "ev1")
    lookup.append([scene_2.time + "ev1", Entity.charList["bill byron"].name, "action"])

    Entity.charList["wanda"].hasState(Rule.getAdjList("absent"), scene_2.time)
    lookup.append([scene_2.time, Entity.charList["wanda"].name, "state"])

    rel_for_sc_2.sequence(scene_2.time, scene_2.time + "ev1")

    Entity.charList["bill byron"].hasLocation("behind " + Entity.charList["wanda"].name, Rule.getVerbList("sit"),
                                              scene_2.time + "inf1")
    lookup.append([scene_2.time + "inf1", Entity.charList["bill byron"].name, "location"])

    rel_for_sc_2.causedBy(scene_2.time + "ev1", scene_2.time + "inf1")
    # rel_for_sc_2.sequence(startScene1.scene_1.time + "ev2", scene_2.time + "ev1")
    ####


def startScene3():
    scene_3.hasLocation([Entity.locList["school"], Entity.locList["rm13"]])
    scene_3.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"]])

    rel_for_sc_3 = Rel.Relations("Relation for Scene 3")

    ####
    Entity.charList["maddie"].hasState("late to school", scene_3.time + "ev1a")
    lookup.append([scene_3.time + "ev1a", Entity.charList["maddie"].name, "state"])

    Entity.charList["peggy"].hasState("late to school", scene_3.time + "ev1b")
    lookup.append([scene_3.time + "ev1b", Entity.charList["peggy"].name, "state"])

    Entity.charList["maddie"].hasAction(Rule.getVerbList("wait"), Entity.charList["wanda"].name, scene_3.time + "inf1a")
    lookup.append([scene_3.time + "inf1a", Entity.charList["maddie"].name, "action"])

    Entity.charList["peggy"].hasAction(Rule.getVerbList("wait"), Entity.charList["wanda"].name, scene_3.time + "inf1b")
    lookup.append([scene_3.time + "inf1b", Entity.charList["peggy"].name, "action"])

    Entity.charList["wanda"].hasState(Rule.getVerbList("absent"), scene_3.time + "inf2")
    lookup.append([scene_3.time + "inf2", Entity.charList["wanda"].name, "state"])

    Entity.charList["peggy"].hasDesire(Rule.getVerbList("bully"), Entity.charList["wanda"].name, scene_3.time + "ev2")
    lookup.append([scene_3.time + "ev2", Entity.charList["peggy"].name, "desire"])

    rel_for_sc_3.causedBy(scene_3.time + "ev1", [scene_3.time + "inf1", scene_3.time + "inf2"])
    rel_for_sc_3.causedBy(scene_3.time + "inf1", scene_3.time + "ev2")
    ####

    ####
    Entity.charList["peggy"].hasLocation(Entity.locList["front row"], Rule.getVerbList("sit"), scene_3.time + "inf4")
    lookup.append([scene_3.time + "inf4", Entity.charList["peggy"].name, "location"])

    Entity.charList["maddie"].hasLocation(Entity.locList["front row"], Rule.getVerbList("sit"), scene_3.time + "inf5")
    lookup.append([scene_3.time + "inf5", Entity.charList["maddie"].name, "location"])

    Rule.assignPropBySeating(Entity.charList["maddie"], scene_3.time + "inf6")
    lookup.append([scene_3.time + "inf6", Entity.charList["maddie"].name, "property"])

    Rule.assignPropBySeating(Entity.charList["peggy"], scene_3.time + "inf7")
    lookup.append([scene_3.time + "inf7", Entity.charList["peggy"].name, "property"])

    Entity.charList["peggy"].hasProperty("pretty", scene_3.time + "inf8")
    lookup.append([scene_3.time + "inf8", Entity.charList["peggy"].name, "property"])

    Entity.charList["peggy"].hasAttribute(Entity.itemList["clothes"], Rule.getVerbList("wear"),
                                          scene_3.time + "inf9").hasProperty(
        ["many", "pretty"], scene_3.time + "inf9ext")
    lookup.append([scene_3.time + "inf9", Entity.charList["peggy"].name, "attribute"])

    Entity.charList["peggy"].hasProperty("popular", scene_3.time + "inf10")
    lookup.append([scene_3.time + "inf10", Entity.charList["peggy"].name, "property"])

    rel_for_sc_3.causedBy(scene_3.time + "inf10", [scene_3.time + "inf8", scene_3.time + "inf9"])

    # ent.itemList["friend"]_peg = item("ent.charList["maddie"]")
    # ent.itemList["friend"]_mad = item("ent.charList["peggy"]")
    # ent.itemList["friend"]_peg.hasProperty("best ent.itemList["friend"]")
    # ent.itemList["friend"]_mad.hasProperty("best ent.itemList["friend"]")
    # ent.charList["maddie"].hasAttribute(ent.itemList["friend"]_mad, "has")
    # ent.charList["peggy"].hasAttribute(ent.itemList["friend"]_peg, "has")("behind " + ent.charList["wanda"].name, "sit", scene_2.time + "inf1")
    ####


def startScene4():
    scene_4.hasLocation([Entity.locList["school"], Entity.locList["rm13"]])
    scene_4.hasCharacter(
        [Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"], Entity.charList["people"],
         Entity.charList["svenson"]])

    rel_for_sc_4 = Rel.Relations("Relation for Scene 4")

    ####
    Entity.charList["wanda"].hasLocation(Entity.itemList["frame house"], Rule.getVerbList("live"), scene_4.time + "ev1")
    lookup.append([scene_4.time + "ev1", Entity.charList["wanda"].name, "location"])

    Rule.checkIfPersonIsPoor(Entity.charList["wanda"], scene_4.time + "inf2")
    lookup.append([scene_4.time + "inf2", Entity.charList["wanda"].name, "property"])

    rel_for_sc_4.causedBy(scene_4.time + "ev1", scene_4.time + "inf2")
    ####

    ####
    Entity.charList["wanda"].hasAttribute(Entity.itemList["mother"], Rule.getVerbList("have"),
                                          scene_4.time + "inf3").hasProperty("no", scene_4.time + "inf3ext")
    lookup.append([scene_4.time + "inf3", Entity.charList["wanda"].name, "attribute"])

    Entity.charList["svenson"].hasLocation(Entity.locList["svenson house"], "live",
                                           scene_4.time + "inf6").hasProperty("yellow", scene_4.time + "inf6ext")
    lookup.append([scene_4.time + "inf6", Entity.charList["svenson"].name, "location"])

    Entity.charList["people"].hasAction("avoid", Entity.locList["svenson house"].name, scene_4.time + "inf4")
    lookup.append([scene_4.time + "inf4", Entity.charList["people"].name, "action"])

    Entity.charList["people"].hasAction("gossip", Entity.charList["svenson"].name, scene_4.time + "inf5")
    lookup.append([scene_4.time + "inf5", Entity.charList["people"].name, "action"])

    rel_for_sc_4.causedBy(scene_4.time + "inf4", scene_4.time + "inf5")
    ####


def startScene5():
    scene_5.hasLocation([Entity.locList["school"], Entity.locList["rm13"]])
    scene_5.hasCharacter(
        [Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"], Entity.charList["girls"]])

    rel_for_sc_5 = Rel.Relations("Relation for Scene 5")

    ####
    Entity.charList["wanda"].hasAttribute(Entity.itemList["name"],
                                          "has", scene_5.time + "inf1").hasProperty(["weird", "not easy to say"],
                                                                                    scene_5.time + "inf1ext")
    lookup.append([scene_5.time + "inf1", Entity.charList["wanda"].name, "attribute"])

    rel_for_sc_5.causedBy(scene_1.time + "inf1", scene_5.time + "inf1")
    ####

    ####
    Entity.charList["wanda"].hasAttribute(Entity.itemList["dress"],
                                          "wear", scene_5.time + "inf2").hasProperty(["blue", "not ironed properly"],
                                                                                     scene_5.time + "inf2ext")
    lookup.append([scene_5.time + "inf2", Entity.charList["wanda"].name, "attribute"])

    rel_for_sc_5.causedBy(scene_5.time + "inf2", scene_4.time + "inf3")
    ####

    ####
    Entity.charList["girls"].hasLocation(Entity.locList["oliver street"], Rule.getVerbList("wait"),
                                         scene_5.time + "ev1")
    lookup.append([scene_5.time + "ev1", Entity.charList["girls"].name, "location"])

    Entity.charList["girls"].hasAction("bully", Entity.charList["wanda"].name, scene_5.time + "ev2")
    lookup.append([scene_5.time + "ev2", Entity.charList["girls"].name, "action"])

    rel_for_sc_5.causedBy(scene_5.time + "ev1", scene_5.time + "ev2")
    rel_for_sc_5.causedBy(scene_5.time + "ev2",
                          [scene_5.time + "inf1", scene_5.time + "inf2", scene_1.time + "inf3"])
    ####

    ####
    Entity.charList["wanda"].hasAction(Rule.getVerbList("say"), "something", scene_5.time + "ev3")
    lookup.append([scene_5.time + "ev3", Entity.charList["wanda"].name, "action"])

    Entity.charList["wanda"].hasAttribute(Entity.itemList["hun dresses"], Rule.getVerbList("have"), scene_5.time)
    lookup.append([scene_5.time, Entity.charList["wanda"].name, "attribute"])

    rel_for_sc_5.causedBy(scene_5.time + "ev3", scene_5.time)

    Entity.charList["girls"].hasAction(Rule.getVerbList("believe", negator="not"), "Wanda's statement",
                                       scene_5.time + "ev4")
    lookup.append([scene_5.time + "ev4", Entity.charList["girls"].name, "action"])

    Entity.charList["wanda"].hasAttribute(Entity.itemList["hun dresses"], Rule.getVerbList("have"), scene_5.time)
    lookup.append([scene_5.time, Entity.charList["wanda"].name, "attribute"])
    rel_for_sc_5.causedBy(scene_5.time + "ev4", [scene_5.time + "ev3", scene_5.time])

    rel_for_sc_5.causedBy(scene_5.time + "ev2", [scene_5.time + "ev3", scene_5.time + "ev4"])
    ####


def startScene6():
    scene_6.hasLocation([Entity.locList["school"], Entity.locList["rm13"]])
    scene_6.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["girls"]])

    rel_for_sc_6 = Rel.Relations("Relation for Scene 6")

    ####
    Entity.charList["maddie"].hasState(Rule.getAdjList("guilty"), scene_6.time + "ev1")
    lookup.append([scene_6.time + "ev1", Entity.charList["maddie"].name, "state"])

    rel_for_sc_6.causedBy(scene_6.time + "ev1", scene_5.time + "ev2")
    ####

    ####
    Entity.charList["maddie"].hasProperty("poor", scene_6.time + "inf1")
    lookup.append([scene_6.time + "inf1", Entity.charList["maddie"].name, "property"])

    Entity.charList["maddie"].hasAttribute(Entity.itemList["clothes"],
                                           Rule.getVerbList("wear"), scene_6.time + "inf2").hasProperty(
        "peggy's hand-me-down", scene_6.time + "inf2ext")
    lookup.append([scene_6.time + "inf2", Entity.charList["maddie"].name, "attribute"])

    Entity.charList["maddie"].hasAction(Rule.getVerbList("sympathize"), Entity.charList["wanda"].name,
                                        scene_6.time + "ev2")
    lookup.append([scene_6.time + "ev2", Entity.charList["maddie"].name, "action"])

    rel_for_sc_6.causedBy(scene_6.time + "ev1", scene_6.time + "ev2")
    rel_for_sc_6.causedBy(scene_6.time + "ev2", [scene_6.time + "inf1", scene_6.time + "inf2"])
    ####

    ####
    Entity.charList["girls"].hasAction(Rule.getVerbList("bully", negator="not"), Entity.charList["maddie"].name,
                                       scene_6.time + "ev3")
    lookup.append([scene_6.time + "ev3", Entity.charList["girls"].name, "action"])

    Entity.charList["maddie"].hasAttribute(
        Entity.itemList["name"], Rule.getVerbList("have"), scene_6.time + "inf3").hasProperty(
        ["not weird", "not hard to say"], scene_6.time + "inf3ext")
    lookup.append([scene_6.time + "inf3", Entity.charList["maddie"].name, "attribute"])

    Entity.charList["maddie"].hasLocation("not Boggins Heights", Rule.getVerbList("live"), scene_6.time + "inf4")
    lookup.append([scene_6.time + "inf4", Entity.charList["maddie"].name, "location"])

    rel_for_sc_6.causedBy(scene_6.time + "ev3", [scene_6.time + "inf3", scene_6.time + "inf4"])
    ####

    ####
    Entity.charList["maddie"].hasState(Rule.getAdjList("guilty"), scene_6.time + "ev4")
    lookup.append([scene_6.time + "ev4", Entity.charList["maddie"].name, "state"])

    Entity.charList["maddie"].hasAction(Rule.getVerbList("defend", negator="not"), Entity.charList["wanda"].name,
                                        scene_6.time + "inf5")
    lookup.append([scene_6.time + "inf5", Entity.charList["maddie"].name, "action"])

    rel_for_sc_6.causedBy(scene_6.time + "ev4", scene_6.time + "inf5")
    ####


def startScene7():
    scene_7.hasLocation([Entity.locList["school"], Entity.locList["rm13"]])
    scene_7.hasCharacter(
        [Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["cecile"], Entity.charList["peggy"],
         Entity.charList["girls"]])

    rel_for_sc_7 = Rel.Relations("Relation for Scene 7")

    ####
    Entity.charList["maddie"].hasState(Rule.getAdjList("troubled"), scene_7.time + "ev1")
    lookup.append([scene_7.time + "ev1", Entity.charList["maddie"].name, "state"])

    rel_for_sc_7.causedBy(scene_7.time + "ev1", [scene_3.time + "ev1", scene_6.time + "ev1"])
    ####

    ####
    Entity.charList["maddie"].hasAction(Rule.getVerbList("think"), Entity.charList["wanda"].name, scene_7.time + "ev2")
    lookup.append([scene_7.time + "ev2", Entity.charList["maddie"].name, "action"])

    Entity.charList["maddie"].hasAction(Rule.getVerbList("think"), Entity.itemList["game"].name, scene_7.time + "ev3")
    lookup.append([scene_7.time + "ev3", Entity.charList["maddie"].name, "action"])

    rel_for_sc_7.causedBy(scene_7.time + "ev1", [scene_7.time + "ev2", scene_7.time + "ev3"])
    ####

    ####
    Entity.itemList["game"].hasState(Rule.getAdjList("start"), scene_7.time + "ev4")
    lookup.append([scene_7.time + "ev4", Entity.itemList["game"].name, "state"])

    Entity.charList["cecile"].hasAction(Rule.getVerbList("wear"),
                                        Entity.itemList["dress"].hasProperty(["pretty", "red"], scene_7.time),
                                        scene_7.time + "ev5")
    lookup.append([scene_7.time + "ev5", Entity.charList["cecile"].name, "action"])

    Entity.charList["girls"].hasAction(Rule.getVerbList("admire"), Entity.charList["cecile"].name, scene_7.time + "ev6")
    lookup.append([scene_7.time + "ev6", Entity.charList["girls"].name, "action"])

    Entity.charList["cecile"].hasAttribute(Entity.itemList["clothes"],
                                           Rule.getVerbList("wear"), scene_7.time + "inf1").hasProperty(
        "prettier than others", scene_7.time + "inf1ext")
    lookup.append([scene_7.time + "inf1", Entity.charList["cecile"].name, "attribute"])

    Entity.charList["cecile"].hasProperty(["tall", "slender"], scene_7.time + "inf2")
    lookup.append([scene_7.time + "inf2", Entity.charList["cecile"].name, "property"])

    rel_for_sc_7.causedBy(scene_7.time + "ev4", [scene_7.time + "ev5", scene_7.time + "ev6"])
    rel_for_sc_7.causedBy(scene_7.time + "ev6", [scene_7.time + "inf1", scene_7.time + "inf2"])
    ####

    ####
    Entity.charList["wanda"].hasDesire(Rule.getVerbList("join"), Entity.charList["girls"].name, scene_7.time + "ev8")
    lookup.append([scene_7.time + "ev8", Entity.charList["wanda"].name, "desire"])

    rel_for_sc_7.causedBy(scene_5.time + "ev3", scene_7.time + "ev8")

    Entity.charList["peggy"].hasAction(Rule.getVerbList("tease"), Entity.charList["wanda"].name, scene_7.time + "ev9")
    lookup.append([scene_7.time + "ev9", Entity.charList["peggy"].name, "action"])

    rel_for_sc_7.causedBy(scene_7.time + "ev9", scene_5.time + "ev3")
    ####


def startScene8():
    scene_8.hasLocation([Entity.locList["school"], Entity.locList["rm13"]])
    scene_8.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"]])

    rel_for_sc_8 = Rel.Relations("Relation for Scene 8")

    ####
    Entity.charList["maddie"].hasDesire(Rule.getVerbList("wish"), "stop" + Entity.charList["peggy"].name,
                                        scene_8.time + "ev1")
    lookup.append([scene_8.time + "ev1", Entity.charList["maddie"].name, "desire"])

    Entity.charList["peggy"].hasAction(Rule.getVerbList("bully"), Entity.charList["wanda"].name, scene_8.time + "ev1a")
    lookup.append([scene_8.time + "ev1a", Entity.charList["peggy"].name, "action"])

    rel_for_sc_8.causedBy(scene_8.time + "ev1", scene_8.time + "ev1a")

    Entity.charList["maddie"].hasAction(Rule.getVerbList("write"), Entity.itemList["note"].name, scene_8.time + "ev2")
    lookup.append([scene_8.time + "ev2", Entity.charList["maddie"].name, "action"])

    rel_for_sc_8.causedBy(scene_8.time + "ev2", scene_8.time + "ev1")
    ####

    ####
    Entity.charList["maddie"].hasAction(Rule.getVerbList("destroy"), Entity.itemList["note"].name, scene_8.time + "ev3")
    lookup.append([scene_8.time + "ev3", Entity.charList["maddie"].name, "action"])

    Entity.charList["maddie"].hasDesire(Rule.getVerbList("want", negator="not"),
                                        "argue with " + Entity.charList["peggy"].name, scene_8.time + "ev4")
    lookup.append([scene_8.time + "ev4", Entity.charList["maddie"].name, "desire"])

    Entity.charList["peggy"].hasAction("hate", Entity.charList["maddie"].name, scene_8.time + "ev4a")
    lookup.append([scene_8.time + "ev4a", Entity.charList["peggy"].name, "action"])

    rel_for_sc_8.causedBy(scene_8.time + "ev3", [scene_8.time + "ev4", scene_8.time + "ev4a"])
    ####


def startScene9():
    scene_9.hasLocation([Entity.locList["school"], Entity.locList["rm13"]])
    scene_9.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"]])

    rel_for_sc_9 = Rel.Relations("Relation for Scene 9")

    ####
    Entity.charList["wanda"].hasAction(Rule.getVerbList("struggle"), "read paragraphs",
                                       scene_9.time + "ev1")

    lookup.append([scene_9.time + "", Entity.charList["wanda"].name, "action"])

    Entity.charList["wanda"].hasProperty("timid", scene_9.time + "inf1")
    lookup.append([scene_9.time + "inf1", Entity.charList["wanda"].name, "property"])

    Entity.charList["wanda"].hasProperty("not smart", scene_9.time + "inf2")
    lookup.append([scene_9.time + "inf2", Entity.charList["wanda"].name, "property"])

    rel_for_sc_9.causedBy(scene_9.time + "ev1", [scene_9.time + "inf1", scene_9.time + "inf2"])
    ####

    # ent.charList["wanda"].hasAction("describe", ent.itemList["dress"].hasProperty(["pale blue", "with cerise-colored trimmings"]), scene_9.time + "ev2")
    # ent.charList["wanda"].hasAction("describe", ent.itemList["dress"].hasProperty(["jungle green", "with red sash"]), scene_9.time + "ev3")

    ####
    Entity.charList["peggy"].hasProperty("artistic", scene_9.time + "ev2")
    lookup.append([scene_9.time + "ev2", Entity.charList["peggy"].name, "property"])

    Entity.charList["maddie"].hasAction(Rule.getAdjList("know"), "winner", scene_9.time + "ev3")
    lookup.append([scene_9.time + "ev3", Entity.charList["maddie"].name, "action"])

    Entity.charList["peggy"].hasAction(Rule.getVerbList("win"), Entity.itemList["drawing contest"].name,
                                       scene_9.time + "ev4")
    lookup.append([scene_9.time, Entity.charList["peggy"].name, "action"])

    rel_for_sc_9.causedBy(scene_9.time + "ev3", [scene_9.time + "ev4", scene_9.time + "ev2"])
    ####


def startScene10():
    scene_10.hasLocation([Entity.locList["school"], Entity.locList["rm13"]])
    scene_10.hasCharacter(
        [Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"], Entity.charList["miss mason"]])

    rel_for_sc_10 = Rel.Relations("Relation for Scene 10")

    ####
    Entity.charList["maddie"].hasState(Rule.getAdjList("shocked"), scene_10.time + "ev1a")
    lookup.append([scene_10.time + "ev1a", Entity.charList["maddie"].name, "state"])

    Entity.charList["peggy"].hasState(Rule.getAdjList("shocked"), scene_10.time + "ev1b")
    lookup.append([scene_10.time + "ev1b", Entity.charList["peggy"].name, "state"])

    Entity.locList["rm13"].hasAttribute(Entity.itemList["drawing"].hasProperty(["100 pieces", "pretty"],
                                                                               scene_10.time + "inf1ext"),
                                        Rule.getVerbList("post"), scene_10.time + "inf1")
    lookup.append([scene_10.time + "inf1", Entity.locList["rm13"].name, "attribute"])

    rel_for_sc_10.causedBy(scene_10.time + "ev1", scene_10.time + "inf1")
    ####

    ####
    Entity.charList["miss mason"].hasAction(Rule.getVerbList("announce"), "winner", scene_10.time + "ev2")
    lookup.append([scene_10.time + "ev2", Entity.charList["miss mason"].name, "action"])

    Entity.charList["wanda"].hasAction(Rule.getVerbList("win"), Entity.itemList["drawing contest"].name,
                                       scene_10.time + "ev6")
    lookup.append([scene_10.time + "ev6", Entity.charList["wanda"].name, "action"])

    rel_for_sc_10.sequence(scene_10.time + "ev2", scene_10.time + "ev6")

    Entity.charList["wanda"].hasAction(Rule.getVerbList("submit"),
                                       Entity.itemList["drawing"].hasProperty(["100 pieces", "pretty"],
                                                                              scene_10.time + "ev3ext"),
                                       scene_10.time + "ev3")
    lookup.append([scene_10.time + "ev3", Entity.charList["wanda"].name, "action"])

    rel_for_sc_10.causedBy(scene_10.time + "ev2", scene_10.time + "ev3")
    ####

    ####
    Entity.charList["wanda"].hasAction(Rule.getVerbList("receive", negator="not"), Entity.itemList["medal"].name,
                                       scene_10.time + "ev4")
    lookup.append([scene_10.time + "ev4", Entity.charList["wanda"].name, "action"])

    Entity.charList["wanda"].hasState(Rule.getAdjList("absent"), scene_10.time + "ev5")
    lookup.append([scene_10.time + "ev5", Entity.charList["wanda"].name, "state"])

    rel_for_sc_10.causedBy(scene_10.time + "ev4", scene_10.time + "ev5")
    ####


def startScene11():
    scene_11.hasLocation([Entity.locList["school"], Entity.locList["rm13"]])
    scene_11.hasCharacter([Entity.charList["wanda"], Entity.charList["students"], Entity.charList["miss mason"]])

    rel_for_sc_11 = Rel.Relations("Relation for Scene 11")

    ####
    Entity.charList["miss mason"].hasAction(Rule.getVerbList("receive"), Entity.itemList["note"].name,
                                            scene_11.time + "ev1")
    lookup.append([scene_11.time + "ev1", Entity.charList["miss mason"].name, "action"])

    Entity.charList["miss mason"].hasState(Rule.getAdjList("serious"), scene_11.time + "ev2")
    lookup.append([scene_11.time + "ev2", Entity.charList["miss mason"].name, "state"])

    Entity.charList["wanda"].hasState(Rule.getAdjList("hurt"), scene_11.time + "inf1")
    lookup.append([scene_11.time + "inf1", Entity.charList["wanda"].name, "state"])

    Entity.itemList["note"].hasPurpose(Rule.getVerbList("say"), Entity.charList["wanda"].name + "'s wherabouts",
                                       scene_11.time + "ev3")
    lookup.append([scene_11.time + "ev3", Entity.itemList["note"].name, "action"])

    Entity.charList["wanda"].hasAction(Rule.getVerbList("move"), "town", scene_11.time)
    lookup.append([scene_11.time, Entity.charList["wanda"].name, "action"])

    rel_for_sc_11.sequence(scene_11.time + "ev3", scene_11.time)

    rel_for_sc_11.causedBy(scene_11.time + "ev3", scene_11.time + "inf1")
    rel_for_sc_11.causedBy(scene_11.time + "inf1", scene_5.time + "ev2")
    rel_for_sc_11.causedBy(scene_11.time + "ev2", [scene_11.time + "ev1", scene_11.time + "ev3"])
    rel_for_sc_11.causedBy(scene_11.time + "ev3", scene_5.time + "ev2")
    ####

    ####
    Entity.charList["miss mason"].hasAction(Rule.getVerbList("defend"), Entity.charList["students"].name,
                                            scene_11.time + "ev4")
    lookup.append([scene_11.time + "ev4", Entity.charList["miss mason"].name, "action"])

    Entity.charList["miss mason"].hasAction("state", Entity.charList["students"].name + "' defense",
                                            scene_11.time + "ev6")
    lookup.append([scene_11.time + "ev6", Entity.charList["miss mason"].name, "action"])

    Entity.charList["students"].hasAction(Rule.getVerbList("desire", negator="not"),
                                          "sadden " + Entity.charList["wanda"].name, scene_11.time + "ev7")
    lookup.append([scene_11.time + "ev7", Entity.charList["students"].name, "action"])

    rel_for_sc_11.causedBy(scene_11.time + "ev6", scene_11.time + "ev7")

    Entity.charList["miss mason"].hasAction(Rule.getVerbList("talk"), Entity.charList["students"].name,
                                            scene_11.time + "ev5")
    lookup.append([scene_11.time + "ev5", Entity.charList["miss mason"].name, "action"])

    Entity.charList["students"].hasAction(Rule.getVerbList("reflect"), Entity.itemList["note"].name,
                                          scene_11.time + "ev7"),
    lookup.append([scene_11.time + "ev6", Entity.charList["students"].name, "action"])

    rel_for_sc_11.sequence(scene_11.time + "ev5", scene_11.time + "ev7")

    rel_for_sc_11.causedBy(scene_11.time + "ev4", scene_11.time + "ev6")
    rel_for_sc_11.causedBy(scene_11.time + "ev5", scene_11.time + "ev3")
    ####


def startScene12():
    scene_12.hasLocation([Entity.locList["school"], Entity.locList["rm13"]])
    scene_12.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"]])

    rel_for_sc_12 = Rel.Relations("Relation for Scene 12")

    ####
    Entity.charList["maddie"].hasState(Rule.getAdjList("distracted"), scene_12.time + "ev1")
    lookup.append([scene_12.time + "ev1", Entity.charList["maddie"].name, "state"])

    Entity.charList["maddie"].hasState(Rule.getAdjList("sick"), scene_12.time + "ev2")
    lookup.append([scene_12.time + "ev2", Entity.charList["maddie"].name, "state"])

    rel_for_sc_12.causedBy(scene_11.time + "ev3", [scene_12.time + "ev1", scene_12.time + "ev2"])
    ####

    ####
    Entity.charList["maddie"].hasAction(Rule.getVerbList("defend", negator="not"), Entity.charList["wanda"].name,
                                        scene_12.time + "ev4")
    lookup.append([scene_12.time + "ev4", Entity.charList["maddie"].name, "action"])

    Entity.charList["maddie"].hasAction(Rule.getAdjList("sorry"), "actions", scene_12.time + "ev5")
    lookup.append([scene_12.time + "ev5", Entity.charList["maddie"].name, "state"])

    rel_for_sc_12.causedBy(scene_12.time + "ev5", scene_11.time + "ev4")

    Entity.charList["girls"].hasAction(Rule.getVerbList("bully"), Entity.charList["wanda"].name,
                                       scene_12.time),

    Entity.charList["maddie"].hasAction(Rule.getVerbList("condone", negator="not"), "bullying", scene_12.time + "inf1")
    lookup.append([scene_12.time + "inf1", Entity.charList["maddie"].name, "action"])

    rel_for_sc_12.contradiction(scene_12.time + "ev5", scene_12.time + "ev4")
    rel_for_sc_12.causedBy(scene_12.time + "ev4", scene_8.time + "ev4")
    rel_for_sc_12.causedBy([scene_12.time + "ev1", scene_12.time + "ev2"], scene_12.time + "ev4")
    rel_for_sc_12.causedBy(scene_12.time + "inf1", scene_11.time + "inf1")
    ####


def startScene13():
    scene_13.hasLocation([Entity.locList["school"], Entity.locList["rm13"]])
    scene_13.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"]])

    rel_for_sc_13 = Rel.Relations("Relation for Scene 13")

    ####
    Entity.charList["maddie"].hasDesire(Rule.getVerbList("apologize"), Entity.charList["wanda"].name,
                                        scene_13.time + "ev1")
    lookup.append([scene_13.time + "ev1", Entity.charList["maddie"].name, "desire"])

    Entity.charList["maddie"].hasDesire(Rule.getVerbList("visit"), Entity.charList["wanda"].name, scene_13.time + "ev2")
    lookup.append([scene_13.time + "ev2", Entity.charList["maddie"].name, "desire"])

    rel_for_sc_13.causedBy(scene_13.time + "ev2", scene_13.time + "ev1")
    rel_for_sc_13.causedBy(scene_13.time + "ev1",
                           [scene_6.time + "ev1", scene_12.time + "ev5"])
    ####

    ####
    Entity.charList["peggy"].hasAction(Rule.getVerbList("say"), "request", scene_13.time + "ev3")
    lookup.append([scene_13.time + "ev3", Entity.charList["peggy"].name, "action"])

    Entity.charList["peggy"].hasDesire(Rule.getVerbList("visit"), Entity.charList["wanda"].name, scene_13.time),
    lookup.append([scene_13.time, Entity.charList["peggy"].name, "desire"])

    rel_for_sc_13.sequence(scene_13.time + "ev3", scene_13.time)

    Entity.charList["maddie"].hasState(Rule.getAdjList("overjoyed"), scene_13.time + "ev5")
    lookup.append([scene_13.time + "ev5", Entity.charList["maddie"].name, "state"])

    rel_for_sc_13.causedBy(scene_13.time + "ev5", [scene_13.time + "ev3", scene_13.time + "ev2"])
    ####


def startScene14():
    scene_14.hasLocation([Entity.locList["school"], Entity.locList["boggins heights"]])
    scene_14.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"]])

    rel_for_sc_14 = Rel.Relations("Relation for Scene 14")

    ####
    Entity.charList["maddie"].hasDesire(Rule.getVerbList("go_back"), "time", scene_14.time + "ev1")
    lookup.append([scene_14.time + "ev1", Entity.charList["maddie"].name, "desire"])

    Entity.itemList["game"].hasState(Rule.getVerbList("exist", negator="not"), scene_14.time + "inf1")
    lookup.append([scene_14.time + "inf1", Entity.itemList["game"].name, "state"])

    rel_for_sc_14.causedBy(scene_14.time + "ev1", scene_14.time + "inf1")
    rel_for_sc_14.causedBy(scene_14.time + "inf1", scene_11.time + "ev3")
    ####

    ####
    Entity.charList["peggy"].hasAction(Rule.getVerbList("avoid"), Entity.locList["svenson house"].name,
                                       scene_14.time + "ev5")
    lookup.append([scene_14.time + "ev5", Entity.charList["peggy"].name, "action"])

    Entity.charList["maddie"].hasAction(Rule.getVerbList("avoid"), Entity.locList["svenson house"].name,
                                        scene_14.time + "ev6")
    lookup.append([scene_14.time + "ev6", Entity.charList["maddie"].name, "action"])

    Entity.charList["peggy"].hasDesire(Rule.getVerbList("meet", negator="not"), Entity.charList["svenson"].name,
                                       scene_14.time + "ev7")
    lookup.append([scene_14.time + "ev7", Entity.charList["peggy"].name, "desire"])

    Entity.charList["maddie"].hasDesire(Rule.getVerbList("meet", negator="not"), Entity.charList["svenson"].name,
                                        scene_14.time + "ev8")
    lookup.append([scene_14.time + "ev8", Entity.charList["maddie"].name, "desire"])

    rel_for_sc_14.causedBy(scene_14.time + "ev5", scene_14.time + "ev7")
    rel_for_sc_14.causedBy(scene_14.time + "ev6", scene_14.time + "ev8")
    rel_for_sc_14.causedBy(scene_14.time + "ev7", scene_4.time + "inf5")
    rel_for_sc_14.causedBy(scene_14.time + "ev8", scene_4.time + "inf5")
    ####

    ####
    Entity.charList["maddie"].hasState(Rule.getVerbList("worry"), scene_14.time + "ev9")
    lookup.append([scene_14.time + "ev9", Entity.charList["maddie"].name, "state"])

    Entity.charList["maddie"].hasAction(Rule.getVerbList("meet", negator="might not"), Entity.charList["wanda"].name,
                                        scene_14.time + "inf3")
    lookup.append([scene_14.time + "inf3", Entity.charList["maddie"].name, "action"])

    Entity.charList["maddie"].hasAction(Rule.getVerbList("apologize", negator="might not"),
                                        Entity.charList["wanda"].name,
                                        scene_14.time + "inf1")
    lookup.append([scene_14.time + "inf1", Entity.charList["maddie"].name, "action"])

    rel_for_sc_14.causedBy(scene_14.time + "ev9", scene_14.time + "inf3")
    rel_for_sc_14.causedBy(scene_14.time + "inf1", scene_14.time + "inf3")
    ####


def startScene15():
    scene_15.hasLocation([Entity.locList["school"], Entity.locList["boggins heights"]])
    scene_15.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"]])

    rel_for_sc_15 = Rel.Relations("Relation for Scene 15")

    ####
    Entity.charList["peggy"].hasState([Rule.getAdjList("downcast"), Rule.getAdjList("discouraged")],
                                      scene_15.time + "ev1")
    lookup.append([scene_15.time + "ev1", Entity.charList["peggy"].name, "state"])

    Entity.charList["maddie"].hasState([Rule.getAdjList("downcast"), Rule.getAdjList("discouraged")],
                                       scene_15.time + "ev2")
    lookup.append([scene_15.time + "ev2", Entity.charList["maddie"].name, "state"])

    Entity.itemList["frame house"].hasState(Rule.getAdjList("empty"), scene_15.time + "inf1")
    lookup.append([scene_15.time + "inf1", Entity.itemList["frame house"].name, "state"])

    Entity.charList["peggy"].hasAction(Rule.getVerbList("meet", negator="not"), Entity.charList["wanda"].name,
                                       scene_15.time + "ev3")
    lookup.append([scene_15.time + "ev3", Entity.charList["peggy"].name, "action"])

    Entity.charList["maddie"].hasAction(Rule.getVerbList("meet", negator="not"), Entity.charList["wanda"].name,
                                        scene_15.time + "ev4")
    lookup.append([scene_15.time + "ev4", Entity.charList["maddie"].name, "action"])

    rel_for_sc_15.causedBy(scene_15.time + "ev1", [scene_15.time + "inf1", scene_15.time + "ev3"])
    rel_for_sc_15.causedBy(scene_15.time + "ev2", [scene_15.time + "inf1", scene_15.time + "ev4"])
    ####

    ####
    Entity.charList["peggy"].hasAction(Rule.getVerbList("write"), Entity.itemList["friendly letter"].name,
                                       scene_15.time + "ev5")
    lookup.append([scene_15.time + "ev5", Entity.charList["peggy"].name, "action"])

    Entity.charList["maddie"].hasAction(Rule.getVerbList("write"), Entity.itemList["friendly letter"].name,
                                        scene_15.time + "ev6")
    lookup.append([scene_15.time + "ev6", Entity.charList["maddie"].name, "action"])

    Entity.charList["peggy"].hasDesire(Rule.getVerbList("apologize"), Entity.charList["wanda"].name,
                                       scene_15.time + "ev7")
    lookup.append([scene_15.time + "ev7", Entity.charList["peggy"].name, "desire"])

    Entity.charList["maddie"].hasDesire(Rule.getVerbList("apologize"), Entity.charList["wanda"].name,
                                        scene_15.time + "ev8")
    lookup.append([scene_15.time + "ev8", Entity.charList["maddie"].name, "desire"])

    rel_for_sc_15.causedBy(scene_15.time + "ev5", [scene_15.time + "ev3", scene_15.time + "ev7"])
    rel_for_sc_15.causedBy(scene_15.time + "ev6", [scene_15.time + "ev4", scene_15.time + "ev8"])
    # ent.charList["peggy"].hasAction("hurry", ent.charList["peggy"].hasAction("reach", ent.locList["boggins heights"], scene_15.time), scene_15.time + "ev5")
    # ent.charList["maddie"].hasAction("hurry", ent.charList["maddie"].hasAction("reach", ent.locList["boggins heights"], scene_15.time), scene_15.time + "ev6")
    # ent.charList["peggy"].hasAction("not find", frame_ent.itemList["house"], scene_15.time + "ev7")
    # ent.charList["maddie"].hasAction("not find", frame_ent.itemList["house"], scene_15.time + "ev8")
    ####


def startScene16():
    scene_16.hasLocation([Entity.locList["school"], Entity.locList["rm13"]])
    scene_16.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"]])

    rel_for_sc_16 = Rel.Relations("Relation for Scene 16")

    ####
    Entity.charList["peggy"].hasState([Rule.getAdjList("carefree"), Rule.getAdjList("happy")], scene_16.time + "ev1")
    lookup.append([scene_16.time + "ev1", Entity.charList["peggy"].name, "state"])

    Entity.charList["maddie"].hasState([Rule.getAdjList("carefree"), Rule.getAdjList("happy")], scene_16.time + "ev2")
    lookup.append([scene_16.time + "ev2", Entity.charList["maddie"].name, "state"])

    Entity.charList["peggy"].hasAction(Rule.getVerbList("send"), Entity.itemList["friendly letter"].name,
                                       scene_16.time + "ev3")
    lookup.append([scene_16.time + "ev3", Entity.charList["peggy"].name, "action"])

    Entity.charList["maddie"].hasAction(Rule.getVerbList("send"), Entity.itemList["friendly letter"].name,
                                        scene_16.time + "ev4")
    lookup.append([scene_16.time + "ev4", Entity.charList["maddie"].name, "action"])

    Entity.charList["peggy"].hasAction(Rule.getVerbList("reconcile"), Entity.charList["wanda"].name,
                                       scene_16.time + "ev5")
    lookup.append([scene_16.time + "ev5", Entity.charList["peggy"].name, "action"])

    Entity.charList["maddie"].hasAction(Rule.getVerbList("reconcile"), Entity.charList["wanda"].name,
                                        scene_16.time + "ev6")
    lookup.append([scene_16.time + "ev6", Entity.charList["maddie"].name, "action"])

    rel_for_sc_16.causedBy(scene_16.time + "ev1", scene_16.time + "ev3")
    rel_for_sc_16.causedBy(scene_16.time + "ev2", scene_16.time + "ev4")
    rel_for_sc_16.consequence(scene_16.time + "ev3", [scene_16.time + "ev5", scene_15.time + "ev7"])
    rel_for_sc_16.consequence(scene_16.time + "ev4", [scene_16.time + "ev6", scene_15.time + "ev8"])
    ####

    ####
    Entity.charList["peggy"].hasAction(Rule.getVerbList("understand"), Entity.charList["wanda"].name,
                                       scene_16.time + "ev7")
    lookup.append([scene_16.time + "ev7", Entity.charList["peggy"].name, "action"])

    Entity.charList["maddie"].hasAction(Rule.getVerbList("understand"), Entity.charList["wanda"].name,
                                        scene_16.time + "ev8")
    lookup.append([scene_16.time + "ev8", Entity.charList["maddie"].name, "action"])

    Entity.charList["wanda"].hasAttribute(Entity.itemList["clothes"], Rule.getVerbList("have"),
                                          scene_16.time + "inf1").hasProperty("only one", scene_16.time + "inf1ext")
    lookup.append([scene_16.time + "inf1", Entity.charList["wanda"].name, "attribute"])
    # ent.charList["wanda"].hasAction("iron", ent.itemList["clothes"], scene_16.time + "inf2")

    rel_for_sc_16.causedBy(scene_16.time + "ev7", scene_16.time + "inf1")
    rel_for_sc_16.causedBy(scene_16.time + "ev8", scene_16.time + "inf1")
    rel_for_sc_16.causedBy(scene_16.time + "inf1", scene_4.time + "inf2")
    rel_for_sc_16.causedBy(scene_5.time + "inf2", scene_16.time + "inf1")
    # rel_for_sc_16.causedBy(startScene5.scene_5.time + "inf2", startScene4.scene_4.time + "inf3")
    # rel_for_sc_16.causedBy(scene_16.time + "inf1", startScene5.scene_5.time + "inf2")
    ####


def startScene17():
    scene_17.hasLocation([Entity.locList["school"], Entity.locList["rm13"]])
    scene_17.hasCharacter(
        [Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"], Entity.charList["miss mason"]])

    rel_for_sc_17 = Rel.Relations("Relation for Scene 17")

    ####
    Entity.charList["miss mason"].hasAction(Rule.getVerbList("receive"),
                                            Entity.itemList["letter"].hasProperty("wanda's", scene_17.time + "ev1ext"),
                                            scene_17.time + "ev1")
    lookup.append([scene_17.time + "", Entity.charList["miss mason"].name, "action"])

    Entity.charList["miss mason"].hasAction(Rule.getVerbList("know"), Entity.charList["wanda"].name + " new house",
                                            scene_17.time + "inf1")
    lookup.append([scene_17.time + "inf1", Entity.charList["miss mason"].name, "action"])

    Entity.charList["miss mason"].hasAction(Rule.getVerbList("send", negator="can"), Entity.itemList["medal"].name,
                                            scene_17.time + "ev2")
    lookup.append([scene_17.time + "", Entity.charList["students"].name, "action"])

    rel_for_sc_17.consequence(scene_17.time + "ev1", scene_17.time + "inf1")
    rel_for_sc_17.consequence(scene_17.time + "inf1", scene_17.time + "ev2")
    rel_for_sc_17.causedBy(scene_17.time + "ev2", scene_10.time + "ev4")
    ####

    ####
    Entity.charList["wanda"].hasAction(Rule.getVerbList("forgive"),
                                       [Entity.charList["peggy"].name, Entity.charList["maddie"].name],
                                       scene_17.time + "ev3")
    lookup.append([scene_17.time + "ev3", Entity.charList["wanda"].name, "action"])

    Entity.charList["wanda"].hasAction(Rule.getVerbList("give"),
                                       Entity.itemList["dress"].hasProperty(
                                           ["pale blue", "with cerise-colored trimmings"],
                                           scene_17.time + "ev4ext"),
                                       scene_17.time + "ev4")
    lookup.append([scene_17.time + "ev4", Entity.charList["wanda"].name, "action"])

    Entity.charList["wanda"].hasAction(Rule.getVerbList("give"),
                                       Entity.itemList["dress"].hasProperty(["jungle green", "with red sash"],
                                                                            scene_17.time + "ev5ext"),
                                       scene_17.time + "ev5")
    lookup.append([scene_17.time + "ev5", Entity.charList["wanda"].name, "action"])

    Entity.charList["wanda"].hasAction(Rule.getVerbList("receive"), Entity.itemList["friendly letter"].name,
                                       scene_17.time + "ev6")
    lookup.append([scene_17.time + "ev6", Entity.charList["wanda"].name, "action"])

    rel_for_sc_17.contradiction(scene_17.time + "ev3", scene_5.time + "ev2")
    rel_for_sc_17.causedBy([scene_17.time + "ev4", scene_17.time + "ev5"], scene_17.time + "ev3")
    rel_for_sc_17.causedBy(scene_17.time + "ev3", scene_17.time + "ev6")
    rel_for_sc_17.causedBy(scene_17.time + "ev6",
                           [scene_16.time + "ev3", scene_16.time + "ev4"])
    ####


def startScene18():
    scene_18.hasLocation([Entity.locList["school"], Entity.locList["rm13"]])
    scene_18.hasCharacter([Entity.charList["wanda"], Entity.charList["maddie"], Entity.charList["peggy"]])

    rel_for_sc_18 = Rel.Relations("Relation for Scene 18")

    ####
    Entity.charList["maddie"].hasState(Rule.getAdjList("sad"), scene_18.time + "ev1")
    lookup.append([scene_18.time + "", Entity.charList["maddie"].name, "state"])

    Entity.charList["peggy"].hasState(Rule.getAdjList("guilty", negator="not"), scene_18.time + "ev2")
    lookup.append([scene_18.time + "ev2", Entity.charList["peggy"].name, "state"])

    rel_for_sc_18.causedBy(scene_18.time + "ev1", scene_17.time + "ev4")
    rel_for_sc_18.causedBy(scene_18.time + "ev2", scene_17.time + "ev5")
    ####

    ####
    Entity.charList["maddie"].hasState(Rule.getVerbList("cry"), scene_17.time + "ev3")
    lookup.append([scene_18.time + "ev3", Entity.charList["maddie"].name, "state"])

    rel_for_sc_18.causedBy(scene_18.time + "ev3",
                           [scene_6.time + "inf5", scene_17.time + "ev3"])
    ####

    ####
    Entity.charList["peggy"].hasAction(Rule.getVerbList("understand"), Entity.itemList["hun dresses"].name,
                                       scene_18.time + "ev4")
    lookup.append([scene_18.time + "ev4", Entity.charList["peggy"].name, "action"])

    Entity.charList["maddie"].hasAction(Rule.getVerbList("understand"), Entity.itemList["hun dresses"].name,
                                        scene_18.time + "ev5")
    lookup.append([scene_18.time + "ev5", Entity.charList["maddie"].name, "action"])

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
