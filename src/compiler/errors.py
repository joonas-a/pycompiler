class EmptyInputError(Exception):
    pass


class UnexpectedTokenError(Exception):
    def __str__(self):
        return f"{self.args[0]}"
