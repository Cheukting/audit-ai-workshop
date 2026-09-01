"""Client library and CLI for the Accounts API."""

from accountsync.client import AccountsClient
from accountsync.errors import AccountsError, AuthError, ConfigError, TransientError

__version__ = "0.4.2"

__all__ = [
    "AccountsClient",
    "AccountsError",
    "AuthError",
    "ConfigError",
    "TransientError",
    "__version__",
]
