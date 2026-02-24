"""Main CLI Application untuk Aleopantest V4.0.0 - by Aleocrophic"""
import sys
import os
from pathlib import Path

try:
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich import print as rprint
except ImportError:
    print("ERROR: Missing dependencies. Run: pip install click rich")
    sys.exit(1)

from aleopantest.core.logger import logger
from aleopantest.core.platform_detector import PlatformDetector

# --- Existing V3 imports (preserved) ---
from aleopantest.modules.network import (
    PortScanner, PacketSniffer, PingTool, DNSLookup, TraceRoute,
    WhoisLookup, SSLChecker, IPScanner, DDoSSimulator, MACLookup,
    NetSpeed, SubnetCalc, ArpScanner, VLANScanner, SNMPWalker
)
from aleopantest.modules.web import (
    SQLInjector, XSSDetector, CSRFDetector, WebCrawler,
    VulnerabilityScanner, SubdomainFinder, TechStack,
    DirBrute, LinkExtractor, AdminFinder, HeadersAnalyzer, ProxyFinder,
    APIAnalyzer
)
from aleopantest.modules.osint import (
    EmailFinder, DomainInfo, IPGeolocation,
    MetadataExtractor, SearchEngineDorking, UserSearch,
    GitRecon, WhoisHistory, ShodanSearch, PhoneLookup,
    MetadataExif, SocialAnalyzer, BreachChecker, DarkWebSearch
)
from aleopantest.modules.web import AdvancedDorking
from aleopantest.modules.utilities import (
    PasswordGenerator, HashTools, Base64Tool, URLEncoder, URLMasker,
    URLShortener, HTMLTool, JSONFormatter, JWTDecoder, TextObfuscator,
    IPConverter, TimestampConvert, ColorConverter, UnitConverter
)
from aleopantest.modules.phishing import (
    PhishingLocator, WebPhishing, EmailPhishing, URLMaskingTool, PhishingFramework
)
from aleopantest.modules.security import (
    AntiDDoS, WAFDetector, VulnDB, FirewallBypass, IDSEvasionHelper
)
from aleopantest.modules.clickjacking import (
    ClickjackingChecker, ClickjackingMaker, AntiClickjackingGenerator
)
from aleopantest.modules.crypto import (
    HashCracker, HashGenerator, VigenereCipher, XORCipher,
    RSAGenerator, Steganography, FileEncryptor
)
from aleopantest.modules.reporting import (
    PDFReportGenerator, HTMLReportGenerator
)
from aleopantest.modules.exploit import (
    SearchSploitWrapper, MetasploitHelper
)
from aleopantest.modules.forensics import (
    FileCarver, MemoryAnalyzer, LogForensics
)
from aleopantest.modules.malware import (
    MalwareSandbox, PEAnalyzer, StringExtractor
)
from aleopantest.modules.mobile import (
    APKAnalyzer, IOSAppAnalyzer
)
from aleopantest.modules.cloud import (
    AWSEnum, AzureAudit
)
from aleopantest.modules.iot import (
    MQTTExplorer, FirmwareScanner
)
from aleopantest.modules.post_exploit import (
    SystemEnum, PrivEscCheck
)
from aleopantest.modules.social import (
    UsernameGen, PayloadDelivery
)
from aleopantest.modules.wireless import (
    BeaconFlood, DeauthTool, WifiScanner, WPSChecker
)
from aleopantest.modules.database import (
    SQLBruteForcer, MongoDBAuditor
)

# --- V4.0 New Tool Imports ---
from aleopantest.modules.active_directory import (ADEnum, Kerberoast, ASREPRoast, DCSyncDetect, BloodhoundIngest, GPPDecrypt)
from aleopantest.modules.active_directory import (ADACLAudit, LDAPSearch, NTLMRelayDetect, ADTrustAudit, ADPasswordAudit, ADDelegation)
from aleopantest.modules.active_directory import (SPNScan, ADCertAudit, ADDNSEnum, ADGPOAudit, ADReplication, ADSIDHistory)
from aleopantest.modules.active_directory import (ADForestAudit, ADPrivUsers, ADLockout, ADStaleObjects, ADSchemaAudit, ADBackupCheck)
from aleopantest.modules.active_directory import (LAPSAudit, ADServiceAccounts, ADGroupNesting, ADRecycleBin, ADAdminCount, ADFunctionalLevel)
from aleopantest.modules.api_security import (GraphQLIntrospect, RESTFuzzer, APIKeyLeak, SwaggerScan, OAuthTest, JWTAttack)
from aleopantest.modules.api_security import (CORSTest, SOAPAudit, GRPCTest, RateLimitTest, APIAuthBypass, APIEnum)
from aleopantest.modules.api_security import (APIVersionCheck, APIParamTamper, APISchemaValidate, WebhookTest, APIDOSTest, APIInjection)
from aleopantest.modules.api_security import (APIMassAssign, APIBrokenAuth, APIExcessiveData, APIBOLA, APISSRF, APIGraphQLDoS)
from aleopantest.modules.api_security import (APIResponseHeader, APIErrorDisclosure, APIMethodTest, APIContentType, APIPagination, APIBatchTest)
from aleopantest.modules.api_security import (APICachePoison, APIRaceCondition, APIIdempotency, APIFileUpload, APIRedirect)
from aleopantest.modules.automation_pipeline import (AutoRecon, AutoVuln, PipelineBuilder, Scheduler, ParallelScan, ResultAggregator)
from aleopantest.modules.automation_pipeline import (NotificationSend, WebhookTrigger, CICDScan, ContinuousMonitor, ScanProfile, ToolChain)
from aleopantest.modules.automation_pipeline import (BatchScan, ScanResume, ReportAuto, TargetImport, AssetDiscover, ChangeDetect)
from aleopantest.modules.automation_pipeline import (WorkflowTemplate, ScanQueue)
from aleopantest.modules.binary_analysis import (ELFAnalyzer, DLLInjectDetect, ROPGadget, FormatString, HeapAnalyzer, FuzzerGen)
from aleopantest.modules.binary_analysis import (ShellcodeGen, PackerDetect, AntiDebugDetect, BinaryDiff, SymbolExtract, CallGraph)
from aleopantest.modules.binary_analysis import (ControlFlow, BinaryPatch, ObfuscationDetect, ImportAnalyzer, EntropyAnalyzer, BinaryStrings)
from aleopantest.modules.binary_analysis import (CodeCave, VTableAnalyzer, BinarySign, Disassembler, Decompiler, BinaryVuln)
from aleopantest.modules.binary_analysis import (FirmwareExtract)
from aleopantest.modules.cloud import (GCPEnum, S3BucketScan, AzureADEnum, K8sClusterAudit, DockerEscapeCheck, LambdaAudit)
from aleopantest.modules.cloud import (IAMPrivesc, CloudTrailAudit, ECRScan, TerraformScan, CloudStorageEnum, GCPIAMAudit)
from aleopantest.modules.cloud import (AzureBlobScan, CloudFirewall, ServerlessAudit, CloudKeyAudit, CloudNetworkAudit, CloudLogging)
from aleopantest.modules.cloud import (CloudCompliance, CloudCostAudit, EKSAudit, AKSAudit, GKEAudit, CloudDBAudit)
from aleopantest.modules.cloud import (CloudSecretScan, CloudSnapshot, MultiCloudAudit, CloudDNSAudit, CloudWAFAudit, CloudCDNAudit)
from aleopantest.modules.cloud import (CloudIdentity, CloudEndpoint, CloudEncryption, CloudContainerReg, CloudAPIGateway, CloudLBAudit)
from aleopantest.modules.cloud import (CloudVPNAudit, CloudIAMRoles)
from aleopantest.modules.compliance_audit import (PCIDSS, HIPAAAudit, GDPRScan, ISO27001, NISTAssess, SOXAudit)
from aleopantest.modules.compliance_audit import (CISBenchmark, STIGCheck, VulnPrioritize, RiskScore, PolicyCheck, BaselineAudit)
from aleopantest.modules.compliance_audit import (AccessReview, DataClass, RetentionCheck, VendorRisk, IncidentReport, ControlMatrix)
from aleopantest.modules.compliance_audit import (GapAnalysis, MaturityAssess, AuditEvidence, PrivacyImpact, ThreatModel, SecurityRoadmap)
from aleopantest.modules.compliance_audit import (ComplianceReport)
from aleopantest.modules.container_security import (DockerAudit, K8sPodScan, ContainerEscapeDetect, ImageScan, RegistryEnum, ComposeAudit)
from aleopantest.modules.container_security import (HelmAudit, IstioCheck, RuntimeScan, CgroupEscape, K8sRBAC, K8sNetworkPolicy)
from aleopantest.modules.container_security import (K8sSecrets, DockerSocket, K8sAdmission, ContainerCaps, K8sEtcd, DockerfileLint)
from aleopantest.modules.container_security import (K8sAPIAudit, ContainerForensics, K8sPSP, ContainerNetwork, K8sIngress, ContainerVolume)
from aleopantest.modules.container_security import (K8sServiceMesh)
from aleopantest.modules.crypto import (AESAttack, RSAAttack, PaddingOracle, TimingAttack, CertAudit, TLSDowngrade)
from aleopantest.modules.crypto import (SSLStripDetect, PGPAudit, BlockchainAnalyze, RandomTest, KeyStrength, CipherDetect)
from aleopantest.modules.crypto import (CryptoAudit, EntropyCheck, HMACTest, KeyExchange, HashCollision, CryptoDowngrade)
from aleopantest.modules.forensics import (DiskForensics, RegistryForensics, BrowserForensics, EmailForensics, TimelineGen, ArtifactCollect)
from aleopantest.modules.forensics import (VolatilityWrap, YaraScan, PCAPAnalyzer, USBForensics, EventLog, PrefetchAnalyzer)
from aleopantest.modules.forensics import (ShadowCopy, DeletedRecovery, SwapAnalyzer, HashVerify, MalwareTriage, SteganographyDetect)
from aleopantest.modules.forensics import (EncryptionDetect, ChainCustody)
from aleopantest.modules.misc_utility import (PayloadEncode, C2Detect, HoneypotDetect, SandboxDetect, ProxyChain, TorCheck)
from aleopantest.modules.misc_utility import (VPNLeakTest, DNSLeakTest, IPRotate, UserAgentGen, ReverseShell, BindShell)
from aleopantest.modules.misc_utility import (FileServer, PortForward, NetworkPivot, DataExfilDetect, LogCleanerDetect, RootkitDetect)
from aleopantest.modules.misc_utility import (BackdoorDetect, WebshellDetect, ConfigAudit, ServiceEnum, CronAudit, SUIDCheck)
from aleopantest.modules.misc_utility import (KernelExploit)
from aleopantest.modules.mobile import (AndroidDebug, IOSJailbreak, MobileSSLPin, AppPermission, SmaliDecompile, FridaScripts)
from aleopantest.modules.mobile import (ObjectionWrap, MobileAPITest, CertPinBypass, IntentFuzz, MobileStorage, MobileCrypto)
from aleopantest.modules.mobile import (MobileNetwork, MobileAuth, AppCloneDetect, MobileMalware, MobilePrivacy, MobileConfig)
from aleopantest.modules.network_advanced import (BGPHijack, DNSTunnel, ICMPTunnel, TCPHijack, MITMDetect, RogueDHCP)
from aleopantest.modules.network_advanced import (IPv6Recon, NetBIOSEnum, SMBEnum, RPCEnum, NTPAmp, SSDPScan)
from aleopantest.modules.network_advanced import (LDAPEnum, FTPAudit, SMTPEnum, POP3Audit, IMAPAudit, RedisAudit)
from aleopantest.modules.network_advanced import (MemcacheAudit, ElasticAudit, KafkaAudit, RabbitAudit, VNCAudit, RDPAudit)
from aleopantest.modules.network_advanced import (TelnetAudit)
from aleopantest.modules.osint import (TelegramOSINT, DiscordRecon, LinkedInEnum, PastebinMonitor, WaybackRecon, CertSearch)
from aleopantest.modules.osint import (DNSHistory, FaviconHash, S3Finder, GoogleDorkingAdv, GitHubRecon, TwitterOSINT)
from aleopantest.modules.osint import (InstagramOSINT, FaceSearch, EmailOSINT, CompanyRecon, GeoOSINT, VehicleOSINT)
from aleopantest.modules.osint import (CryptoTrace, DomainMonitor, LeakSearch, WebArchive, ImageForensics, SocialMediaMap)
from aleopantest.modules.osint import (WebsiteMonitor, TechProfiler, NetworkOSINT, DocumentOSINT, PhoneOSINT, UsernameSearch)
from aleopantest.modules.osint import (IPReputation, ThreatIntel, MalwareHash, SubdomainEnum, ASNLookup)
from aleopantest.modules.password_auth import (SprayAttack, CredentialTest, PassPolicyAudit, MFABypassCheck, SessionHijackDetect, CookieAnalyzer)
from aleopantest.modules.password_auth import (OAuthAbuse, SAMLAttack, TicketForge, RainbowGen, WordlistGen, HashIdentify)
from aleopantest.modules.password_auth import (PassStrength, BruteHTTP, BruteSSH, BruteFTP, BruteRDP, BruteMySQL)
from aleopantest.modules.password_auth import (BruteSMTP, BruteLDAP, BruteCustom, DefaultCreds, PassReuse, AuthTokenTest)
from aleopantest.modules.password_auth import (SSOAudit, TOTPTest, APIKeyTest, CertAuthTest, BiometricBypass, CaptchaTest)
from aleopantest.modules.reporting import (ExecutiveReport, ComplianceRep, RiskMatrix, VulnTimeline, DiffReport, CSVExport)
from aleopantest.modules.reporting import (XMLExport, SARIFExport, MarkdownReport, ChartGen, DashboardGen, ScanCompare)
from aleopantest.modules.reporting import (EvidencePack)
from aleopantest.modules.social import (PhishTemplate, VishingSim, SmishingSim, PretextingGen, CloneSite, CredentialHarvest)
from aleopantest.modules.social import (USBDropSim, WateringHole, SpearPhish, DeepfakeDetect, SocialProfile, PhishDetect)
from aleopantest.modules.social import (AwarenessTest, QRPhish, CallbackPhish)
from aleopantest.modules.web_advanced import (XXEDetect, SSRFDetect, SSTIDetect, PrototypePollute, DeserializeCheck, HTTPSmuggle)
from aleopantest.modules.web_advanced import (CachePoison, CORSMiscfg, OpenRedirect, HostHeaderInject, CRLFInject, LFIDetect)
from aleopantest.modules.web_advanced import (RFIDetect, CommandInject, IDORDetect, PathTraversal, UploadVuln, SessionFixation)
from aleopantest.modules.web_advanced import (BusinessLogic, RaceCondition, SubdomainTakeover, WebSocketTest, CSRFAdvanced, ContentSecurity)
from aleopantest.modules.web_advanced import (CookieSecurity, JSAnalyzer, WAFBypass, WebFingerprint, BrokenAccess, SecurityHeaders)
from aleopantest.modules.web_advanced import (HTMLInject, WebParamMine, HTTP2Test, GraphQLVuln, WebSocketHijack, DOMXSS)
from aleopantest.modules.web_advanced import (WebCacheDeception, ClickHijack, JWTVuln)
from aleopantest.modules.wireless_advanced import (EvilTwin, KRACKTest, PMKIDCapture, WPA3Audit, BluetoothScan, BLEEnum)
from aleopantest.modules.wireless_advanced import (ZigbeeScan, RFIDAnalyze, SDRScan, DroneDetect, WifiDeauthDetect, WifiHandshake)
from aleopantest.modules.wireless_advanced import (WifiChannel, WifiRogueAP, NFCAnalyze, WifiProbe, WifiKarma, WifiSignal)
from aleopantest.modules.wireless_advanced import (WifiWEPCrack, WifiEnterprise)

import json
import requests
from datetime import datetime

console = Console()


def send_to_web_dashboard(tool_id, result):
    """Send tool execution results to the web dashboard if available"""
    try:
        requests.post("http://127.0.0.1:8002/api/report",
            json={"tool_id": tool_id, "result": result, "timestamp": datetime.now().isoformat()},
            timeout=2)
    except Exception:
        pass


# === TOOLS REGISTRY (V3 + V4 Combined) ===
TOOLS_REGISTRY = {
    # --- V3 Existing Tools ---
    'port-scan': PortScanner,
    'ping': PingTool,
    'dns': DNSLookup,
    'traceroute': TraceRoute,
    'whois': WhoisLookup,
    'ssl-check': SSLChecker,
    'ip-scan': IPScanner,
    'sniffer': PacketSniffer,
    'ddos-sim': DDoSSimulator,
    'mac-lookup': MACLookup,
    'net-speed': NetSpeed,
    'subnet-calc': SubnetCalc,
    'arp-scan': ArpScanner,
    'vlan-scan': VLANScanner,
    'snmp-walker': SNMPWalker,
    'sql-inject': SQLInjector,
    'xss-detect': XSSDetector,
    'csrf-detect': CSRFDetector,
    'crawler': WebCrawler,
    'vuln-scan': VulnerabilityScanner,
    'subdomain': SubdomainFinder,
    'dorking': AdvancedDorking,
    'tech-stack': TechStack,
    'dir-brute': DirBrute,
    'link-extract': LinkExtractor,
    'admin-finder': AdminFinder,
    'headers-analyzer': HeadersAnalyzer,
    'proxy-finder': ProxyFinder,
    'api-analyzer': APIAnalyzer,
    'email-find': EmailFinder,
    'domain-info': DomainInfo,
    'ip-geo': IPGeolocation,
    'metadata': MetadataExtractor,
    'dorking-search': SearchEngineDorking,
    'user-search': UserSearch,
    'git-recon': GitRecon,
    'whois-history': WhoisHistory,
    'shodan-search': ShodanSearch,
    'phone-lookup': PhoneLookup,
    'metadata-exif': MetadataExif,
    'social-analyzer': SocialAnalyzer,
    'breach-check': BreachChecker,
    'dark-web-search': DarkWebSearch,
    'password-gen': PasswordGenerator,
    'hash-tools': HashTools,
    'base64': Base64Tool,
    'url-encode': URLEncoder,
    'url-mask': URLMasker,
    'url-shorten': URLShortener,
    'html-tool': HTMLTool,
    'json-format': JSONFormatter,
    'jwt-decoder': JWTDecoder,
    'text-obfuscate': TextObfuscator,
    'ip-convert': IPConverter,
    'timestamp-convert': TimestampConvert,
    'color-convert': ColorConverter,
    'unit-convert': UnitConverter,
    'phishing-locator': PhishingLocator,
    'web-phishing': WebPhishing,
    'email-phishing': EmailPhishing,
    'url-masking': URLMaskingTool,
    'phishing-framework': PhishingFramework,
    'anti-ddos': AntiDDoS,
    'waf-detect': WAFDetector,
    'vuln-db': VulnDB,
    'firewall-bypass': FirewallBypass,
    'ids-evasion': IDSEvasionHelper,
    'clickjacking-check': ClickjackingChecker,
    'clickjacking-make': ClickjackingMaker,
    'anti-clickjacking': AntiClickjackingGenerator,
    'hash-cracker': HashCracker,
    'hash-gen': HashGenerator,
    'vigenere': VigenereCipher,
    'xor-cipher': XORCipher,
    'rsa-gen': RSAGenerator,
    'stegano': Steganography,
    'file-encrypt': FileEncryptor,
    'beacon-flood': BeaconFlood,
    'deauth': DeauthTool,
    'wifi-scan': WifiScanner,
    'wps-check': WPSChecker,
    'sql-brute': SQLBruteForcer,
    'mongodb-audit': MongoDBAuditor,
    'pdf-report': PDFReportGenerator,
    'html-report': HTMLReportGenerator,
    'searchsploit': SearchSploitWrapper,
    'msf-helper': MetasploitHelper,
    'file-carver': FileCarver,
    'memory-analyzer': MemoryAnalyzer,
    'log-forensics': LogForensics,
    'malware-sandbox': MalwareSandbox,
    'pe-analyzer': PEAnalyzer,
    'string-extractor': StringExtractor,
    'apk-analyzer': APKAnalyzer,
    'ios-analyzer': IOSAppAnalyzer,
    'aws-enum': AWSEnum,
    'azure-audit': AzureAudit,
    'mqtt-explorer': MQTTExplorer,
    'firmware-scan': FirmwareScanner,
    'system-enum': SystemEnum,
    'priv-esc-check': PrivEscCheck,
    'username-gen': UsernameGen,
    'payload-delivery': PayloadDelivery,

    # --- V4.0 New Tools ---
    'ad-enum': ADEnum,
    'kerberoast': Kerberoast,
    'asrep-roast': ASREPRoast,
    'dcsync-detect': DCSyncDetect,
    'bloodhound-ingest': BloodhoundIngest,
    'gpp-decrypt': GPPDecrypt,
    'ad-acl-audit': ADACLAudit,
    'ldap-search': LDAPSearch,
    'ntlm-relay-detect': NTLMRelayDetect,
    'ad-trust-audit': ADTrustAudit,
    'ad-pass-audit': ADPasswordAudit,
    'ad-delegation': ADDelegation,
    'spn-scan': SPNScan,
    'ad-cert-audit': ADCertAudit,
    'ad-dns-enum': ADDNSEnum,
    'ad-gpo-audit': ADGPOAudit,
    'ad-replication': ADReplication,
    'ad-sid-history': ADSIDHistory,
    'ad-forest-audit': ADForestAudit,
    'ad-priv-users': ADPrivUsers,
    'ad-lockout': ADLockout,
    'ad-stale-objects': ADStaleObjects,
    'ad-schema-audit': ADSchemaAudit,
    'ad-backup-check': ADBackupCheck,
    'laps-audit': LAPSAudit,
    'ad-svc-audit': ADServiceAccounts,
    'ad-group-nesting': ADGroupNesting,
    'ad-recycle-bin': ADRecycleBin,
    'ad-admin-count': ADAdminCount,
    'ad-func-level': ADFunctionalLevel,
    'graphql-introspect': GraphQLIntrospect,
    'rest-fuzz': RESTFuzzer,
    'api-key-leak': APIKeyLeak,
    'swagger-scan': SwaggerScan,
    'oauth-test': OAuthTest,
    'jwt-attack': JWTAttack,
    'cors-test': CORSTest,
    'soap-audit': SOAPAudit,
    'grpc-test': GRPCTest,
    'rate-limit-test': RateLimitTest,
    'api-auth-bypass': APIAuthBypass,
    'api-enum': APIEnum,
    'api-version-check': APIVersionCheck,
    'api-param-tamper': APIParamTamper,
    'api-schema-validate': APISchemaValidate,
    'webhook-test': WebhookTest,
    'api-dos-test': APIDOSTest,
    'api-injection': APIInjection,
    'api-mass-assign': APIMassAssign,
    'api-broken-auth': APIBrokenAuth,
    'api-excessive-data': APIExcessiveData,
    'api-bola': APIBOLA,
    'api-ssrf': APISSRF,
    'graphql-dos': APIGraphQLDoS,
    'api-response-header': APIResponseHeader,
    'api-error-disclosure': APIErrorDisclosure,
    'api-method-test': APIMethodTest,
    'api-content-type': APIContentType,
    'api-pagination': APIPagination,
    'api-batch-test': APIBatchTest,
    'api-cache-poison': APICachePoison,
    'api-race-condition': APIRaceCondition,
    'api-idempotency': APIIdempotency,
    'api-file-upload': APIFileUpload,
    'api-redirect': APIRedirect,
    'docker-audit': DockerAudit,
    'k8s-pod-scan': K8sPodScan,
    'container-escape-detect': ContainerEscapeDetect,
    'image-scan': ImageScan,
    'registry-enum': RegistryEnum,
    'compose-audit': ComposeAudit,
    'helm-audit': HelmAudit,
    'istio-check': IstioCheck,
    'runtime-scan': RuntimeScan,
    'cgroup-escape': CgroupEscape,
    'k8s-rbac': K8sRBAC,
    'k8s-net-policy': K8sNetworkPolicy,
    'k8s-secrets': K8sSecrets,
    'docker-socket': DockerSocket,
    'k8s-admission': K8sAdmission,
    'container-caps': ContainerCaps,
    'k8s-etcd': K8sEtcd,
    'dockerfile-lint': DockerfileLint,
    'k8s-api-audit': K8sAPIAudit,
    'container-forensics': ContainerForensics,
    'k8s-psp': K8sPSP,
    'container-network': ContainerNetwork,
    'k8s-ingress': K8sIngress,
    'container-volume': ContainerVolume,
    'k8s-service-mesh': K8sServiceMesh,
    'gcp-enum': GCPEnum,
    's3-bucket-scan': S3BucketScan,
    'azure-ad-enum': AzureADEnum,
    'k8s-cluster-audit': K8sClusterAudit,
    'docker-escape-check': DockerEscapeCheck,
    'lambda-audit': LambdaAudit,
    'iam-privesc': IAMPrivesc,
    'cloudtrail-audit': CloudTrailAudit,
    'ecr-scan': ECRScan,
    'terraform-scan': TerraformScan,
    'cloud-storage-enum': CloudStorageEnum,
    'gcp-iam-audit': GCPIAMAudit,
    'azure-blob-scan': AzureBlobScan,
    'cloud-firewall': CloudFirewall,
    'serverless-audit': ServerlessAudit,
    'cloud-key-audit': CloudKeyAudit,
    'cloud-network-audit': CloudNetworkAudit,
    'cloud-logging': CloudLogging,
    'cloud-compliance': CloudCompliance,
    'cloud-cost-audit': CloudCostAudit,
    'eks-audit': EKSAudit,
    'aks-audit': AKSAudit,
    'gke-audit': GKEAudit,
    'cloud-db-audit': CloudDBAudit,
    'cloud-secret-scan': CloudSecretScan,
    'cloud-snapshot': CloudSnapshot,
    'multi-cloud-audit': MultiCloudAudit,
    'cloud-dns-audit': CloudDNSAudit,
    'cloud-waf-audit': CloudWAFAudit,
    'cloud-cdn-audit': CloudCDNAudit,
    'cloud-identity': CloudIdentity,
    'cloud-endpoint': CloudEndpoint,
    'cloud-encryption': CloudEncryption,
    'cloud-container-reg': CloudContainerReg,
    'cloud-api-gateway': CloudAPIGateway,
    'cloud-lb-audit': CloudLBAudit,
    'cloud-vpn-audit': CloudVPNAudit,
    'cloud-iam-roles': CloudIAMRoles,
    'xxe-detect': XXEDetect,
    'ssrf-detect': SSRFDetect,
    'ssti-detect': SSTIDetect,
    'prototype-pollute': PrototypePollute,
    'deserialize-check': DeserializeCheck,
    'http-smuggle': HTTPSmuggle,
    'cache-poison': CachePoison,
    'cors-miscfg': CORSMiscfg,
    'open-redirect': OpenRedirect,
    'host-header-inject': HostHeaderInject,
    'crlf-inject': CRLFInject,
    'lfi-detect': LFIDetect,
    'rfi-detect': RFIDetect,
    'command-inject': CommandInject,
    'idor-detect': IDORDetect,
    'path-traversal': PathTraversal,
    'upload-vuln': UploadVuln,
    'session-fixation': SessionFixation,
    'business-logic': BusinessLogic,
    'race-condition': RaceCondition,
    'subdomain-takeover': SubdomainTakeover,
    'websocket-test': WebSocketTest,
    'csrf-advanced': CSRFAdvanced,
    'content-security': ContentSecurity,
    'cookie-security': CookieSecurity,
    'js-analyzer': JSAnalyzer,
    'waf-bypass': WAFBypass,
    'web-fingerprint': WebFingerprint,
    'broken-access': BrokenAccess,
    'security-headers': SecurityHeaders,
    'html-inject': HTMLInject,
    'web-param-mine': WebParamMine,
    'http2-test': HTTP2Test,
    'graphql-vuln': GraphQLVuln,
    'ws-hijack': WebSocketHijack,
    'dom-xss': DOMXSS,
    'web-cache-deception': WebCacheDeception,
    'click-hijack': ClickHijack,
    'jwt-vuln': JWTVuln,
    'bgp-hijack': BGPHijack,
    'dns-tunnel': DNSTunnel,
    'icmp-tunnel': ICMPTunnel,
    'tcp-hijack': TCPHijack,
    'mitm-detect': MITMDetect,
    'rogue-dhcp': RogueDHCP,
    'ipv6-recon': IPv6Recon,
    'netbios-enum': NetBIOSEnum,
    'smb-enum': SMBEnum,
    'rpc-enum': RPCEnum,
    'ntp-amp': NTPAmp,
    'ssdp-scan': SSDPScan,
    'ldap-enum': LDAPEnum,
    'ftp-audit': FTPAudit,
    'smtp-enum': SMTPEnum,
    'pop3-audit': POP3Audit,
    'imap-audit': IMAPAudit,
    'redis-audit': RedisAudit,
    'memcache-audit': MemcacheAudit,
    'elastic-audit': ElasticAudit,
    'kafka-audit': KafkaAudit,
    'rabbit-audit': RabbitAudit,
    'vnc-audit': VNCAudit,
    'rdp-audit': RDPAudit,
    'telnet-audit': TelnetAudit,
    'evil-twin': EvilTwin,
    'krack-test': KRACKTest,
    'pmkid-capture': PMKIDCapture,
    'wpa3-audit': WPA3Audit,
    'bluetooth-scan': BluetoothScan,
    'ble-enum': BLEEnum,
    'zigbee-scan': ZigbeeScan,
    'rfid-analyze': RFIDAnalyze,
    'sdr-scan': SDRScan,
    'drone-detect': DroneDetect,
    'wifi-deauth-detect': WifiDeauthDetect,
    'wifi-handshake': WifiHandshake,
    'wifi-channel': WifiChannel,
    'wifi-rogue-ap': WifiRogueAP,
    'nfc-analyze': NFCAnalyze,
    'wifi-probe': WifiProbe,
    'wifi-karma': WifiKarma,
    'wifi-signal': WifiSignal,
    'wifi-wep-crack': WifiWEPCrack,
    'wifi-enterprise': WifiEnterprise,
    'elf-analyzer': ELFAnalyzer,
    'dll-inject-detect': DLLInjectDetect,
    'rop-gadget': ROPGadget,
    'format-string': FormatString,
    'heap-analyzer': HeapAnalyzer,
    'fuzzer-gen': FuzzerGen,
    'shellcode-gen': ShellcodeGen,
    'packer-detect': PackerDetect,
    'anti-debug-detect': AntiDebugDetect,
    'binary-diff': BinaryDiff,
    'symbol-extract': SymbolExtract,
    'call-graph': CallGraph,
    'control-flow': ControlFlow,
    'binary-patch': BinaryPatch,
    'obfuscation-detect': ObfuscationDetect,
    'import-analyzer': ImportAnalyzer,
    'entropy-analyzer': EntropyAnalyzer,
    'binary-strings': BinaryStrings,
    'code-cave': CodeCave,
    'vtable-analyzer': VTableAnalyzer,
    'binary-sign': BinarySign,
    'disassembler': Disassembler,
    'decompiler': Decompiler,
    'binary-vuln': BinaryVuln,
    'firmware-extract': FirmwareExtract,
    'telegram-osint': TelegramOSINT,
    'discord-recon': DiscordRecon,
    'linkedin-enum': LinkedInEnum,
    'pastebin-monitor': PastebinMonitor,
    'wayback-recon': WaybackRecon,
    'cert-search': CertSearch,
    'dns-history': DNSHistory,
    'favicon-hash': FaviconHash,
    's3-finder': S3Finder,
    'google-dorking-adv': GoogleDorkingAdv,
    'github-recon': GitHubRecon,
    'twitter-osint': TwitterOSINT,
    'instagram-osint': InstagramOSINT,
    'face-search': FaceSearch,
    'email-osint': EmailOSINT,
    'company-recon': CompanyRecon,
    'geo-osint': GeoOSINT,
    'vehicle-osint': VehicleOSINT,
    'crypto-trace': CryptoTrace,
    'domain-monitor': DomainMonitor,
    'leak-search': LeakSearch,
    'web-archive': WebArchive,
    'image-forensics': ImageForensics,
    'social-media-map': SocialMediaMap,
    'website-monitor': WebsiteMonitor,
    'tech-profiler': TechProfiler,
    'network-osint': NetworkOSINT,
    'document-osint': DocumentOSINT,
    'phone-osint': PhoneOSINT,
    'username-search': UsernameSearch,
    'ip-reputation': IPReputation,
    'threat-intel': ThreatIntel,
    'malware-hash': MalwareHash,
    'subdomain-enum': SubdomainEnum,
    'asn-lookup': ASNLookup,
    'spray-attack': SprayAttack,
    'credential-test': CredentialTest,
    'pass-policy-audit': PassPolicyAudit,
    'mfa-bypass-check': MFABypassCheck,
    'session-hijack-detect': SessionHijackDetect,
    'cookie-analyzer': CookieAnalyzer,
    'oauth-abuse': OAuthAbuse,
    'saml-attack': SAMLAttack,
    'ticket-forge': TicketForge,
    'rainbow-gen': RainbowGen,
    'wordlist-gen': WordlistGen,
    'hash-identify': HashIdentify,
    'pass-strength': PassStrength,
    'brute-http': BruteHTTP,
    'brute-ssh': BruteSSH,
    'brute-ftp': BruteFTP,
    'brute-rdp': BruteRDP,
    'brute-mysql': BruteMySQL,
    'brute-smtp': BruteSMTP,
    'brute-ldap': BruteLDAP,
    'brute-custom': BruteCustom,
    'default-creds': DefaultCreds,
    'pass-reuse': PassReuse,
    'auth-token-test': AuthTokenTest,
    'sso-audit': SSOAudit,
    'totp-test': TOTPTest,
    'api-key-test': APIKeyTest,
    'cert-auth-test': CertAuthTest,
    'biometric-bypass': BiometricBypass,
    'captcha-test': CaptchaTest,
    'disk-forensics': DiskForensics,
    'registry-forensics': RegistryForensics,
    'browser-forensics': BrowserForensics,
    'email-forensics': EmailForensics,
    'timeline-gen': TimelineGen,
    'artifact-collect': ArtifactCollect,
    'volatility-wrap': VolatilityWrap,
    'yara-scan': YaraScan,
    'pcap-analyzer': PCAPAnalyzer,
    'usb-forensics': USBForensics,
    'event-log': EventLog,
    'prefetch-analyzer': PrefetchAnalyzer,
    'shadow-copy': ShadowCopy,
    'deleted-recovery': DeletedRecovery,
    'swap-analyzer': SwapAnalyzer,
    'hash-verify': HashVerify,
    'malware-triage': MalwareTriage,
    'stego-detect': SteganographyDetect,
    'encryption-detect': EncryptionDetect,
    'chain-custody': ChainCustody,
    'pci-dss': PCIDSS,
    'hipaa-audit': HIPAAAudit,
    'gdpr-scan': GDPRScan,
    'iso27001': ISO27001,
    'nist-assess': NISTAssess,
    'sox-audit': SOXAudit,
    'cis-benchmark': CISBenchmark,
    'stig-check': STIGCheck,
    'vuln-prioritize': VulnPrioritize,
    'risk-score': RiskScore,
    'policy-check': PolicyCheck,
    'baseline-audit': BaselineAudit,
    'access-review': AccessReview,
    'data-class': DataClass,
    'retention-check': RetentionCheck,
    'vendor-risk': VendorRisk,
    'incident-report': IncidentReport,
    'control-matrix': ControlMatrix,
    'gap-analysis': GapAnalysis,
    'maturity-assess': MaturityAssess,
    'audit-evidence': AuditEvidence,
    'privacy-impact': PrivacyImpact,
    'threat-model': ThreatModel,
    'security-roadmap': SecurityRoadmap,
    'compliance-report': ComplianceReport,
    'phish-template': PhishTemplate,
    'vishing-sim': VishingSim,
    'smishing-sim': SmishingSim,
    'pretexting-gen': PretextingGen,
    'clone-site': CloneSite,
    'credential-harvest': CredentialHarvest,
    'usb-drop-sim': USBDropSim,
    'watering-hole': WateringHole,
    'spear-phish': SpearPhish,
    'deepfake-detect': DeepfakeDetect,
    'social-profile': SocialProfile,
    'phish-detect': PhishDetect,
    'awareness-test': AwarenessTest,
    'qr-phish': QRPhish,
    'callback-phish': CallbackPhish,
    'android-debug': AndroidDebug,
    'ios-jailbreak': IOSJailbreak,
    'mobile-ssl-pin': MobileSSLPin,
    'app-permission': AppPermission,
    'smali-decompile': SmaliDecompile,
    'frida-scripts': FridaScripts,
    'objection-wrap': ObjectionWrap,
    'mobile-api-test': MobileAPITest,
    'cert-pin-bypass': CertPinBypass,
    'intent-fuzz': IntentFuzz,
    'mobile-storage': MobileStorage,
    'mobile-crypto': MobileCrypto,
    'mobile-network': MobileNetwork,
    'mobile-auth': MobileAuth,
    'app-clone-detect': AppCloneDetect,
    'mobile-malware': MobileMalware,
    'mobile-privacy': MobilePrivacy,
    'mobile-config': MobileConfig,
    'executive-report': ExecutiveReport,
    'compliance-rep': ComplianceRep,
    'risk-matrix': RiskMatrix,
    'vuln-timeline': VulnTimeline,
    'diff-report': DiffReport,
    'csv-export': CSVExport,
    'xml-export': XMLExport,
    'sarif-export': SARIFExport,
    'markdown-report': MarkdownReport,
    'chart-gen': ChartGen,
    'dashboard-gen': DashboardGen,
    'scan-compare': ScanCompare,
    'evidence-pack': EvidencePack,
    'auto-recon': AutoRecon,
    'auto-vuln': AutoVuln,
    'pipeline-builder': PipelineBuilder,
    'scheduler': Scheduler,
    'parallel-scan': ParallelScan,
    'result-aggregator': ResultAggregator,
    'notification-send': NotificationSend,
    'webhook-trigger': WebhookTrigger,
    'ci-cd-scan': CICDScan,
    'continuous-monitor': ContinuousMonitor,
    'scan-profile': ScanProfile,
    'tool-chain': ToolChain,
    'batch-scan': BatchScan,
    'scan-resume': ScanResume,
    'report-auto': ReportAuto,
    'target-import': TargetImport,
    'asset-discover': AssetDiscover,
    'change-detect': ChangeDetect,
    'workflow-template': WorkflowTemplate,
    'scan-queue': ScanQueue,
    'aes-attack': AESAttack,
    'rsa-attack': RSAAttack,
    'padding-oracle': PaddingOracle,
    'timing-attack': TimingAttack,
    'cert-audit': CertAudit,
    'tls-downgrade': TLSDowngrade,
    'ssl-strip-detect': SSLStripDetect,
    'pgp-audit': PGPAudit,
    'blockchain-analyze': BlockchainAnalyze,
    'random-test': RandomTest,
    'key-strength': KeyStrength,
    'cipher-detect': CipherDetect,
    'crypto-audit': CryptoAudit,
    'entropy-check': EntropyCheck,
    'hmac-test': HMACTest,
    'key-exchange': KeyExchange,
    'hash-collision': HashCollision,
    'crypto-downgrade': CryptoDowngrade,
    'payload-encode': PayloadEncode,
    'c2-detect': C2Detect,
    'honeypot-detect': HoneypotDetect,
    'sandbox-detect': SandboxDetect,
    'proxy-chain': ProxyChain,
    'tor-check': TorCheck,
    'vpn-leak-test': VPNLeakTest,
    'dns-leak-test': DNSLeakTest,
    'ip-rotate': IPRotate,
    'user-agent-gen': UserAgentGen,
    'reverse-shell': ReverseShell,
    'bind-shell': BindShell,
    'file-server': FileServer,
    'port-forward': PortForward,
    'network-pivot': NetworkPivot,
    'data-exfil-detect': DataExfilDetect,
    'log-cleaner-detect': LogCleanerDetect,
    'rootkit-detect': RootkitDetect,
    'backdoor-detect': BackdoorDetect,
    'webshell-detect': WebshellDetect,
    'config-audit': ConfigAudit,
    'service-enum': ServiceEnum,
    'cron-audit': CronAudit,
    'suid-check': SUIDCheck,
    'kernel-exploit': KernelExploit,

}

# === TOOLS BY CATEGORY (V3 + V4 Combined) ===
TOOLS_BY_CATEGORY = {
    # V3 Categories
    'Network': ['port-scan', 'ping', 'dns', 'traceroute', 'whois', 'ssl-check', 'ip-scan', 'sniffer', 'ddos-sim', 'mac-lookup', 'net-speed', 'subnet-calc', 'arp-scan', 'vlan-scan', 'snmp-walker'],
    'Web': ['sql-inject', 'xss-detect', 'csrf-detect', 'crawler', 'vuln-scan', 'subdomain', 'dorking', 'tech-stack', 'dir-brute', 'link-extract', 'admin-finder', 'headers-analyzer', 'proxy-finder', 'api-analyzer'],
    'OSINT': ['email-find', 'domain-info', 'ip-geo', 'metadata', 'dorking-search', 'user-search', 'git-recon', 'whois-history', 'shodan-search', 'phone-lookup', 'metadata-exif', 'social-analyzer', 'breach-check', 'dark-web-search'],
    'Utilities': ['password-gen', 'hash-tools', 'base64', 'url-encode', 'url-mask', 'url-shorten', 'html-tool', 'json-format', 'jwt-decoder', 'text-obfuscate', 'ip-convert', 'timestamp-convert', 'color-convert', 'unit-convert'],
    'Phishing': ['phishing-locator', 'web-phishing', 'email-phishing', 'url-masking', 'phishing-framework'],
    'Security': ['anti-ddos', 'waf-detect', 'vuln-db', 'firewall-bypass', 'ids-evasion'],
    'Clickjacking': ['clickjacking-check', 'clickjacking-make', 'anti-clickjacking'],
    'Crypto': ['hash-cracker', 'hash-gen', 'vigenere', 'xor-cipher', 'rsa-gen', 'stegano', 'file-encrypt'],
    'Wireless': ['beacon-flood', 'deauth', 'wifi-scan', 'wps-check'],
    'Database': ['sql-brute', 'mongodb-audit'],
    'Reporting': ['pdf-report', 'html-report'],
    'Exploit': ['searchsploit', 'msf-helper'],
    'Forensics': ['file-carver', 'memory-analyzer', 'log-forensics'],
    'Malware': ['malware-sandbox', 'pe-analyzer', 'string-extractor'],
    'Mobile Security': ['apk-analyzer', 'ios-analyzer'],
    'Cloud Security': ['aws-enum', 'azure-audit'],
    'IoT Security': ['mqtt-explorer', 'firmware-scan'],
    'Post-Exploitation': ['system-enum', 'priv-esc-check'],
    'Social Engineering': ['username-gen', 'payload-delivery'],
    # V4 Categories
    'Active Directory': ['ad-enum', 'kerberoast', 'asrep-roast', 'dcsync-detect', 'bloodhound-ingest', 'gpp-decrypt', 'ad-acl-audit', 'ldap-search', 'ntlm-relay-detect', 'ad-trust-audit', 'ad-pass-audit', 'ad-delegation', 'spn-scan', 'ad-cert-audit', 'ad-dns-enum', 'ad-gpo-audit', 'ad-replication', 'ad-sid-history', 'ad-forest-audit', 'ad-priv-users', 'ad-lockout', 'ad-stale-objects', 'ad-schema-audit', 'ad-backup-check', 'laps-audit', 'ad-svc-audit', 'ad-group-nesting', 'ad-recycle-bin', 'ad-admin-count', 'ad-func-level'],
    'Api Security': ['graphql-introspect', 'rest-fuzz', 'api-key-leak', 'swagger-scan', 'oauth-test', 'jwt-attack', 'cors-test', 'soap-audit', 'grpc-test', 'rate-limit-test', 'api-auth-bypass', 'api-enum', 'api-version-check', 'api-param-tamper', 'api-schema-validate', 'webhook-test', 'api-dos-test', 'api-injection', 'api-mass-assign', 'api-broken-auth', 'api-excessive-data', 'api-bola', 'api-ssrf', 'graphql-dos', 'api-response-header', 'api-error-disclosure', 'api-method-test', 'api-content-type', 'api-pagination', 'api-batch-test', 'api-cache-poison', 'api-race-condition', 'api-idempotency', 'api-file-upload', 'api-redirect'],
    'Container': ['docker-audit', 'k8s-pod-scan', 'container-escape-detect', 'image-scan', 'registry-enum', 'compose-audit', 'helm-audit', 'istio-check', 'runtime-scan', 'cgroup-escape', 'k8s-rbac', 'k8s-net-policy', 'k8s-secrets', 'docker-socket', 'k8s-admission', 'container-caps', 'k8s-etcd', 'dockerfile-lint', 'k8s-api-audit', 'container-forensics', 'k8s-psp', 'container-network', 'k8s-ingress', 'container-volume', 'k8s-service-mesh'],
    'Cloud': ['gcp-enum', 's3-bucket-scan', 'azure-ad-enum', 'k8s-cluster-audit', 'docker-escape-check', 'lambda-audit', 'iam-privesc', 'cloudtrail-audit', 'ecr-scan', 'terraform-scan', 'cloud-storage-enum', 'gcp-iam-audit', 'azure-blob-scan', 'cloud-firewall', 'serverless-audit', 'cloud-key-audit', 'cloud-network-audit', 'cloud-logging', 'cloud-compliance', 'cloud-cost-audit', 'eks-audit', 'aks-audit', 'gke-audit', 'cloud-db-audit', 'cloud-secret-scan', 'cloud-snapshot', 'multi-cloud-audit', 'cloud-dns-audit', 'cloud-waf-audit', 'cloud-cdn-audit', 'cloud-identity', 'cloud-endpoint', 'cloud-encryption', 'cloud-container-reg', 'cloud-api-gateway', 'cloud-lb-audit', 'cloud-vpn-audit', 'cloud-iam-roles'],
    'Web Advanced': ['xxe-detect', 'ssrf-detect', 'ssti-detect', 'prototype-pollute', 'deserialize-check', 'http-smuggle', 'cache-poison', 'cors-miscfg', 'open-redirect', 'host-header-inject', 'crlf-inject', 'lfi-detect', 'rfi-detect', 'command-inject', 'idor-detect', 'path-traversal', 'upload-vuln', 'session-fixation', 'business-logic', 'race-condition', 'subdomain-takeover', 'websocket-test', 'csrf-advanced', 'content-security', 'cookie-security', 'js-analyzer', 'waf-bypass', 'web-fingerprint', 'broken-access', 'security-headers', 'html-inject', 'web-param-mine', 'http2-test', 'graphql-vuln', 'ws-hijack', 'dom-xss', 'web-cache-deception', 'click-hijack', 'jwt-vuln'],
    'Network Advanced': ['bgp-hijack', 'dns-tunnel', 'icmp-tunnel', 'tcp-hijack', 'mitm-detect', 'rogue-dhcp', 'ipv6-recon', 'netbios-enum', 'smb-enum', 'rpc-enum', 'ntp-amp', 'ssdp-scan', 'ldap-enum', 'ftp-audit', 'smtp-enum', 'pop3-audit', 'imap-audit', 'redis-audit', 'memcache-audit', 'elastic-audit', 'kafka-audit', 'rabbit-audit', 'vnc-audit', 'rdp-audit', 'telnet-audit'],
    'Wireless Advanced': ['evil-twin', 'krack-test', 'pmkid-capture', 'wpa3-audit', 'bluetooth-scan', 'ble-enum', 'zigbee-scan', 'rfid-analyze', 'sdr-scan', 'drone-detect', 'wifi-deauth-detect', 'wifi-handshake', 'wifi-channel', 'wifi-rogue-ap', 'nfc-analyze', 'wifi-probe', 'wifi-karma', 'wifi-signal', 'wifi-wep-crack', 'wifi-enterprise'],
    'Binary': ['elf-analyzer', 'dll-inject-detect', 'rop-gadget', 'format-string', 'heap-analyzer', 'fuzzer-gen', 'shellcode-gen', 'packer-detect', 'anti-debug-detect', 'binary-diff', 'symbol-extract', 'call-graph', 'control-flow', 'binary-patch', 'obfuscation-detect', 'import-analyzer', 'entropy-analyzer', 'binary-strings', 'code-cave', 'vtable-analyzer', 'binary-sign', 'disassembler', 'decompiler', 'binary-vuln', 'firmware-extract'],
    'Osint': ['telegram-osint', 'discord-recon', 'linkedin-enum', 'pastebin-monitor', 'wayback-recon', 'cert-search', 'dns-history', 'favicon-hash', 's3-finder', 'google-dorking-adv', 'github-recon', 'twitter-osint', 'instagram-osint', 'face-search', 'email-osint', 'company-recon', 'geo-osint', 'vehicle-osint', 'crypto-trace', 'domain-monitor', 'leak-search', 'web-archive', 'image-forensics', 'social-media-map', 'website-monitor', 'tech-profiler', 'network-osint', 'document-osint', 'phone-osint', 'username-search', 'ip-reputation', 'threat-intel', 'malware-hash', 'subdomain-enum', 'asn-lookup'],
    'Password': ['spray-attack', 'credential-test', 'pass-policy-audit', 'mfa-bypass-check', 'session-hijack-detect', 'cookie-analyzer', 'oauth-abuse', 'saml-attack', 'ticket-forge', 'rainbow-gen', 'wordlist-gen', 'hash-identify', 'pass-strength', 'brute-http', 'brute-ssh', 'brute-ftp', 'brute-rdp', 'brute-mysql', 'brute-smtp', 'brute-ldap', 'brute-custom', 'default-creds', 'pass-reuse', 'auth-token-test', 'sso-audit', 'totp-test', 'api-key-test', 'cert-auth-test', 'biometric-bypass', 'captcha-test'],
    'Forensics': ['disk-forensics', 'registry-forensics', 'browser-forensics', 'email-forensics', 'timeline-gen', 'artifact-collect', 'volatility-wrap', 'yara-scan', 'pcap-analyzer', 'usb-forensics', 'event-log', 'prefetch-analyzer', 'shadow-copy', 'deleted-recovery', 'swap-analyzer', 'hash-verify', 'malware-triage', 'stego-detect', 'encryption-detect', 'chain-custody'],
    'Compliance': ['pci-dss', 'hipaa-audit', 'gdpr-scan', 'iso27001', 'nist-assess', 'sox-audit', 'cis-benchmark', 'stig-check', 'vuln-prioritize', 'risk-score', 'policy-check', 'baseline-audit', 'access-review', 'data-class', 'retention-check', 'vendor-risk', 'incident-report', 'control-matrix', 'gap-analysis', 'maturity-assess', 'audit-evidence', 'privacy-impact', 'threat-model', 'security-roadmap', 'compliance-report'],
    'Social': ['phish-template', 'vishing-sim', 'smishing-sim', 'pretexting-gen', 'clone-site', 'credential-harvest', 'usb-drop-sim', 'watering-hole', 'spear-phish', 'deepfake-detect', 'social-profile', 'phish-detect', 'awareness-test', 'qr-phish', 'callback-phish'],
    'Mobile': ['android-debug', 'ios-jailbreak', 'mobile-ssl-pin', 'app-permission', 'smali-decompile', 'frida-scripts', 'objection-wrap', 'mobile-api-test', 'cert-pin-bypass', 'intent-fuzz', 'mobile-storage', 'mobile-crypto', 'mobile-network', 'mobile-auth', 'app-clone-detect', 'mobile-malware', 'mobile-privacy', 'mobile-config'],
    'Reporting': ['executive-report', 'compliance-rep', 'risk-matrix', 'vuln-timeline', 'diff-report', 'csv-export', 'xml-export', 'sarif-export', 'markdown-report', 'chart-gen', 'dashboard-gen', 'scan-compare', 'evidence-pack'],
    'Automation': ['auto-recon', 'auto-vuln', 'pipeline-builder', 'scheduler', 'parallel-scan', 'result-aggregator', 'notification-send', 'webhook-trigger', 'ci-cd-scan', 'continuous-monitor', 'scan-profile', 'tool-chain', 'batch-scan', 'scan-resume', 'report-auto', 'target-import', 'asset-discover', 'change-detect', 'workflow-template', 'scan-queue'],
    'Crypto': ['aes-attack', 'rsa-attack', 'padding-oracle', 'timing-attack', 'cert-audit', 'tls-downgrade', 'ssl-strip-detect', 'pgp-audit', 'blockchain-analyze', 'random-test', 'key-strength', 'cipher-detect', 'crypto-audit', 'entropy-check', 'hmac-test', 'key-exchange', 'hash-collision', 'crypto-downgrade'],
    'Misc': ['payload-encode', 'c2-detect', 'honeypot-detect', 'sandbox-detect', 'proxy-chain', 'tor-check', 'vpn-leak-test', 'dns-leak-test', 'ip-rotate', 'user-agent-gen', 'reverse-shell', 'bind-shell', 'file-server', 'port-forward', 'network-pivot', 'data-exfil-detect', 'log-cleaner-detect', 'rootkit-detect', 'backdoor-detect', 'webshell-detect', 'config-audit', 'service-enum', 'cron-audit', 'suid-check', 'kernel-exploit'],

}


def get_license_text():
    """Read LICENSE file content"""
    for p in [Path(__file__).parent.parent / "LICENSE", Path.cwd() / "LICENSE"]:
        if p.exists():
            return p.read_text(encoding="utf-8", errors="ignore")
    return "LICENSE file not found."


def get_tos_text():
    """Read TERMS_OF_SERVICE.md content"""
    for p in [Path(__file__).parent.parent / "TERMS_OF_SERVICE.md", Path.cwd() / "TERMS_OF_SERVICE.md"]:
        if p.exists():
            return p.read_text(encoding="utf-8", errors="ignore")
    return "TERMS_OF_SERVICE.md file not found."


def print_banner():
    platform_info = PlatformDetector.get_platform_name()
    platform_emoji = PlatformDetector.get_platform_emoji()
    total = len(TOOLS_REGISTRY)
    banner = f"""
[bold cyan]
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║     █████╗ ██╗     ███████╗ ██████╗ ██████╗  █████╗ ███╗   ██╗   ║
    ║    ██╔══██╗██║     ██╔════╝██╔═══██╗██╔══██╗██╔══██╗████╗  ██║   ║
    ║    ███████║██║     █████╗  ██║   ██║██████╔╝███████║██╔██╗ ██║   ║
    ║    ██╔══██║██║     ██╔══╝  ██║   ██║██╔═══╝ ██╔══██║██║╚██╗██║   ║
    ║    ██║  ██║███████╗███████╗╚██████╔╝██║     ██║  ██║██║ ╚████║   ║
    ║    ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝   ║
    ║                                                                  ║
    ║    ████████╗███████╗███████╗████████╗                            ║
    ║    ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝                            ║
    ║       ██║   █████╗  ███████╗   ██║                               ║
    ║       ██║   ██╔══╝  ╚════██║   ██║                               ║
    ║       ██║   ███████╗███████║   ██║                               ║
    ║       ╚═╝   ╚══════╝╚══════╝   ╚═╝                               ║
    ║                                                                  ║
    ║  [bold white]🛡️  Aleopantest V4.0.0 PRO[/bold white] [dim]- Codename: HYDRA[/dim]              ║
    ║  [bold yellow]⚡ {total}+ Advanced Cybersecurity Tools[/bold yellow]                       ║
    ║  [dim]{platform_emoji} Platform: {platform_info}[/dim]                             ║
    ║  [dim]👤 by Aleocrophic Team[/dim]                                      ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
[/bold cyan]"""
    console.print(banner)


def print_tools_table():
    """Print tools table organized by category"""
    for category, tools in TOOLS_BY_CATEGORY.items():
        table = Table(title=f"🔧 {category}", show_header=True, header_style="bold cyan", border_style="dim")
        table.add_column("Tool ID", style="green", width=25)
        table.add_column("Class", style="yellow", width=30)
        table.add_column("Status", style="bold green", width=10)
        for tool_id in tools:
            cls = TOOLS_REGISTRY.get(tool_id)
            cls_name = cls.__name__ if cls and hasattr(cls, '__name__') else str(cls)
            table.add_row(tool_id, cls_name, "✓ Ready")
        console.print(table)
        console.print()


@click.group(invoke_without_command=True)
@click.option('--version', '-v', is_flag=True, help='Show version information')
@click.option('--license', '-lcs', 'show_license', is_flag=True, help='Show LICENSE')
@click.option('--tos', '-ts', is_flag=True, help='Show Terms of Service')
@click.pass_context
def cli(ctx, version, show_license, tos):
    """
    🛡️  Aleopantest V4.0.0 PRO - by Aleocrophic

    Advanced Cybersecurity Tool Suite with 548+ tools.

    ALIASES: You can also use 'alpnts' instead of 'aleopantest'.

    EXAMPLES:
      aleopantest --help              Show all commands
      aleopantest list-tools          List all available tools
      aleopantest run dns --domain example.com
      aleopantest run sql-inject --url http://example.com
      alpnts -v                       Show version (short alias)
      alpnts --license                Show LICENSE
      alpnts --tos                    Show Terms of Service
    """
    if version:
        from aleopantest import __version__
        console.print(f"[bold cyan]Aleopantest[/bold cyan] v{__version__} (Codename: HYDRA)")
        console.print(f"[dim]Platform: {PlatformDetector.get_platform_name()}[/dim]")
        console.print(f"[dim]Tools: {len(TOOLS_REGISTRY)}+ registered[/dim]")
        console.print(f"[dim]Python: {sys.version.split()[0]}[/dim]")
        return
    if show_license:
        console.print(Panel(get_license_text(), title="📄 LICENSE", border_style="cyan"))
        return
    if tos:
        console.print(Panel(get_tos_text(), title="⚖️ TERMS OF SERVICE", border_style="yellow"))
        return
    if ctx.invoked_subcommand is None:
        print_banner()
        console.print("[bold]Quick Start:[/bold]")
        console.print("  [cyan]aleopantest list-tools[/cyan]    List all tools")
        console.print("  [cyan]aleopantest info[/cyan]          Show framework info")
        console.print("  [cyan]aleopantest run <tool>[/cyan]    Run a specific tool")
        console.print("  [cyan]aleopantest tui[/cyan]           Launch TUI dashboard")
        console.print("  [cyan]aleopantest web[/cyan]           Launch Web dashboard")
        console.print()
        console.print("[dim]Tip: Use 'alpnts' as a shortcut for 'aleopantest'[/dim]")
        console.print("[dim]Tip: Use 'aleopantest --license' or 'aleopantest --tos'[/dim]")


@cli.command()
def info():
    """Show tool information and statistics"""
    from aleopantest import __version__
    print_banner()
    table = Table(title="📊 Framework Statistics", border_style="cyan")
    table.add_column("Metric", style="bold")
    table.add_column("Value", style="green")
    table.add_row("Version", __version__)
    table.add_row("Codename", "HYDRA")
    table.add_row("Total Tools", str(len(TOOLS_REGISTRY)))
    table.add_row("Categories", str(len(TOOLS_BY_CATEGORY)))
    table.add_row("Platform", PlatformDetector.get_platform_name())
    table.add_row("Python", sys.version.split()[0])
    table.add_row("License", "MIT - Educational Use Only")
    console.print(table)


@cli.command()
def list_tools():
    """List all available tools"""
    print_banner()
    console.print(f"[bold]📋 Total Tools: {len(TOOLS_REGISTRY)}[/bold]\n")
    print_tools_table()


@cli.command()
def tui():
    """Launch the modern TUI dashboard"""
    from aleopantest.tui import AleopantestTUI
    app = AleopantestTUI()
    app.run()


@cli.command()
@click.option('--host', default='127.0.0.1', help='Host to bind')
@click.option('--port', default=8002, help='Port to listen on')
def web(host, port):
    """Launch the modern Web Dashboard"""
    from aleopantest.core.web_server import start_web_server
    console.print(f"[bold cyan]🌐 Starting Web Dashboard at http://{host}:{port}[/bold cyan]")
    start_web_server(host=host, port=port)


@cli.command()
@click.argument('tool_id')
@click.option('--target', '-t', help='Target (URL, IP, domain)')
@click.option('--host', '-H', help='Host/IP')
@click.option('--domain', '-d', help='Domain name')
@click.option('--url', '-u', help='URL target')
@click.option('--ip', help='IP address')
@click.option('--port', '-p', help='Port/range')
@click.option('--output', '-o', help='Output file')
@click.option('--format', 'fmt', help='Output format')
@click.option('--threads', type=int, default=10, help='Thread count')
@click.option('--timeout', type=int, default=30, help='Timeout seconds')
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode')
@click.option('--verbose', '-V', is_flag=True, help='Verbose output')
def run(tool_id, target, host, domain, url, ip, port, output, fmt, threads, timeout, interactive, verbose, **kwargs):
    """Run a specific security tool

    EXAMPLES:
      aleopantest run dns --domain target.com
      aleopantest run port-scan --host 192.168.1.1 --port 1-1000
      aleopantest run sql-inject --url http://example.com
      aleopantest run ip-geo --ip 8.8.8.8
      alpnts run ad-enum --target dc.company.com
    """
    if tool_id not in TOOLS_REGISTRY:
        console.print(f"[red]❌ Unknown tool: {tool_id}[/red]")
        console.print("[yellow]Use 'aleopantest list-tools' to see available tools[/yellow]")
        return

    tool_class = TOOLS_REGISTRY[tool_id]
    tool = tool_class()

    params = {}
    if target: params['target'] = target
    if host: params['host'] = host
    if domain: params['domain'] = domain
    if url: params['url'] = url
    if ip: params['ip'] = ip
    if port: params['port'] = port
    if threads: params['threads'] = threads
    if timeout: params['timeout'] = timeout

    # Auto-detect target from various params
    if not params.get('target'):
        params['target'] = host or domain or url or ip

    if interactive and not params.get('target'):
        from aleopantest.interactive import prompt_for_parameters
        params = prompt_for_parameters(tool_id, tool.metadata)
        if not params:
            return

    console.print(f"\n[bold cyan]🚀 Running {tool.metadata.name}...[/bold cyan]")

    try:
        result = tool.run(**params)
        if result:
            console.print_json(data=result)
            send_to_web_dashboard(tool_id, result)
            if output:
                if fmt == 'txt':
                    tool.export_txt(output)
                else:
                    tool.export_json(output)
                console.print(f"[green]✓ Results saved to {output}[/green]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
