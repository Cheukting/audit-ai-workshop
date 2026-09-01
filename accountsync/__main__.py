"""Allow ``python -m accountsync``."""

from accountsync.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
