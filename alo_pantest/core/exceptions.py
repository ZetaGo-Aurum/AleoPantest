"""Custom exceptions for AloPantest"""


class AloPantestException(Exception):
    """Base exception for AloPantest"""
    pass


class ToolException(AloPantestException):
    """Exception for tool execution"""
    pass


class NetworkException(AloPantestException):
    """Exception for network operations"""
    pass


class WebException(AloPantestException):
    """Exception for web operations"""
    pass


class OsintException(AloPantestException):
    """Exception for OSINT operations"""
    pass


class DatabaseException(AloPantestException):
    """Exception for database operations"""
    pass


class AuthenticationException(AloPantestException):
    """Exception for authentication"""
    pass


class ValidationException(AloPantestException):
    """Exception for validation"""
    pass


class ConfigException(AloPantestException):
    """Exception for configuration"""
    pass
