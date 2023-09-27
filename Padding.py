class Padding:
    def __init__(self, padding=10, top=None, bottom=None, left=None, right=None):
        self.top = top if top is not None else padding
        self.bottom = bottom if bottom is not None else padding
        self.left = left if left is not None else padding
        self.right = right if right is not None else padding
