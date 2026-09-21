class WorldObject:

    def __init__(
        self,
        object_id,
        object_type,
        position=None,
        location=None,
        visible=False,
        graspable=False
    ):

        self.object_id = object_id
        self.object_type = object_type
        self.position = position
        self.location = location
        self.visible = visible
        self.graspable = graspable

    def to_dict(self):

        return {
            "object_id": self.object_id,
            "type": self.object_type,
            "position": self.position,
            "location": self.location,
            "visible": self.visible,
            "graspable": self.graspable
        }