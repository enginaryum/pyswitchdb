from switch_client import *
import json

# TAPU DB KEYS
api_key = '61e87e02-3509-4503-971f-fdc90eef8611'
api_secret = 'c7w9rO36knRa87JtSIkK4VPpJqhNglMB6Xau46MN0KDQEDpegR3yfUte9SFuPKDP'

client = SwitchClient(api_key=api_key, api_secret=api_secret, server='tr01')

# Returns created lists
lists = client.lists()
print lists

# Add method
client.add(list_name='test_2', json_data={
    "BookGuid": "2D72BCE5-2897-4C52-BD22-D5079DA5C976",
    "Title": "Lorem Ipsum Dolor",
    "Author": "Sit Amet",
    "IsActive": 1
})

# Update method
client.update(list_name='test_2', list_item_id='593a8dc810a0b00a441ab593', json_data={
    "BookGuid": "2D72BCE5-2897-4C52-BD22-D5079DA5C976",
    "Title": "Lorem Ipsum",
    "Author": "Sit Amet",
    "IsActive": 0
})

# Delete method
client.delete(list_name='test_2', list_item_id="593a8f9410a0b00a441ab595")

# Returns objects in list
list_objects = client.list(list_name="test_2", query={
    "list": "test_2",
    "count": 100,
    "page": 0,
    "where": [],
    "order": {
        "type": "DESC",
        "by": "id"
    }
})
print list_objects
