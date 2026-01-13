class CisoApiError(RuntimeError):
    pass


class CisoAuthError(CisoApiError):
    pass


class CisoValidationError(CisoApiError):
    pass
