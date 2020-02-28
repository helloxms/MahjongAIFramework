class PayInfo:

    PAY_TILL_END = 0
    PAYED  = 1
    UNPAYED = 2

    def __init__(self, amount=0, status=0):
        self.amount = amount
        self.status = status

    def update_by_pay(self, amount):
        self.amount += amount

    def update_to_payed(self):
        self.status = self.PAYED

    def update_to_unpayed(self):
        self.status = self.UNPAYED

    # serialize format : [amount, status]
    def serialize(self):
        return [self.amount, self.status]

    @classmethod
    def deserialize(self, serial):
        return self(amount=serial[0], status=serial[1])
