class Student:
    def __init__(self, name, id):
        assert type(name) == str and type(id) == int

        self.name = name
        self.id = id

    def __repr__(self):
        return "{%s:%d}" % (self.name, self.id)
