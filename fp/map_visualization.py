import folium


def marker_color(category):
    """
    Return a marker color based on facility category.
    """
    if category == "ER":
        return "red"
    if category == "URGENT_CARE":
        return "orange"
    if category == "PRIMARY_CARE":
        return "blue"
    if category == "COMMUNITY_CLINIC":
        return "green"
    if category == "TELEHEALTH":
        return "purple"
    return "gray"


def create_facility_map(ranked_facilities, filename="recommendations_map.html"):
    """
    Create an interactive HTML map of the top recommended facilities.
    Skip remote facilities with coordinates 0, 0.
    """
    top = ranked_facilities[:5]

    map_points = []
    for score, facility, reasons in top:
        try:
            lat = float(facility.latitude)
            lon = float(facility.longitude)
            if lat == 0 and lon == 0:
                continue
            map_points.append((score, facility, reasons, lat, lon))
        except ValueError:
            continue

    if len(map_points) == 0:
        return None

    first_lat = map_points[0][3]
    first_lon = map_points[0][4]

    facility_map = folium.Map(
        location=[first_lat, first_lon],
        zoom_start=12,
        tiles="CartoDB positron"
    )

    for score, facility, reasons, lat, lon in map_points:
        popup_text = (
            f"{facility.name}<br>"
            f"Category: {facility.category}<br>"
            f"City: {facility.city}<br>"
            f"Score: {score}<br>"
            f"Why: {', '.join(reasons)}"
        )

        folium.Marker(
            location=[lat, lon],
            popup=popup_text,
            icon=folium.Icon(color=marker_color(facility.category))
        ).add_to(facility_map)

    facility_map.save(filename)
    return filename