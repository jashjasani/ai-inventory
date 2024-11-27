INVENTORY_PROMPT = """Generate a JSON output that catalogs the count of movable items along with the name of that item, this wil help\
        movers and packers to estimate total items such as furniture and electronics, don't include the items with count zero or that are not present \
        in a given image. The output should be in the format of a JSON object, with name of the item the the count of the item and size of the item \
        your response should only include json."""