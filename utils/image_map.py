IMAGE_MAP = {
    #Attractions
    "nine_arch_bridge.txt": {
        "query": "Nine Arch Bridge Ella Sri Lanka railway",
    },
    "little_adams_peak.txt": {
        "query": "Little Adams Peak Ella Sri Lanka hiking",
    },
    "ella_rock.txt": {
        "query": "Ella Rock hiking mountain Sri Lanka",
    },
    "ravana_falls.txt": {
        "query": "Ravana Falls waterfall Sri Lanka",
    },
    "lipton_seat.txt": {
        "query": "tea plantation viewpoint Sri Lanka",
    },
    "ravana_cave.txt": {
        "query": "cave forest Sri Lanka",
    },
    "demodara_loop.txt": {
        "query": "railway train loop Sri Lanka hill country",
    },
    "ella_gap.txt": {
        "query": "mountain valley view Sri Lanka",
    },
    # Hotels (with approximate price per night, from the knowledge base) 
    "98_acres_resort.txt": {
        "query": "luxury resort infinity pool tea plantation",
        "price": "USD 150-300+ per night",
    },
    "ella_flower_garden_resort.txt": {
        "query": "garden resort mountain view Sri Lanka",
        "price": "USD 40-80 per night",
    },
    "zion_view.txt": {
        "query": "guesthouse home cooked breakfast",
        "price": "USD 20-40 per night",
    },
    "ella_jungle_resort.txt": {
        "query": "jungle chalet eco resort",
        "price": "USD 50-100 per night",
    },
    "budget_hostels_ella.txt": {
        "query": "backpacker hostel dorm room",
        "price": "USD 8-25 per night",
    },
    # Transport
    "train_kandy_ella.txt": {
        "query": "scenic train hill country Sri Lanka",
    },
    "bus_routes_ella.txt": {
        "query": "local bus Sri Lanka road",
    },
    "tuk_tuk_ella.txt": {
        "query": "tuk tuk three wheeler Sri Lanka",
    },
    "getting_to_ella.txt": {
        "query": "mountain road trip Sri Lanka",
    },
    # Culture 
    "tea_plantation_culture.txt": {
        "query": "tea plantation workers Sri Lanka",
    },
    "sri_lankan_food_ella.txt": {
        "query": "Sri Lankan rice and curry food",
    },
    "local_etiquette.txt": {
        "query": "Buddhist temple Sri Lanka",
    },
    "festivals_sri_lanka.txt": {
        "query": "Vesak lanterns festival Sri Lanka",
    },
    "history_of_ella.txt": {
        "query": "colonial era railway bridge Sri Lanka",
    },
}


def get_image_info(filename: str) -> dict | None:
    
    return IMAGE_MAP.get(filename)
