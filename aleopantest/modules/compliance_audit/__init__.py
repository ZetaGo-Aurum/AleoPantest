"""Compliance module - Aleopantest V4.0.0"""
from aleopantest.core.tool_helper import robust_import

PCIDSS = robust_import("aleopantest.modules.compliance_audit.pci_dss", "PCIDSS")
HIPAAAudit = robust_import("aleopantest.modules.compliance_audit.hipaa_audit", "HIPAAAudit")
GDPRScan = robust_import("aleopantest.modules.compliance_audit.gdpr_scan", "GDPRScan")
ISO27001 = robust_import("aleopantest.modules.compliance_audit.iso27001", "ISO27001")
NISTAssess = robust_import("aleopantest.modules.compliance_audit.nist_assess", "NISTAssess")
SOXAudit = robust_import("aleopantest.modules.compliance_audit.sox_audit", "SOXAudit")
CISBenchmark = robust_import("aleopantest.modules.compliance_audit.cis_benchmark", "CISBenchmark")
STIGCheck = robust_import("aleopantest.modules.compliance_audit.stig_check", "STIGCheck")
VulnPrioritize = robust_import("aleopantest.modules.compliance_audit.vuln_prioritize", "VulnPrioritize")
RiskScore = robust_import("aleopantest.modules.compliance_audit.risk_score", "RiskScore")
PolicyCheck = robust_import("aleopantest.modules.compliance_audit.policy_check", "PolicyCheck")
BaselineAudit = robust_import("aleopantest.modules.compliance_audit.baseline_audit", "BaselineAudit")
AccessReview = robust_import("aleopantest.modules.compliance_audit.access_review", "AccessReview")
DataClass = robust_import("aleopantest.modules.compliance_audit.data_class", "DataClass")
RetentionCheck = robust_import("aleopantest.modules.compliance_audit.retention_check", "RetentionCheck")
VendorRisk = robust_import("aleopantest.modules.compliance_audit.vendor_risk", "VendorRisk")
IncidentReport = robust_import("aleopantest.modules.compliance_audit.incident_report", "IncidentReport")
ControlMatrix = robust_import("aleopantest.modules.compliance_audit.control_matrix", "ControlMatrix")
GapAnalysis = robust_import("aleopantest.modules.compliance_audit.gap_analysis", "GapAnalysis")
MaturityAssess = robust_import("aleopantest.modules.compliance_audit.maturity_assess", "MaturityAssess")
AuditEvidence = robust_import("aleopantest.modules.compliance_audit.audit_evidence", "AuditEvidence")
PrivacyImpact = robust_import("aleopantest.modules.compliance_audit.privacy_impact", "PrivacyImpact")
ThreatModel = robust_import("aleopantest.modules.compliance_audit.threat_model", "ThreatModel")
SecurityRoadmap = robust_import("aleopantest.modules.compliance_audit.security_roadmap", "SecurityRoadmap")
ComplianceReport = robust_import("aleopantest.modules.compliance_audit.compliance_report", "ComplianceReport")

__all__ = [
    'PCIDSS',
    'HIPAAAudit',
    'GDPRScan',
    'ISO27001',
    'NISTAssess',
    'SOXAudit',
    'CISBenchmark',
    'STIGCheck',
    'VulnPrioritize',
    'RiskScore',
    'PolicyCheck',
    'BaselineAudit',
    'AccessReview',
    'DataClass',
    'RetentionCheck',
    'VendorRisk',
    'IncidentReport',
    'ControlMatrix',
    'GapAnalysis',
    'MaturityAssess',
    'AuditEvidence',
    'PrivacyImpact',
    'ThreatModel',
    'SecurityRoadmap',
    'ComplianceReport',
]
