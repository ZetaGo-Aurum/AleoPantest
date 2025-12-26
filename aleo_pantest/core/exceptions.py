"""Custom exceptions for Aleocrophic"""


class AleocrophicException(Exception):
    """Base exception for Aleocrophic"""
    pass


class ToolException(AleocrophicException):
    """Exception for tool execution"""
    pass


class NetworkException(AleocrophicException):
    """Exception for network operations"""
    pass


class WebException(AleocrophicException):
    """Exception for web operations"""
    pass


class OsintException(AleocrophicException):
    """Exception for OSINT operations"""
    pass


class DatabaseException(AleocrophicException):
    """Exception for database operations"""
    pass


class AuthenticationException(AleocrophicException):
    """Exception for authentication"""
    pass


class ValidationException(AleocrophicException):
    """Exception for validation"""
    pass


class ConfigException(AleocrophicException):
    """Exception for configuration"""
    pass
