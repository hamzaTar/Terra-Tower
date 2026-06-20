class Moneda:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.moneda_w = 5
        self.moneda_h = 5
        self.recogida = False

    def get_Bounds(self):
        return self.x, self.y, self.moneda_w, self.moneda_h

    def recoger(self):
        self.recogida = True