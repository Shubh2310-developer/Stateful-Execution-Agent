class AgentException(Exception):
    """Base exception for all agent-related errors."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class PlanningError(AgentException):
    """Raised when the planner fails to generate a valid plan."""
    pass


class ExecutionError(AgentException):
    """Raised when a step execution fails."""
    pass


class StateValidationError(AgentException):
    """Raised when state validation fails."""
    pass


class ValidationError(AgentException):
    """Raised when input or data validation fails."""
    pass


class MemoryError(AgentException):
    """Raised when there is an issue with memory retrieval or storage."""
    pass


class ConfigError(AgentException):
    """Raised when there is a configuration issue."""
    pass


class LLMError(AgentException):
    """Raised when there is an issue with the LLM provider or response."""
    pass
