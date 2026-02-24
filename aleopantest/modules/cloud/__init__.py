"""Cloud tools module initialization"""
from aleopantest.core.tool_helper import robust_import

AWSEnumerator = robust_import("aleopantest.modules.cloud.aws_enum", "AWSEnumerator")
AzureAudit = robust_import("aleopantest.modules.cloud.azure_audit", "AzureAudit")

GCPEnum = robust_import("aleopantest.modules.cloud.gcp_enum", "GCPEnum")
S3BucketScan = robust_import("aleopantest.modules.cloud.s3_bucket_scan", "S3BucketScan")
AzureADEnum = robust_import("aleopantest.modules.cloud.azure_ad_enum", "AzureADEnum")
K8sClusterAudit = robust_import("aleopantest.modules.cloud.k8s_cluster_audit", "K8sClusterAudit")
DockerEscapeCheck = robust_import("aleopantest.modules.cloud.docker_escape_check", "DockerEscapeCheck")
LambdaAudit = robust_import("aleopantest.modules.cloud.lambda_audit", "LambdaAudit")
IAMPrivesc = robust_import("aleopantest.modules.cloud.iam_privesc", "IAMPrivesc")
CloudTrailAudit = robust_import("aleopantest.modules.cloud.cloudtrail_audit", "CloudTrailAudit")
ECRScan = robust_import("aleopantest.modules.cloud.ecr_scan", "ECRScan")
TerraformScan = robust_import("aleopantest.modules.cloud.terraform_scan", "TerraformScan")
CloudStorageEnum = robust_import("aleopantest.modules.cloud.cloud_storage_enum", "CloudStorageEnum")
GCPIAMAudit = robust_import("aleopantest.modules.cloud.gcp_iam_audit", "GCPIAMAudit")
AzureBlobScan = robust_import("aleopantest.modules.cloud.azure_blob_scan", "AzureBlobScan")
CloudFirewall = robust_import("aleopantest.modules.cloud.cloud_firewall", "CloudFirewall")
ServerlessAudit = robust_import("aleopantest.modules.cloud.serverless_audit", "ServerlessAudit")
CloudKeyAudit = robust_import("aleopantest.modules.cloud.cloud_key_audit", "CloudKeyAudit")
CloudNetworkAudit = robust_import("aleopantest.modules.cloud.cloud_network_audit", "CloudNetworkAudit")
CloudLogging = robust_import("aleopantest.modules.cloud.cloud_logging", "CloudLogging")
CloudCompliance = robust_import("aleopantest.modules.cloud.cloud_compliance", "CloudCompliance")
CloudCostAudit = robust_import("aleopantest.modules.cloud.cloud_cost_audit", "CloudCostAudit")
EKSAudit = robust_import("aleopantest.modules.cloud.eks_audit", "EKSAudit")
AKSAudit = robust_import("aleopantest.modules.cloud.aks_audit", "AKSAudit")
GKEAudit = robust_import("aleopantest.modules.cloud.gke_audit", "GKEAudit")
CloudDBAudit = robust_import("aleopantest.modules.cloud.cloud_db_audit", "CloudDBAudit")
CloudSecretScan = robust_import("aleopantest.modules.cloud.cloud_secret_scan", "CloudSecretScan")
CloudSnapshot = robust_import("aleopantest.modules.cloud.cloud_snapshot", "CloudSnapshot")
MultiCloudAudit = robust_import("aleopantest.modules.cloud.multi_cloud_audit", "MultiCloudAudit")
CloudDNSAudit = robust_import("aleopantest.modules.cloud.cloud_dns_audit", "CloudDNSAudit")
CloudWAFAudit = robust_import("aleopantest.modules.cloud.cloud_waf_audit", "CloudWAFAudit")
CloudCDNAudit = robust_import("aleopantest.modules.cloud.cloud_cdn_audit", "CloudCDNAudit")
CloudIdentity = robust_import("aleopantest.modules.cloud.cloud_identity", "CloudIdentity")
CloudEndpoint = robust_import("aleopantest.modules.cloud.cloud_endpoint", "CloudEndpoint")
CloudEncryption = robust_import("aleopantest.modules.cloud.cloud_encryption", "CloudEncryption")
CloudContainerReg = robust_import("aleopantest.modules.cloud.cloud_container_reg", "CloudContainerReg")
CloudAPIGateway = robust_import("aleopantest.modules.cloud.cloud_api_gateway", "CloudAPIGateway")
CloudLBAudit = robust_import("aleopantest.modules.cloud.cloud_lb_audit", "CloudLBAudit")
CloudVPNAudit = robust_import("aleopantest.modules.cloud.cloud_vpn_audit", "CloudVPNAudit")
CloudIAMRoles = robust_import("aleopantest.modules.cloud.cloud_iam_roles", "CloudIAMRoles")

__all__ = ['AWSEnumerator', 'AzureAudit'
    'GCPEnum',
    'S3BucketScan',
    'AzureADEnum',
    'K8sClusterAudit',
    'DockerEscapeCheck',
    'LambdaAudit',
    'IAMPrivesc',
    'CloudTrailAudit',
    'ECRScan',
    'TerraformScan',
    'CloudStorageEnum',
    'GCPIAMAudit',
    'AzureBlobScan',
    'CloudFirewall',
    'ServerlessAudit',
    'CloudKeyAudit',
    'CloudNetworkAudit',
    'CloudLogging',
    'CloudCompliance',
    'CloudCostAudit',
    'EKSAudit',
    'AKSAudit',
    'GKEAudit',
    'CloudDBAudit',
    'CloudSecretScan',
    'CloudSnapshot',
    'MultiCloudAudit',
    'CloudDNSAudit',
    'CloudWAFAudit',
    'CloudCDNAudit',
    'CloudIdentity',
    'CloudEndpoint',
    'CloudEncryption',
    'CloudContainerReg',
    'CloudAPIGateway',
    'CloudLBAudit',
    'CloudVPNAudit',
    'CloudIAMRoles',
]
