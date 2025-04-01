import io

import contextily as ctx
import geopandas as gpd
import gpxpy
import matplotlib.pyplot as plt
from shapely.geometry import LineString


# Coordinates are in latitude/longitude (angles)
def highlight_unsafe_segments(file):
    if isinstance(file, str):
        with open(file, "r") as f:
            gpx = gpxpy.parse(f)
    elif isinstance(file, io.BytesIO):
        gpx = gpxpy.parse(file)
    else:
        print("Unsupported file type")
        exit(-1)

    points = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append((point.longitude, point.latitude))

    komoot_line = LineString(points)

    komoot_gdf = gpd.GeoDataFrame(
        {"name": ["Komoot Route"]}, geometry=[komoot_line], crs="EPSG:4326"
    )

    zurich_gdf = gpd.read_file("zurich.geojson")
    if zurich_gdf.crs is None:
        zurich_gdf.crs = "EPSG:4326"

    # Override coordinate system: from now coordinates are in meters

    komoot_gdf = komoot_gdf.to_crs(epsg=3857)
    zurich_gdf = zurich_gdf.to_crs(epsg=3857)

    buffer_distance = 30  # meters
    safe_buffers = zurich_gdf.buffer(buffer_distance)
    safe_buffer_union = safe_buffers.union_all()
    unsafe_segments = komoot_gdf.geometry.iloc[0].difference(safe_buffer_union)
    unsafe_gdf = gpd.GeoDataFrame(geometry=[unsafe_segments], crs=komoot_gdf.crs)

    fig, ax = plt.subplots(figsize=(10, 10))
    zurich_gdf.plot(ax=ax, color="blue", linewidth=1, label="Safe Routes", alpha=0.7)
    komoot_gdf.plot(ax=ax, color="green", linewidth=2, label="Komoot Route")
    unsafe_gdf.plot(ax=ax, color="red", linewidth=3, label="Komoot Route")

    # Get bounding boxes to zoom into the appropriate part of the map

    route_bounds = komoot_gdf.total_bounds
    zurich_bounds = zurich_gdf.total_bounds

    padding = 200  # meters

    if (
        route_bounds[0] >= zurich_bounds[0]
        and route_bounds[1] >= zurich_bounds[1]
        and route_bounds[2] <= zurich_bounds[2]
        and route_bounds[3] <= zurich_bounds[3]
    ):
        # Route completely fits inside the city:
        minx, miny, maxx, maxy = route_bounds
        print("Using route bounds for zooming.")
    else:
        # Route exceeds city limits; restrict to the city bounds:
        minx, miny, maxx, maxy = zurich_bounds
        print("Using city bounds for zooming.")

    minx -= padding
    miny -= padding
    maxx += padding
    maxy += padding

    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

    ctx.add_basemap(
        ax=ax, crs=zurich_gdf.crs, source=ctx.providers.OpenStreetMap.CH, zoom=15
    )

    print("Saving figure as pdf...")
    if __name__ == "__main__":
        plt.show()
        return None
    else:
        return fig


if __name__ == "__main__":
    ctx.set_cache_dir("cache")
    gpx_file = "test1.gpx"
    highlight_unsafe_segments(gpx_file)
