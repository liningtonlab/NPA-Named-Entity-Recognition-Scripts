import sqlite3
import json


def main():
    db_connection = sqlite3.connect("ITIS.sqlite")
    curse = db_connection.cursor()

    # Animal Genera List Generation
    animal_rows = curse.execute(
            "SELECT * FROM taxonomic_units WHERE kingdom_id IS 5"
        )
    animal_genera = []
    for animal in animal_rows:
        animal_genera.append(animal[2])
    unique_animal_genera = list(set(animal_genera))
   # with open("animal_genera.txt", "w", encoding="utf-8") as f_one:
     #   f_one.write(str(sorted(unique_animal_genera)))

    # Plant Genera List Generation
    plant_rows = curse.execute(
            "SELECT * FROM taxonomic_units WHERE kingdom_id IS 3"
        )
    plant_genera = []
    for plant in plant_rows:
        plant_genera.append(plant[2])
    unique_plant_genera = list(set(plant_genera))
    #with open("plant_genera.txt", "w", encoding="utf-8") as f_two:
        #f_two.write(str(sorted(unique_plant_genera)))

    # Microbe Genera List Generation
    microbe_rows = curse.execute(
            "SELECT * FROM taxonomic_units WHERE kingdom_id IS 1 OR kingdom_id IS 2 OR kingdom_id IS 4 OR kingdom_id IS 7"
        )
    microbe_genera = []
    for microbe in microbe_rows:
        microbe_genera.append(microbe[2])
    unique_microbe_genera = list(set(microbe_genera))

    with open("known_microbial_genera_2019-06-21.json", "r") as gen_file:
        data = json.load(gen_file)
        for genera in data:
            known_genera = genera["genus"]
            if known_genera not in unique_microbe_genera:
                unique_microbe_genera.append(known_genera)

    final_microbe_genera = []
    for item in unique_microbe_genera:
        if item not in plant_genera and animal_genera:
            final_microbe_genera.append(item)

    with open("microbe_genera.txt", "w", encoding="utf-8") as f_third:
        f_third.write(str(sorted(final_microbe_genera)))


if __name__ == "__main__":
    main()
