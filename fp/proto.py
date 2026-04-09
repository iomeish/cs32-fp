import csv

# Categories used in facilities.csv:
# ER, URGENT_CARE, PRIMARY_CARE, COMMUNITY_CLINIC, TELEHEALTH

class Facility:
    def __init__(self, row):
        self.id = row["id"]
        self.name = row["name"]
        self.category = row["category"]
        self.city = row["city"]
        self.address = row["address"]
        self.phone = row["phone"]
        self.walk_in = row["walk_in"]
        self.hours = row["hours"]
        self.cost_level = row["cost_level"]
        self.notes = row["notes"]

    def matches(self, desired_category, desired_city, need_walk_in):
        if self.category != desired_category:
            return False

        if desired_city != "":
            if self.city.lower() != desired_city.lower():
                return False

        if need_walk_in:
            if self.walk_in.lower() != "yes":
                return False

        return True

    def show(self):
        print(f"- {self.name} ({self.category})")
        print(f"  city: {self.city}")
        print(f"  address: {self.address}")
        print(f"  phone: {self.phone}")
        print(f"  hours: {self.hours}")
        print(f"  walk-in: {self.walk_in}")
        print(f"  cost_level: {self.cost_level}")
        if self.notes != "":
            print(f"  notes: {self.notes}")


def load_facilities(filename):
    facilities = []
    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            facilities.append(Facility(row))
    return facilities


def ask_yes_no(prompt):
    while True:
        ans = input(prompt).strip().lower()
        if ans == "y" or ans == "yes":
            return True
        if ans == "n" or ans == "no":
            return False
        print("Please type y or n.")


def choose_care_level():
    print("\nThis prototype is for a class project and is not medical advice.\n")

    emergency = ask_yes_no(
        "Emergency warning signs (chest pain, severe trouble breathing, heavy bleeding, fainting)? (y/n): "
    )
    if emergency:
        return "ER"

    urgent = ask_yes_no(
        "Do you think you need care today (new issue, worsening symptoms, concerning pain/fever/injury)? (y/n): "
    )
    if urgent:
        return "URGENT_CARE"

    ongoing = ask_yes_no(
        "Is this an ongoing or routine issue (checkup, prescription refill, chronic problem)? (y/n): "
    )
    if ongoing:
        return "PRIMARY_CARE"

    return "TELEHEALTH"


def main():
    facilities = load_facilities("fp/facilities.csv")

    desired_category = choose_care_level()

    print("\nOptional filters (press Enter to skip a filter).")
    desired_city = input("City (example: Cambridge): ").strip()

    need_walk_in = ask_yes_no("Do you need walk-in availability? (y/n): ")

    print("\nRecommended options:\n")

    found_any = False
    for facility in facilities:
        if facility.matches(desired_category, desired_city, need_walk_in):
            facility.show()
            print()
            found_any = True

    if not found_any:
        print("No matches found with those filters.")
        print("Try removing the city filter or the walk-in filter, or try a different care level.")


if __name__ == "__main__":
    main()
