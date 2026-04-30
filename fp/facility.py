class Facility:
    """
    Represents one healthcare facility.
    """

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
        self.latitude = row["latitude"]
        self.longitude = row["longitude"]

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