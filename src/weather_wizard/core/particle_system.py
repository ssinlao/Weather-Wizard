import random


class Particle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def create_particle(self, effect_type, start_x=None):
        # when creating particle, where do we want it to start
        if start_x is None:
            x = random.randint(0, self.width)
        else:
            x = start_x

        if effect_type == "rain":
            return {
                'x': x,
                'y': 0,
                'speed': random.randint(25, 35),
                'type': effect_type
            }
        elif effect_type == "snow":
            return {
                'x': x,
                'y': 0,
                'speed': random.randint(2, 5), # slower than rain
                'drift': random.uniform(-1, 1), # more at an angle
                'type': effect_type
            }
        elif effect_type == "lightning":
            # create lightning branches and itll shoot from ur finger and stuff
            branches = [(x, 0)]
            current_y = 0
            while current_y < self.height:
                new_x = branches[-1][0] + random.randint(-20, 20)
                current_y += random.randint(20, 50)
                branches.append((new_x, current_y))
            return {
                'x': x,
                'y': 0,
                'lifetime': random.randint(5, 10),
                'branches': branches,
                'type': effect_type,
                'flash_intensity': random.uniform(0.1, 0.3)
            }