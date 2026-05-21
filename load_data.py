import json

def load_person_data():
    file = open("data/person_db.json")
    return json.load(file)

def person_list():
    personlist = []
    for person in load_person_data():
        personlist.append(f"{person['lastname']}, {person['firstname']}")  # ← Nachname, Vorname
    return personlist

def find_person_data_by_name(fullname):
    """Erwartet Format: 'Nachname, Vorname'"""
    nachname, vorname = fullname.split(", ")
    for person in load_person_data():
        if person['firstname'] == vorname and person['lastname'] == nachname:
            return person
    return None