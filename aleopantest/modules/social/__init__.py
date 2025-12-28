"""Social Engineering tools module initialization"""
from aleopantest.core.tool_helper import robust_import

UsernameGen = robust_import("aleopantest.modules.social.username_gen", "UsernameGen")
PayloadDelivery = robust_import("aleopantest.modules.social.payload_delivery", "PayloadDelivery")

__all__ = ['UsernameGen', 'PayloadDelivery']
