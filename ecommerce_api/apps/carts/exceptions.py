from core.exceptions import BusinessLogicException

class EmptyCartException(BusinessLogicException):
    default_detail = "Cannot checkout an empty cart."


class InsufficientStockException(BusinessLogicException):
    default_detail = "Not enough stock for one or more products."