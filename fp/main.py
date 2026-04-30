from load_data import load_facilities
from triage import choose_care_level, explain_care_level
from helpers import ask_yes_no
from filters import recommend_facilities
from map_visualization import create_facility_map


def print_ranked_table(ranked):
    """
    Print a simple ranked table of facility recommendations.
    """
    print(f"{'Rank':<5}{'Score':<8}{'Name':<45}{'City':<15}{'Walk-in':<10}{'Cost':<6}")
    print("-" * 95)

    for i, (score, facility, reasons) in enumerate(ranked[:5], start=1):
        print(
            f"{i:<5}{score:<8}{facility.name[:42]:<45}{facility.city:<15}{facility.walk_in:<10}{facility.cost_level:<6}"
        )


def main():
    facilities = load_facilities("facilities.csv")

    desired_category = choose_care_level()

    print("\nRecommended care level:", desired_category)
    print(explain_care_level(desired_category))

    print("\nOptional filters (press Enter to skip a filter).")
    desired_city = input("City (example: Cambridge): ").strip()
    need_walk_in = ask_yes_no("Do you need walk-in availability? (y/n): ")

    match_type, ranked = recommend_facilities(
        facilities, desired_category, desired_city, need_walk_in
    )

    print("\nRecommended options:\n")

    if len(ranked) == 0:
        print("No facilities found for that care level.")
        return

    if match_type == "fallback":
        print("No exact matches found for all selected filters.")
        print("Showing the best available alternatives in the same care category.\n")

    print_ranked_table(ranked)

    map_file = create_facility_map(ranked)

    if map_file is not None:
        print(f"\nSaved recommendation map to: {map_file}")
        print("Open that HTML file in a browser for the full interactive map.")

    print("\nTop recommendation details:\n")
    for score, facility, reasons in ranked[:3]:
        facility.show()
        print(f"  score: {score}")
        print(f"  why: {', '.join(reasons)}")
        print()


if __name__ == "__main__":
    main()