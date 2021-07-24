class Student:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __repr__(self):
        return f"|name:{self.name}|id:{self.id}|"
