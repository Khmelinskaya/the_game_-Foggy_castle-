class Room:

    def __init__(self, title, empty_room_description, descriptions_with_items):
        self.title = title
        self.empty_room_description = empty_room_description
        self.descriptions_with_items = descriptions_with_items
        self.item_id = None
        self.links = [] # связанные комнаты

    def add_link(self, room_to_link):
        self.links.append(room_to_link)

    def put_item(self, item_id):
        self.item_id = item_id

    def remove_item(self):
        self.item_id = None

