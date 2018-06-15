import model.story_world.classes.Character as Char
import model.story_world.classes.Item as Item
import model.story_world.classes.Location as Loc

# def generateAllchar.Characteracters():
students = Char.Character("students", "collective", ["Student", "Townsperson"])
girls = Char.Character("girls", "collective", ["Student", "Townsperson"])
wanda = Char.Character("Wanda", "female", ["Student", "Townsperson"])
bill_byron = Char.Character("Bill Byron", "male", ["Student", "Townsperson"])
peggy = Char.Character("Peggy", "female", ["Student", "Townsperson"])
maddie = Char.Character("Maddie", "female", ["Student", "Townsperson"])
people = Char.Character("townspeople", "collective", ["Townsperson"])
svenson = Char.Character("Svenson", "male", ["Townsperson"])
cecile = Char.Character("Cecile", "female", ["Student"])
miss_mason = Char.Character("Miss Mason", "female", ["Townsperson"])
jake_petronski = Char.Character("Jake Petronski", "male", ["Student", "Townsperson"])
jan_petronski = Char.Character("Jan Petronski", "male", ["Townsperson"])
jack_beggles = Char.Character("Jack Beggles", "male", ["Townsperson"])

# Wanda#
wanda.hasRelationship(jake_petronski, "brother")
wanda.hasRelationship(jan_petronski, "father")
wanda.hasRelationship(peggy, ["friend", "classmate"])
wanda.hasRelationship(maddie, ["friend", "classmate"])
wanda.hasRelationship(girls, "classmate")
wanda.hasRelationship(cecile, "classmate")
wanda.hasRelationship(students, "classmate")
wanda.hasRelationship(miss_mason, "teacher")
wanda.hasRelationship(svenson, "neighbor")
wanda.hasRelationship(bill_byron, "classmate")
wanda.hasRelationship(jack_beggles, "classmate")

# Maddie#
maddie.hasRelationship(peggy, ["best friend", "classmate"])
maddie.hasRelationship(wanda, ["friend", "classmate"])
maddie.hasRelationship(girls, "classmate")
maddie.hasRelationship(cecile, "classmate")
maddie.hasRelationship(students, "classmate")
maddie.hasRelationship(miss_mason, "teacher")
maddie.hasRelationship(bill_byron, "classmate")

# Peggy#
peggy.hasRelationship(maddie, ["best friend", "classmate"])
peggy.hasRelationship(wanda, ["friend", "classmate"])
peggy.hasRelationship(girls, "classmate")
peggy.hasRelationship(cecile, "classmate")
peggy.hasRelationship(students, "classmate")
peggy.hasRelationship(miss_mason, "teacher")
peggy.hasRelationship(bill_byron, "classmate")

# Cecile#
cecile.hasRelationship(maddie, ["friend", "classmate"])
cecile.hasRelationship(peggy, ["friend", "classmate"])
cecile.hasRelationship(girls, "classmate")
cecile.hasRelationship(wanda, "classmate")
cecile.hasRelationship(miss_mason, "teacher")
cecile.hasRelationship(students, "classmate")
cecile.hasRelationship(bill_byron, "classmate")

# Bill Byron#
bill_byron.hasRelationship(maddie, "classmate")
bill_byron.hasRelationship(peggy, "classmate")
bill_byron.hasRelationship(girls, "classmate")
bill_byron.hasRelationship(wanda, "classmate")
bill_byron.hasRelationship(students, "classmate")
bill_byron.hasRelationship(miss_mason, "teacher")

# Jack Beggles#
jack_beggles.hasRelationship(maddie, "classmate")
jack_beggles.hasRelationship(peggy, "classmate")
jack_beggles.hasRelationship(girls, "classmate")
jack_beggles.hasRelationship(wanda, "classmate")
jack_beggles.hasRelationship(students, "classmate")
jack_beggles.hasRelationship(miss_mason, "teacher")

# Jake Petronski#
jake_petronski.hasRelationship(wanda, "sister")
jake_petronski.hasRelationship(jan_petronski, "father")
jake_petronski.hasRelationship(people, "neighbor")

# Jan Petronski#
jan_petronski.hasRelationship(wanda, "daughter")
jan_petronski.hasRelationship(jake_petronski, "son")
jan_petronski.hasRelationship(people, "neighbor")

# Svenson#
svenson.hasRelationship(wanda, "neighbor")
svenson.hasRelationship(people, "neighbor")

# Miss Mason#
miss_mason.hasRelationship(maddie, "student")
miss_mason.hasRelationship(peggy, "student")
miss_mason.hasRelationship(wanda, "student")
miss_mason.hasRelationship(girls, "student")
miss_mason.hasRelationship(students, "student")
miss_mason.hasRelationship(bill_byron, "student")
miss_mason.hasRelationship(jack_beggles, "student")

charList = {"students": students, "girls": girls, "wanda": wanda, "bill byron": bill_byron, "peggy": peggy,
            "maddie": maddie, "townspeople": people, "svenson": svenson, "cecile": cecile,
            "miss mason": miss_mason,
            "jake petronski": jake_petronski, "jan petronski": jan_petronski, "jack beggles": jack_beggles}

relList = ["classmate", "teacher", "brother", "sister", "neighbor", "father", "mother", "friend", "student"]

# def generateAllitem.Items():
friend = Item.Item("friend")
grades = Item.Item("grades")
shoes = Item.Item("shoes")
clothes = Item.Item("clothes")
mother = Item.Item("mother")
name = Item.Item("name")
dress = Item.Item("dress")
game = Item.Item("dresses game")
hun_dresses = Item.Item("100 dresses")
note = Item.Item("note")
contest = Item.Item("drawing contest")
drawing = Item.Item("drawing")
medal = Item.Item("medal")
letter = Item.Item("letter")
friendly_letter = Item.Item("friendly letter")

itemList = {"friend": friend, "shoes": shoes, "clothes": clothes, "mother": mother, "name": name, "dress": dress,
            "dresses game": game, "100 dresses": hun_dresses, "note": note, "drawing contest": contest, "drawing": drawing,
            "medal": medal, "letter": letter, "friendly letter": friendly_letter, "grades": grades}

# def generateAllloc.Locationations():
school = Loc.Location("School")
rm13 = Loc.Location("Room 13")
corner_of_room = Loc.Location("corner of the room")
front_row = Loc.Location("front row")
boggins_heights = Loc.Location("Boggins Heights")
boggins_heights_road = Loc.Location("Boggins Heights Road")
neighborhood = Loc.Location("neighborhood")
svenson_house = Loc.Location("Svenson's house")
oliver_street = Loc.Location("Oliver Street")
frame_house = Loc.Location("frame house")

locList = {"school": school, "room 13": rm13, "corner of the room": corner_of_room, "front row": front_row,
           "boggins heights": boggins_heights, "boggins heights road": boggins_heights_road,
           "neighborhood": neighborhood, "svenson's house": svenson_house,
           "oliver street": oliver_street, "frame house": frame_house}
