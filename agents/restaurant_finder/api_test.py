import requests, textwrap

lat, lon, radius = 6.9271, 79.8612, 3000  # Colombo, 1.5km
ql = textwrap.dedent(f"""
[out:json][timeout:25];
(
  node["amenity"~"^(restaurant|fast_food|cafe)$"](around:{radius},{lat},{lon});
  way["amenity"~"^(restaurant|fast_food|cafe)$"](around:{radius},{lat},{lon});
  relation["amenity"~"^(restaurant|fast_food|cafe)$"](around:{radius},{lat},{lon});
);
out center tags;
""").strip()

resp = requests.post(
    "https://overpass-api.de/api/interpreter",
    data={"data": ql},
    headers={"User-Agent": "Cuisinise/1.0 (heshaltempdissanayake@gmail.com)"}
)
resp.raise_for_status()
data = resp.json()

def get_coord(e):
    if e.get("type") == "node":
        return e["lat"], e["lon"]
    c = e.get("center")
    return (c["lat"], c["lon"]) if c else (None, None)

print(f"Found {len(data.get('elements', []))} places")
for e in data.get("elements", [])[:15]:
    tags = e.get("tags", {})
    name = tags.get("name", "(no name)")
    addr = ", ".join(filter(None, [
        tags.get("addr:housenumber"), tags.get("addr:street"),
        tags.get("addr:city"), tags.get("addr:postcode")
    ]))
    oh = tags.get("opening_hours", "—")
    lat, lon = get_coord(e)
    print(f"- {name} [{lat},{lon}] | {addr or '—'} | hours: {oh}")
