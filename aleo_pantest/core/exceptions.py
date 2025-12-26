"""Custom exceptions for AleoPantest"""


class AleoPantestException(Exception):
    """Base exception for AleoPantest"""
    pass


class ToolException(AleoPantestException):
    """Exception for tool execution"""
    pass


class NetworkException(AleoPantestException):
    """Exception for network operations"""
    pass


class WebException(AleoPantestException):
    """Exception for web operations"""
    pass


class OsintException(AleoPantestException):
    """Exception for OSINT operations"""
    pass


class DatabaseException(AleoPantestException):
    """Exception for database operations"""
    pass


class AuthenticationException(AleoPantestException):
    """Exception for authentication"""
    pass


class ValidationException(AleoPantestException):
    """Exception for validation"""
    pass


class ConfigException(AleoPantestException):
    """Exception for configuration"""
    pass
