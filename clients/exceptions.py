from rest_framework.exceptions import APIException


class AddressNotFound(APIException):
    def __init__(self, addresses_ids):
        detail = f"Address(es) {addresses_ids} not found"
        super().__init__(detail=detail, code=404)


class AddressConflitError(APIException):
    def __init__(self):
        detail = 'Main address cannot be set as secondary address'
        super().__init__(detail=detail, code=409)
