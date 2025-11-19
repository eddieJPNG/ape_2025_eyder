class Calculator:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

        if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
            raise(ValueError("Both x and y must be numbers."))
        
        def add(self):
            return self.x + self.y




x = Calculator(10,5)

x.add()