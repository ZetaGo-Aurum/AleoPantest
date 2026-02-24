"""Crypto module - Aleopantest V4.0.0"""
from aleopantest.core.tool_helper import robust_import

AESAttack = robust_import("aleopantest.modules.crypto.aes_attack", "AESAttack")
RSAAttack = robust_import("aleopantest.modules.crypto.rsa_attack", "RSAAttack")
PaddingOracle = robust_import("aleopantest.modules.crypto.padding_oracle", "PaddingOracle")
TimingAttack = robust_import("aleopantest.modules.crypto.timing_attack", "TimingAttack")
CertAudit = robust_import("aleopantest.modules.crypto.cert_audit", "CertAudit")
TLSDowngrade = robust_import("aleopantest.modules.crypto.tls_downgrade", "TLSDowngrade")
SSLStripDetect = robust_import("aleopantest.modules.crypto.ssl_strip_detect", "SSLStripDetect")
PGPAudit = robust_import("aleopantest.modules.crypto.pgp_audit", "PGPAudit")
BlockchainAnalyze = robust_import("aleopantest.modules.crypto.blockchain_analyze", "BlockchainAnalyze")
RandomTest = robust_import("aleopantest.modules.crypto.random_test", "RandomTest")
KeyStrength = robust_import("aleopantest.modules.crypto.key_strength", "KeyStrength")
CipherDetect = robust_import("aleopantest.modules.crypto.cipher_detect", "CipherDetect")
CryptoAudit = robust_import("aleopantest.modules.crypto.crypto_audit", "CryptoAudit")
EntropyCheck = robust_import("aleopantest.modules.crypto.entropy_check", "EntropyCheck")
HMACTest = robust_import("aleopantest.modules.crypto.hmac_test", "HMACTest")
KeyExchange = robust_import("aleopantest.modules.crypto.key_exchange", "KeyExchange")
HashCollision = robust_import("aleopantest.modules.crypto.hash_collision", "HashCollision")
CryptoDowngrade = robust_import("aleopantest.modules.crypto.crypto_downgrade", "CryptoDowngrade")

__all__ = [
    'AESAttack',
    'RSAAttack',
    'PaddingOracle',
    'TimingAttack',
    'CertAudit',
    'TLSDowngrade',
    'SSLStripDetect',
    'PGPAudit',
    'BlockchainAnalyze',
    'RandomTest',
    'KeyStrength',
    'CipherDetect',
    'CryptoAudit',
    'EntropyCheck',
    'HMACTest',
    'KeyExchange',
    'HashCollision',
    'CryptoDowngrade',
]
