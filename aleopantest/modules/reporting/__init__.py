from aleopantest.core.tool_helper import robust_import

PDFReportGenerator = robust_import("aleopantest.modules.reporting.pdf_report", "PDFReportGenerator")
HTMLReportGenerator = robust_import("aleopantest.modules.reporting.html_report", "HTMLReportGenerator")

ExecutiveReport = robust_import("aleopantest.modules.reporting.executive_report", "ExecutiveReport")
ComplianceRep = robust_import("aleopantest.modules.reporting.compliance_rep", "ComplianceRep")
RiskMatrix = robust_import("aleopantest.modules.reporting.risk_matrix", "RiskMatrix")
VulnTimeline = robust_import("aleopantest.modules.reporting.vuln_timeline", "VulnTimeline")
DiffReport = robust_import("aleopantest.modules.reporting.diff_report", "DiffReport")
CSVExport = robust_import("aleopantest.modules.reporting.csv_export", "CSVExport")
XMLExport = robust_import("aleopantest.modules.reporting.xml_export", "XMLExport")
SARIFExport = robust_import("aleopantest.modules.reporting.sarif_export", "SARIFExport")
MarkdownReport = robust_import("aleopantest.modules.reporting.markdown_report", "MarkdownReport")
ChartGen = robust_import("aleopantest.modules.reporting.chart_gen", "ChartGen")
DashboardGen = robust_import("aleopantest.modules.reporting.dashboard_gen", "DashboardGen")
ScanCompare = robust_import("aleopantest.modules.reporting.scan_compare", "ScanCompare")
EvidencePack = robust_import("aleopantest.modules.reporting.evidence_pack", "EvidencePack")

__all__ = ["PDFReportGenerator", "HTMLReportGenerator"
    'ExecutiveReport',
    'ComplianceRep',
    'RiskMatrix',
    'VulnTimeline',
    'DiffReport',
    'CSVExport',
    'XMLExport',
    'SARIFExport',
    'MarkdownReport',
    'ChartGen',
    'DashboardGen',
    'ScanCompare',
    'EvidencePack',
]
