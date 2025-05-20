INVENTORY_PROMPT = """Generate a JSON output that catalogs the count of movable items along with the name of that item, this wil help
        movers and packers to estimate total items such as furniture and electronics, don't include the items with count zero or that are not present
        in a given image. The output should be in the format of a array of JSON object, with name of the item the the count of the item and size of the item
        your response should only include json. If the image has no furniture or electronics, the output should be an empty JSON object. In case there are no items
        you can reply with {{ "items" : [] }} or if there are items you can reply with {{ "items" : [ {{ "name" : `item_name`, "count" : `item_count`, "size" : `item_size`, 
        inDb : true if in database_items else false, "volume": `approx volume in CFT`, "weight": `approx weight in lbs`  }} ] "room_name" : `name of the room eg(Living room, bedroom)` }}
        There are some items inside the database_items which are : [{items}]

        if items are not provided or if its empty you can make all inDB false

        Please note only use the item name if it matches to the item in the picture completely. The item does not need to be in database you can add new items if not in db. 
        """