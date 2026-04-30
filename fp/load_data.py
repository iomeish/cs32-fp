import csv
from facility import Facility


def load_facilities(filename):
    """
    Load facilities from a CSV file into a list of Facility objects.
    """
    facilities = []

    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            facilities.append(Facility(row))

    return facilities