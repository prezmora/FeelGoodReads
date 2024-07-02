from db import mood_container

def get_moods():
    query = "SELECT * FROM c"
    items = list(mood_container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    return items

def add_mood(mood):
    mood_id = str(len(get_moods()) + 1)
    mood_container.upsert_item({
        'id': mood_id,
        'mood': mood
    })

def update_mood(mood_id, new_mood):
    item = mood_container.read_item(item=mood_id, partition_key=mood_id)
    item['mood'] = new_mood
    mood_container.upsert_item(item)

def delete_mood(mood_id):
    mood_container.delete_item(item=mood_id, partition_key=mood_id)
