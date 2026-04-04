from core.exceptions import BusinessLogicException


class PaymentAlreadyProcessedException(BusinessLogicException):
    default_detail = "Payment is already confirmed or failed."
    default_code = "payment_already_processed"


class InsufficientStockException(BusinessLogicException):
    default_detail = "Insufficient stock for one or more products."
    default_code = "insufficient_stock"