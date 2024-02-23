class Mouse:
    def __init__(self):
        self.down = False
        self.up = False
        self.pos = (0, 0)
        self.mbd_pos = (0, 0)
        self.mbu_pos = (0, 0)
        self.clicked = False

    def update_position(self, position):
        self.pos = (position[0], position[1])

    def press_down(self):
        self.mbd_pos = self.pos
        self.down = True
        self.up = False

    def release_up(self):
        if self.down:
            self.down = False
            self.up = True
            self.mbu_pos = self.pos
            print("clicked")
            print("mbd_pos:", self.mbd_pos)
            print("mbu_pos:", self.mbu_pos)
            self.clicked = True
