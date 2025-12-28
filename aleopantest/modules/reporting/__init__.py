from aleopantest.core.tool_helper import robust_import

PDFReportGenerator = robust_import("aleopantest.modules.reporting.pdf_report", "PDFReportGenerator")
HTMLReportGenerator = robust_import("aleopantest.modules.reporting.html_report", "HTMLReportGenerator")

__all__ = ["PDFReportGenerator", "HTMLReportGenerator"]
