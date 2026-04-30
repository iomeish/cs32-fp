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


def info_row(label, value):
    """
    Return one consistently formatted row for the popup.
    """
    return f"""
    <div style="display: flex; margin-bottom: 6px; line-height: 1.35;">
        <div style="width: 95px; font-weight: bold; color: #222;">{label}</div>
        <div style="flex: 1; color: #333; word-break: break-word;">{value}</div>
    </div>
    """


def facility_popup_html(score, facility, reasons, dist):
    """
    Return nicely formatted HTML for a facility popup.
    """
    if dist is None:
        distance_text = "Distance unavailable"
    else:
        distance_text = f"{dist:.1f} miles away"

    return f"""
    <div style="
        width: 320px;
        font-family: Arial, sans-serif;
        font-size: 13px;
        color: #222;
    ">
        <div style="
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #1f3a5f;
            line-height: 1.25;
            word-break: break-word;
        ">
            {facility.name}
        </div>

        <div style="margin-bottom: 10px;">
            <span style="
                display: inline-block;
                background-color: #eef3ff;
                color: #333;
                padding: 4px 10px;
                border-radius: 10px;
                font-weight: bold;
            ">
                {facility.category}
            </span>
        </div>

        {info_row("City:", facility.city)}
        {info_row("Score:", str(score))}
        {info_row("Distance:", distance_text)}
        {info_row("Walk-in:", facility.walk_in)}
        {info_row("Cost:", facility.cost_level)}
        {info_row("Address:", facility.address)}
        {info_row("Phone:", facility.phone)}

        <div style="
            margin-top: 10px;
            padding: 10px 12px;
            background-color: #f3f3f3;
            border-radius: 8px;
            line-height: 1.4;
            word-break: break-word;
        ">
            <div style="font-weight: bold; margin-bottom: 4px;">Why recommended:</div>
            <div>{", ".join(reasons)}</div>
        </div>
    </div>
    """


def create_facility_map(
    ranked_facilities,
    user_location=None,
    user_label="Your location",
    filename="recommendations_map.html"
):
    """
    Create an interactive HTML map of the top recommended facilities.
    Skip remote facilities with coordinates 0, 0.
    """
    top = ranked_facilities[:5]

    map_points = []
    for score, facility, reasons, dist in top:
        try:
            lat = float(facility.latitude)
            lon = float(facility.longitude)
            if lat == 0 and lon == 0:
                continue
            map_points.append((score, facility, reasons, dist, lat, lon))
        except ValueError:
            continue

    if len(map_points) == 0 and user_location is None:
        return None

    if user_location is not None:
        center_lat = user_location[0]
        center_lon = user_location[1]
    else:
        center_lat = map_points[0][4]
        center_lon = map_points[0][5]

    facility_map = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles=None,
        control_scale=True
    )

    folium.TileLayer(
        tiles="CartoDB positron",
        name="Clean map",
        control=True
    ).add_to(facility_map)

    folium.TileLayer(
        tiles="OpenStreetMap",
        name="Street map",
        control=True
    ).add_to(facility_map)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Tiles © Esri",
        name="Satellite",
        control=True
    ).add_to(facility_map)

    if user_location is not None:
        user_popup = folium.Popup(
            f"""
            <div style="
                width: 200px;
                font-family: Arial, sans-serif;
                font-size: 13px;
                line-height: 1.35;
            ">
                <div style="
                    font-size: 15px;
                    font-weight: bold;
                    margin-bottom: 6px;
                    color: #0b5394;
                ">
                    Your location
                </div>
                <div style="word-break: break-word;">{user_label}</div>
            </div>
            """,
            max_width=240
        )

        folium.CircleMarker(
            location=[user_location[0], user_location[1]],
            radius=9,
            color="black",
            weight=2,
            fill=True,
            fill_color="cyan",
            fill_opacity=1,
            popup=user_popup,
            tooltip="Your location"
        ).add_to(facility_map)

    for score, facility, reasons, dist, lat, lon in map_points:
        popup = folium.Popup(
            facility_popup_html(score, facility, reasons, dist),
            max_width=360
        )

        folium.Marker(
            location=[lat, lon],
            popup=popup,
            tooltip=facility.name,
            icon=folium.Icon(color=marker_color(facility.category), icon="info-sign")
        ).add_to(facility_map)

        if user_location is not None:
            folium.PolyLine(
                locations=[[user_location[0], user_location[1]], [lat, lon]],
                color="blue",
                weight=2,
                opacity=0.45
            ).add_to(facility_map)

    folium.LayerControl(collapsed=False).add_to(facility_map)

    facility_map.save(filename)
    return filename