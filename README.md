# cs32-fp

## Project: Healthcare Navigation Prototype

Goal: Help a user decide what kind of care they likely need (self-care, primary care, urgent care, or ER) and then recommend the most appropriate nearby option based on urgency and access constraints.

### Current prototype (April milestone)
- Uses a small CSV dataset (`fp/facilities.csv`) representing one limited region (a simple grid).
- Inputs: symptom, severity (1–5), red-flag yes/no, insurance yes/no, current hour, and user location.
- Output: recommended care level + top ranked facilities of that type.

### How ranking works (prototype rules)
Facilities are ranked using:
1) Open now (preferred)
2) Insurance match (preferred when user has insurance)
3) Distance (Manhattan distance on a grid)
4) Availability level (high/medium/low)
5) Cost level (lower is better)

### Scope plan (to keep it realistic)
We will focus on one geographic region for the final project (for example: a single city/area or a single state’s subset of facilities) so the dataset stays manageable and the results are testable.

### “New concept/tool” we will learn
We will learn one additional skill beyond the course core by expanding our data pipeline (for example: adding a second CSV file for symptoms-to-urgency rules, or introducing a small class-based design for facilities and ranking).
