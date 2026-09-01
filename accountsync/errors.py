"""Exception hierarchy for :mod:`accountsync`.

Callers that want to catch everything this package raises can catch
:class:`AccountsError`; everything else derives from it.
"""


class AccountsError(Exception):
    """Base class for every error raised by this package."""


class ConfigError(AccountsError):
    """Raised when the effective configuration is missing or unusable."""


class AuthError(AccountsError):
    """Raised when credentials are absent, rejected, or expired."""


class TransientError(AccountsError):
    """Raised by a client when a call failed but may succeed if retried."""
