class CoursePilotError(Exception):
    """Base exception for expected, user-visible failures."""


class ParsingError(CoursePilotError):
    pass


class LLMError(CoursePilotError):
    pass


class ValidationError(CoursePilotError):
    pass
