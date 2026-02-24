"""Wireless Advanced module - Aleopantest V4.0.0"""
from aleopantest.core.tool_helper import robust_import

EvilTwin = robust_import("aleopantest.modules.wireless_advanced.evil_twin", "EvilTwin")
KRACKTest = robust_import("aleopantest.modules.wireless_advanced.krack_test", "KRACKTest")
PMKIDCapture = robust_import("aleopantest.modules.wireless_advanced.pmkid_capture", "PMKIDCapture")
WPA3Audit = robust_import("aleopantest.modules.wireless_advanced.wpa3_audit", "WPA3Audit")
BluetoothScan = robust_import("aleopantest.modules.wireless_advanced.bluetooth_scan", "BluetoothScan")
BLEEnum = robust_import("aleopantest.modules.wireless_advanced.ble_enum", "BLEEnum")
ZigbeeScan = robust_import("aleopantest.modules.wireless_advanced.zigbee_scan", "ZigbeeScan")
RFIDAnalyze = robust_import("aleopantest.modules.wireless_advanced.rfid_analyze", "RFIDAnalyze")
SDRScan = robust_import("aleopantest.modules.wireless_advanced.sdr_scan", "SDRScan")
DroneDetect = robust_import("aleopantest.modules.wireless_advanced.drone_detect", "DroneDetect")
WifiDeauthDetect = robust_import("aleopantest.modules.wireless_advanced.wifi_deauth_detect", "WifiDeauthDetect")
WifiHandshake = robust_import("aleopantest.modules.wireless_advanced.wifi_handshake", "WifiHandshake")
WifiChannel = robust_import("aleopantest.modules.wireless_advanced.wifi_channel", "WifiChannel")
WifiRogueAP = robust_import("aleopantest.modules.wireless_advanced.wifi_rogue_ap", "WifiRogueAP")
NFCAnalyze = robust_import("aleopantest.modules.wireless_advanced.nfc_analyze", "NFCAnalyze")
WifiProbe = robust_import("aleopantest.modules.wireless_advanced.wifi_probe", "WifiProbe")
WifiKarma = robust_import("aleopantest.modules.wireless_advanced.wifi_karma", "WifiKarma")
WifiSignal = robust_import("aleopantest.modules.wireless_advanced.wifi_signal", "WifiSignal")
WifiWEPCrack = robust_import("aleopantest.modules.wireless_advanced.wifi_wep_crack", "WifiWEPCrack")
WifiEnterprise = robust_import("aleopantest.modules.wireless_advanced.wifi_enterprise", "WifiEnterprise")

__all__ = [
    'EvilTwin',
    'KRACKTest',
    'PMKIDCapture',
    'WPA3Audit',
    'BluetoothScan',
    'BLEEnum',
    'ZigbeeScan',
    'RFIDAnalyze',
    'SDRScan',
    'DroneDetect',
    'WifiDeauthDetect',
    'WifiHandshake',
    'WifiChannel',
    'WifiRogueAP',
    'NFCAnalyze',
    'WifiProbe',
    'WifiKarma',
    'WifiSignal',
    'WifiWEPCrack',
    'WifiEnterprise',
]
