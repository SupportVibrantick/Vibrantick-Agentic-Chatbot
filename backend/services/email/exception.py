class EmailException(Exception):
    """Base exception for all email-related errors."""
    pass


class EmailConfigurationError(EmailException):
    """Raised when the email provider is misconfigured."""
    pass


class EmailProviderError(EmailException):
    """Raised when the email provider fails."""
    pass


class EmailDeliveryError(EmailException):
    """Raised when an email cannot be delivered."""
    pass


class EmailTemplateError(EmailException):
    """Raised when an email template cannot be rendered."""
    pass