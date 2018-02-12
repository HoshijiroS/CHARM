import model.story_world.classes.Character as Char
import model.story_world.classes.Item as Item
import model.story_world.classes.Location as Loc

# def generateAllchar.Characteracters():
students = Char.Character("Students", ["Student", "Townsperson"])
girls = Char.Character("girls", ["Student", "Townsperson"])
wanda = Char.Character("Wanda", ["Student", "Townsperson"])
bill_byron = Char.Character("Bill Byron", ["Student", "Townsperson"])
peggy = Char.Character("Peggy", ["Student", "Townsperson"])
maddie = Char.Character("Maddie", ["Student", "Townsperson"])
people = Char.Character("townspeople", ["Townsperson"])
svenson = Char.Character("Svenson", ["Townsperson"])
cecile = Char.Character("Cecile", ["Student"])
miss_mason = Char.Character("Miss Mason", ["Townsperson"])
jake_petronski = Char.Character("Jake Petronski", ["Student", "Townsperson"])
jan_petronski = Char.Character("Jan Petronski", ["Townsperson"])
jack_beggles = Char.Character("Jack Beggles", ["Townsperson"])

# Wanda#
wanda.hasRelationship(jake_petronski.name, "brother")
wanda.hasRelationship(jan_petronski.name, "father")
wanda.hasRelationship(peggy.name, ["friend", "classmate"])
wanda.hasRelationship(maddie.name, ["friend", "classmate"])
wanda.hasRelationship(girls.name, "classmate")
wanda.hasRelationship(cecile.name, "classmate")
wanda.hasRelationship(students.name, "classmate")
wanda.hasRelationship(miss_mason.name, "teacher")
wanda.hasRelationship(svenson.name, "neighbor")
wanda.hasRelationship(bill_byron.name, "classmate")

# Maddie#
maddie.hasRelationship(peggy.name, ["best friend", "classmate"])
maddie.hasRelationship(wanda.name, ["friend", "classmate"])
maddie.hasRelationship(girls.name, "classmate")
maddie.hasRelationship(cecile.name, "classmate")
maddie.hasRelationship(students.name, "classmate")
maddie.hasRelationship(miss_mason.name, "teacher")
maddie.hasRelationship(bill_byron.name, "classmate")

# Peggy#
peggy.hasRelationship(maddie.name, ["best friend", "classmate"])
peggy.hasRelationship(wanda.name, ["friend", "classmate"])
peggy.hasRelationship(girls.name, "classmate")
peggy.hasRelationship(cecile.name, "classmate")
peggy.hasRelationship(students.name, "classmate")
peggy.hasRelationship(miss_mason.name, "teacher")
peggy.hasRelationship(bill_byron.name, "classmate")

# Cecile#
cecile.hasRelationship(maddie.name, ["friend", "classmate"])
cecile.hasRelationship(peggy.name, ["friend", "classmate"])
cecile.hasRelationship(girls.name, "classmate")
cecile.hasRelationship(wanda.name, "classmate")
cecile.hasRelationship(miss_mason.name, "teacher")
cecile.hasRelationship(students.name, "classmate")
cecile.hasRelationship(bill_byron.name, "classmate")

# Bill Byron#
bill_byron.hasRelationship(maddie.name, "classmate")
bill_byron.hasRelationship(peggy.name, "classmate")
bill_byron.hasRelationship(girls.name, "classmate")
bill_byron.hasRelationship(wanda.name, "classmate")
bill_byron.hasRelationship(students.name, "classmate")
bill_byron.hasRelationship(miss_mason.name, "teacher")

# Jack Beggles#
jack_beggles.hasRelationship(maddie.name, "classmate")
jack_beggles.hasRelationship(peggy.name, "classmate")
jack_beggles.hasRelationship(girls.name, "classmate")
jack_beggles.hasRelationship(wanda.name, "classmate")
jack_beggles.hasRelationship(students.name, "classmate")
jack_beggles.hasRelationship(miss_mason.name, "teacher")

# Jake Petronski#
jake_petronski.hasRelationship(wanda.name, "sister")
jake_petronski.hasRelationship(jan_petronski.name, "father")
jake_petronski.hasRelationship(people.name, "neighbor")

# Jan Petronski#
jan_petronski.hasRelationship(wanda.name, "daughter")
jan_petronski.hasRelationship(jake_petronski.name, "son")
jan_petronski.hasRelationship(people.name, "neighbor")

# Svenson#
svenson.hasRelationship(wanda.name, "neighbor")
svenson.hasRelationship(people.name, "neighbor")

# Miss Mason#
miss_mason.hasRelationship(maddie.name, "student")
miss_mason.hasRelationship(peggy.name, "student")
miss_mason.hasRelationship(wanda.name, "student")
miss_mason.hasRelationship(girls.name, "student")
miss_mason.hasRelationship(students.name, "student")
miss_mason.hasRelationship(bill_byron.name, "student")
miss_mason.hasRelationship(jack_beggles.name, "student")

charList = {"students": students, "girls": girls, "wanda": wanda, "bill byron": bill_byron, "peggy": peggy,
            "maddie": maddie, "people": people, "svenson": svenson, "cecile": cecile,
            "miss mason": miss_mason,
            "jake petronski": jake_petronski, "jan petronski": jan_petronski, "jack beggles": jack_beggles}

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
            "game": game, "hun dresses": hun_dresses, "note": note, "drawing contest": contest, "drawing": drawing,
            "medal": medal, "letter": letter, "friendly letter": friendly_letter, "grades": grades}

# def generateAllloc.Locationations():
school = Loc.Location("School")
rm13 = Loc.Location("Room 13")
corner_of_room = Loc.Location("corner of the room")
front_row = Loc.Location("front row")
boggins_heights = Loc.Location("Boggins Heights")
boggins_heights_road = Item.Item("road")
neighborhood = Loc.Location("neighborhood")
svenson_house = Loc.Location("Svenson's house")
oliver_street = Loc.Location("Oliver Street")
frame_house = Loc.Location("frame house")

locList = {"school": school, "rm13": rm13, "corner of room": corner_of_room, "front row": front_row,
           "boggins heights": boggins_heights, "boggins heights road": boggins_heights_road,
           "neighborhood": neighborhood, "svenson house": svenson_house,
           "oliver street": oliver_street, "frame house": frame_house}
