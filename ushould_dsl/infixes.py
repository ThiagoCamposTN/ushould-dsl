class Infix:
    def __ror__(self, left):
        # other | should
        self.left_value = left
        return self

    def __or__(self, right):
        # should | other
        self.statement  = self.infix_match(right)
    
    def infix_match(self, right):
        raise NotImplementedError()

class Should(Infix):
    def __or__(self, other):
        super().__or__(other)

        try:
            assert self.statement
        except:
            other.message_for_failed_should(self.left_value)
    
    def infix_match(self, right):
        return right.should_match(self.left_value)

class ShouldNot(Infix):
    def __or__(self, other):
        super().__or__(other)

        try:
            assert self.statement
        except:
            other.message_for_failed_should_not(self.left_value)

    def infix_match(self, right):
        return right.should_not_match(self.left_value)

should      = Should()
should_not  = ShouldNot()
