"""Automation module - Aleopantest V4.0.0"""
from aleopantest.core.tool_helper import robust_import

AutoRecon = robust_import("aleopantest.modules.automation_pipeline.auto_recon", "AutoRecon")
AutoVuln = robust_import("aleopantest.modules.automation_pipeline.auto_vuln", "AutoVuln")
PipelineBuilder = robust_import("aleopantest.modules.automation_pipeline.pipeline_builder", "PipelineBuilder")
Scheduler = robust_import("aleopantest.modules.automation_pipeline.scheduler", "Scheduler")
ParallelScan = robust_import("aleopantest.modules.automation_pipeline.parallel_scan", "ParallelScan")
ResultAggregator = robust_import("aleopantest.modules.automation_pipeline.result_aggregator", "ResultAggregator")
NotificationSend = robust_import("aleopantest.modules.automation_pipeline.notification_send", "NotificationSend")
WebhookTrigger = robust_import("aleopantest.modules.automation_pipeline.webhook_trigger", "WebhookTrigger")
CICDScan = robust_import("aleopantest.modules.automation_pipeline.ci_cd_scan", "CICDScan")
ContinuousMonitor = robust_import("aleopantest.modules.automation_pipeline.continuous_monitor", "ContinuousMonitor")
ScanProfile = robust_import("aleopantest.modules.automation_pipeline.scan_profile", "ScanProfile")
ToolChain = robust_import("aleopantest.modules.automation_pipeline.tool_chain", "ToolChain")
BatchScan = robust_import("aleopantest.modules.automation_pipeline.batch_scan", "BatchScan")
ScanResume = robust_import("aleopantest.modules.automation_pipeline.scan_resume", "ScanResume")
ReportAuto = robust_import("aleopantest.modules.automation_pipeline.report_auto", "ReportAuto")
TargetImport = robust_import("aleopantest.modules.automation_pipeline.target_import", "TargetImport")
AssetDiscover = robust_import("aleopantest.modules.automation_pipeline.asset_discover", "AssetDiscover")
ChangeDetect = robust_import("aleopantest.modules.automation_pipeline.change_detect", "ChangeDetect")
WorkflowTemplate = robust_import("aleopantest.modules.automation_pipeline.workflow_template", "WorkflowTemplate")
ScanQueue = robust_import("aleopantest.modules.automation_pipeline.scan_queue", "ScanQueue")

__all__ = [
    'AutoRecon',
    'AutoVuln',
    'PipelineBuilder',
    'Scheduler',
    'ParallelScan',
    'ResultAggregator',
    'NotificationSend',
    'WebhookTrigger',
    'CICDScan',
    'ContinuousMonitor',
    'ScanProfile',
    'ToolChain',
    'BatchScan',
    'ScanResume',
    'ReportAuto',
    'TargetImport',
    'AssetDiscover',
    'ChangeDetect',
    'WorkflowTemplate',
    'ScanQueue',
]
