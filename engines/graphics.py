class GraphicsEngine:
    def render_state(self, objects):

        for obj in objects:
            if obj.shape == "circle":
                symbol = "●"
            elif obj.shape == "square":
                symbol = "■"
            else:
                symbol = "?"

            print(f"{symbol} {obj.name} at ({obj.x}, {obj.y})")

class test_obj:
    def __init__(self):
        self.x = 10
        self.y = 20
        self.shape = "triangle"
        self.name = "TestObject"

g = GraphicsEngine()
g.render_state([test_obj()])
