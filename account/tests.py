class Base:
    def __init__(self, name):
        self.name = name


class SecondBase(Base):
    def __init__(self, name):
        self.last_name = name


class ThirdBase(SecondBase):
    def __init__(self, name):
        super().super().__init__(name)


a = ThirdBase('Mamad')
