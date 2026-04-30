# Healthcare Access Navigator

## Author
Ibrahim Omeish

## Project Description
Healthcare Access Navigator is a Python program that helps a user decide what type of medical care may be appropriate based on a short series of questions, then recommends healthcare facilities that match that care level.

The final version can recommend:
- ER
- URGENT_CARE
- PRIMARY_CARE
- COMMUNITY_CLINIC
- TELEHEALTH

After choosing a care level, the program filters facilities based on user preferences such as city and walk-in availability. It also supports optional proximity-based ranking and generates an interactive map of the top recommended facilities.

This project is for educational purposes only and is not medical advice.

## Files
- `main.py` — runs the program
- `facility.py` — defines the `Facility` class
- `load_data.py` — loads facility data from `facilities.csv`
- `helpers.py` — helper functions such as yes/no input handling
- `triage.py` — care-level recommendation logic
- `filters.py` — filtering, scoring, and ranking logic
- `map_visualization.py` — generates the interactive recommendation map
- `test_project.py` — automated tests
- `facilities.csv` — facility dataset

## How to Run
From the project folder, run:
python3 main.py

## How to Test
From the project folder, run:
python3 test_project.py

## Setup
This project uses Python 3 and the packages `folium` and `geopy`.

Install them with:
pip install folium geopy

The program expects `facilities.csv` to be in the same folder as the Python files.

## Viewing the Map
The program saves an interactive map as `recommendations_map.html`.

For best results, open that file in a normal web browser such as Chrome or Safari. Some IDE previews may not render every map tile correctly even when the map file is generated correctly.

## High-Level Design
The program takes in:
- user answers to triage questions
- an optional city filter
- a walk-in preference
- an optional approximate user location for proximity-based ranking

The program outputs:
- a recommended care level
- a ranked table of healthcare facilities
- detailed explanations for the top recommendations
- an interactive HTML map of the top recommended facilities

The main logical components are:
- `triage.py`, which determines the recommended care level
- `load_data.py`, which loads the dataset
- `filters.py`, which filters facilities and assigns recommendation scores
- `map_visualization.py`, which plots facility locations and the optional user location on an interactive map
- `test_project.py`, which verifies core filtering and ranking behavior

## Ranking System
The ranking system is a weighted recommendation heuristic.

Facilities are first restricted to the recommended care category. Then the score is based on:
- city match
- walk-in availability
- cost level
- optional proximity to the user

If no exact match exists for all selected filters, the program falls back to the same care category and ranks the best available alternatives instead of returning only a dead end.

## Testing
The project includes automated tests using `unittest`.

The tests check:
- care-level selection logic
- category filtering
- city filtering
- walk-in filtering
- exact-match recommendation behavior
- fallback recommendation behavior
- distance-based ranking behavior

I also manually tested the project with example runs for ER, urgent care, primary care, community clinic, and telehealth scenarios.

## Data Notes
The facility dataset is intended to support this educational project. Names, addresses, phone numbers, and hours were checked against current provider or clinic pages during development, but real-world healthcare information can change over time.

Latitude and longitude values are approximate address-based coordinates used to support the interactive map.

## External Contributors and Sources

I used CS32 course materials as the main reference for the design and development of this project.

I also used official provider and clinic websites to verify the facility dataset, including sites from:
- Mass General
- Brigham and Women’s Hospital
- Cambridge Health Alliance
- Mount Auburn Hospital
- Beth Israel Deaconess / BILH
- AFC Urgent Care
- CVS MinuteClinic
- NeighborHealth
- Teladoc
- Amwell

I used the following Python libraries and their documentation:
- folium
- geopy

I did not copy and paste code from outside tutorials without reviewing and adapting it to my project.

## Generative AI Use

I used generative AI tools to help me:

- brainstorm how to reorganize my original prototype into multiple files
- think through possible README wording
- think through testing structure and edge cases
- verify whether parts of my code were logically correct
- help debug issues in my program
- identify useful packages to install for new features, especially for mapping and location-based functionality
- think through ranking and visualization ideas

I reviewed, edited, and tested all code myself before using it.

AI-assisted planning influenced the modular structure and refinement of the project, including:

- `facility.py`
- `load_data.py`
- `helpers.py`
- `triage.py`
- `filters.py`
- `map_visualization.py`
- `main.py`
- `test_project.py`

I did not blindly copy and submit code without reviewing it.
