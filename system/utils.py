import requests
from .models import Event, Category

def import_dummy_events():
    """
    Fetch sample events from a free API (dummyjson) 
    and save them into the DB as Events.
    """
    url = "https://dummyjson.com/products?limit=5"  # free fake data API
    res = requests.get(url).json()

    cat, _ = Category.objects.get_or_create(
        name="Imported",
        description="Auto-generated from Dummy API"
    )

    for item in res.get("products", []):
        Event.objects.create(
            name=item["title"],
            description=item["description"],
            date="2025-09-15",
            time="18:00",
            location="Online",
            category=cat
        )
