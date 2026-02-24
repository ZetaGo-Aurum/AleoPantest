"""Social Engineering tools module initialization"""
from aleopantest.core.tool_helper import robust_import

UsernameGen = robust_import("aleopantest.modules.social.username_gen", "UsernameGen")
PayloadDelivery = robust_import("aleopantest.modules.social.payload_delivery", "PayloadDelivery")

PhishTemplate = robust_import("aleopantest.modules.social.phish_template", "PhishTemplate")
VishingSim = robust_import("aleopantest.modules.social.vishing_sim", "VishingSim")
SmishingSim = robust_import("aleopantest.modules.social.smishing_sim", "SmishingSim")
PretextingGen = robust_import("aleopantest.modules.social.pretexting_gen", "PretextingGen")
CloneSite = robust_import("aleopantest.modules.social.clone_site", "CloneSite")
CredentialHarvest = robust_import("aleopantest.modules.social.credential_harvest", "CredentialHarvest")
USBDropSim = robust_import("aleopantest.modules.social.usb_drop_sim", "USBDropSim")
WateringHole = robust_import("aleopantest.modules.social.watering_hole", "WateringHole")
SpearPhish = robust_import("aleopantest.modules.social.spear_phish", "SpearPhish")
DeepfakeDetect = robust_import("aleopantest.modules.social.deepfake_detect", "DeepfakeDetect")
SocialProfile = robust_import("aleopantest.modules.social.social_profile", "SocialProfile")
PhishDetect = robust_import("aleopantest.modules.social.phish_detect", "PhishDetect")
AwarenessTest = robust_import("aleopantest.modules.social.awareness_test", "AwarenessTest")
QRPhish = robust_import("aleopantest.modules.social.qr_phish", "QRPhish")
CallbackPhish = robust_import("aleopantest.modules.social.callback_phish", "CallbackPhish")

__all__ = ['UsernameGen', 'PayloadDelivery'
    'PhishTemplate',
    'VishingSim',
    'SmishingSim',
    'PretextingGen',
    'CloneSite',
    'CredentialHarvest',
    'USBDropSim',
    'WateringHole',
    'SpearPhish',
    'DeepfakeDetect',
    'SocialProfile',
    'PhishDetect',
    'AwarenessTest',
    'QRPhish',
    'CallbackPhish',
]
