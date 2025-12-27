"""Custom exceptions for Aleopantest"""


class AleopantestException(Exception):
    """Base exception for Aleopantest"""
    pass


class ToolException(AleopantestException):
    """Exception for tool execution"""
    pass


class NetworkException(AleopantestException):
    """Exception for network operations"""
    pass


class WebException(AleopantestException):
    """Exception for web operations"""
    pass


class OsintException(AleopantestException):
    """Exception for OSINT operations"""
    pass


class DatabaseException(AleopantestException):
    """Exception for database operations"""
    pass


class AuthenticationException(AleopantestException):
    """Exception for authentication"""
    pass


class ValidationException(AleopantestException):
    """Exception for validation"""
    pass


class ConfigException(AleopantestException):
    """Exception for configuration"""
    pass
