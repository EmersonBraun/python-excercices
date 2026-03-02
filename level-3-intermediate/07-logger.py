"""
Simple Logger
==============
Difficulty: 3/5
Estimated time: 20 minutes

Problem:
--------
Build a simple logging system with:
1. Multiple log levels: DEBUG, INFO, WARNING, ERROR (each with a numeric severity).
2. Console output with colored prefixes.
3. File output that appends timestamped log entries.
4. Configurable minimum log level (messages below it are ignored).
5. Log formatting with timestamp, level, and message.

Concepts practiced:
- File I/O (append mode)
- Enumerations or constants
- Datetime formatting
- String formatting
- Class design

Expected output (example):
--------------------------
# [2024-01-15 10:30:00] [DEBUG]   Application started
# [2024-01-15 10:30:00] [INFO]    User logged in: alice
# [2024-01-15 10:30:00] [WARNING] Disk usage at 85%
# [2024-01-15 10:30:00] [ERROR]   Connection to database failed
#
# --- Setting level to WARNING ---
# [2024-01-15 10:30:00] [WARNING] Memory usage high
# [2024-01-15 10:30:00] [ERROR]   Out of memory
# (DEBUG and INFO messages are suppressed)
"""

import os
from datetime import datetime


class LogLevel:
    """Log level constants with numeric severity."""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3

    _names = {0: "DEBUG", 1: "INFO", 2: "WARNING", 3: "ERROR"}
    _colors = {
        0: "\033[36m",    # Cyan
        1: "\033[32m",    # Green
        2: "\033[33m",    # Yellow
        3: "\033[31m",    # Red
    }
    RESET = "\033[0m"

    @classmethod
    def name(cls, level):
        """Return the string name for a numeric level."""
        return cls._names.get(level, "UNKNOWN")

    @classmethod
    def color(cls, level):
        """Return the ANSI color code for a level."""
        return cls._colors.get(level, "")


class Logger:
    """A simple logger with console and file output."""

    def __init__(self, name, level=LogLevel.DEBUG, log_file=None):
        """
        Initialize the logger.

        Parameters:
            name (str): Logger name (shown in output).
            level (int): Minimum log level to output.
            log_file (str, optional): Path to a log file for persistent output.
        """
        self.name = name
        self.level = level
        self.log_file = log_file
        self._entries = []

    def set_level(self, level):
        """
        Set the minimum log level.

        Parameters:
            level (int): New minimum level.
        """
        self.level = level
        level_name = LogLevel.name(level)
        print(f"\n--- Logger '{self.name}' level set to {level_name} ---\n")

    def _format_message(self, level, message):
        """Create a formatted log string (without color)."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        level_name = LogLevel.name(level)
        return f"[{timestamp}] [{level_name:8s}] {message}"

    def _log(self, level, message):
        """
        Internal log method. Outputs to console and optionally to file.

        Parameters:
            level (int): Severity level.
            message (str): Log message.
        """
        if level < self.level:
            return

        formatted = self._format_message(level, message)
        self._entries.append(formatted)

        # Console output with color
        color = LogLevel.color(level)
        reset = LogLevel.RESET
        print(f"{color}{formatted}{reset}")

        # File output (no color codes)
        if self.log_file:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(formatted + "\n")

    def debug(self, message):
        """Log a DEBUG message."""
        self._log(LogLevel.DEBUG, message)

    def info(self, message):
        """Log an INFO message."""
        self._log(LogLevel.INFO, message)

    def warning(self, message):
        """Log a WARNING message."""
        self._log(LogLevel.WARNING, message)

    def error(self, message):
        """Log an ERROR message."""
        self._log(LogLevel.ERROR, message)

    def get_entries(self, level=None):
        """
        Get stored log entries, optionally filtered by minimum level.

        Parameters:
            level (int, optional): Minimum level to return.

        Returns:
            list[str]: Log entries.
        """
        if level is None:
            return list(self._entries)

        level_name = LogLevel.name(level)
        return [e for e in self._entries if f"[{level_name}" in e]

    def clear(self):
        """Clear stored entries and the log file."""
        self._entries.clear()
        if self.log_file and os.path.exists(self.log_file):
            os.remove(self.log_file)


if __name__ == "__main__":
    log_file = "demo_app.log"

    print("--- Logger Demo ---\n")

    # Create logger with file output
    logger = Logger("MyApp", level=LogLevel.DEBUG, log_file=log_file)

    # Log at all levels
    logger.debug("Application started")
    logger.info("User logged in: alice")
    logger.warning("Disk usage at 85%")
    logger.error("Connection to database failed")

    # Change level to WARNING
    logger.set_level(LogLevel.WARNING)

    logger.debug("This DEBUG message will be suppressed")
    logger.info("This INFO message will be suppressed")
    logger.warning("Memory usage high")
    logger.error("Out of memory")

    # Show stored entries
    print("\n--- All Stored Entries ---")
    for entry in logger.get_entries():
        print(f"  {entry}")

    print(f"\n--- Total entries: {len(logger.get_entries())} ---")

    # Show file contents
    if os.path.exists(log_file):
        print(f"\n--- Contents of {log_file} ---")
        with open(log_file, "r", encoding="utf-8") as f:
            print(f.read())

    # Cleanup
    logger.clear()
    print(f"Cleaned up {log_file}.")
