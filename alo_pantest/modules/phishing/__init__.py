"""Phishing Tools Module"""
from .web_phishing import WebPhishing
from .email_phishing import EmailPhishing
from .phishing_locator import PhishingLocator
from .phishing_impersonation import PhishingImpersonation

__all__ = [
    'WebPhishing',
    'EmailPhishing',
    'PhishingLocator',
    'PhishingImpersonation',
]
