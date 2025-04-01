# There are many routes through Zurich ...

but not many of them are safe when you're on a bike. Routing apps like Komoot tend to suggest straight routes along Langstrasse, Hardbrücke and Bellevue. If you prefer riding on some quieter roads (well, relatively speaking), but don't know the good roads yet, this app is for you!

## Preferred cycling routes to the rescue

The city government has published so-called ["Velovorzugsrouten" (preferred cycling routes)](https://www.stadt-zuerich.ch/de/mobilitaet/velo/velovorzugsrouten.html) on its website, which are also available as a GeoJSON file. This app overlays the preferred cycling routes over a base image of the city. On top of that, it overlays your route and highlights sections where your route deviates from preferred cycling routes in red. This allows you to make changes to the route in your planner app (Komoot etc), generate a new GPX file and repeat the process until you're happy with the result.

## How to use this app

You can find a hosted version of this app on [streamlit](https://route-zurich.streamlit.app/).

Apps like Komoot generate GPX files containing the route. Simply drag-and-drop the GPX file to the corresopnding element on the website and wait for a few seconds. Then your route along with the preferred cycling routes should appear.