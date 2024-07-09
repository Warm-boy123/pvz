import objectbase

class ZombieBase(objectbase.ObjectBase):
    def __init__(self, id, pos, row):
        super().__init__(id, pos)
        self.row = row
    pass