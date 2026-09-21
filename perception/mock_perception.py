from world.object import WorldObject


class MockPerception:

    def detect_objects(self):

        observations = [

            WorldObject(
                object_id="red_bottle",
                object_type="bottle",
                position=[1.2, 0.7, 0.85],
                location="kitchen",
                visible=True,
                graspable=True
            ),

            WorldObject(
                object_id="blue_cup",
                object_type="cup",
                position=[1.5, 0.9, 0.80],
                location="kitchen",
                visible=True,
                graspable=True
            ),

            WorldObject(
                object_id="laptop",
                object_type="laptop",
                position=[-1.0, 2.0, 0.75],
                location="office",
                visible=True,
                graspable=True
            )
        ]

        return observations