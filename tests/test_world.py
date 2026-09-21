import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from world.world_state import WorldState


world = WorldState()

world.show()

world.update({
    "status": "SUCCESS",
    "skill": "navigate",
    "target": "kitchen"
})

world.show()

world.update({
    "status": "SUCCESS",
    "skill": "grasp",
    "object_id": "red_bottle"
})

world.show()