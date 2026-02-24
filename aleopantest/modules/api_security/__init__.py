"""Api Security module - Aleopantest V4.0.0"""
from aleopantest.core.tool_helper import robust_import

GraphQLIntrospect = robust_import("aleopantest.modules.api_security.graphql_introspect", "GraphQLIntrospect")
RESTFuzzer = robust_import("aleopantest.modules.api_security.rest_fuzz", "RESTFuzzer")
APIKeyLeak = robust_import("aleopantest.modules.api_security.api_key_leak", "APIKeyLeak")
SwaggerScan = robust_import("aleopantest.modules.api_security.swagger_scan", "SwaggerScan")
OAuthTest = robust_import("aleopantest.modules.api_security.oauth_test", "OAuthTest")
JWTAttack = robust_import("aleopantest.modules.api_security.jwt_attack", "JWTAttack")
CORSTest = robust_import("aleopantest.modules.api_security.cors_test", "CORSTest")
SOAPAudit = robust_import("aleopantest.modules.api_security.soap_audit", "SOAPAudit")
GRPCTest = robust_import("aleopantest.modules.api_security.grpc_test", "GRPCTest")
RateLimitTest = robust_import("aleopantest.modules.api_security.rate_limit_test", "RateLimitTest")
APIAuthBypass = robust_import("aleopantest.modules.api_security.api_auth_bypass", "APIAuthBypass")
APIEnum = robust_import("aleopantest.modules.api_security.api_enum", "APIEnum")
APIVersionCheck = robust_import("aleopantest.modules.api_security.api_version_check", "APIVersionCheck")
APIParamTamper = robust_import("aleopantest.modules.api_security.api_param_tamper", "APIParamTamper")
APISchemaValidate = robust_import("aleopantest.modules.api_security.api_schema_validate", "APISchemaValidate")
WebhookTest = robust_import("aleopantest.modules.api_security.webhook_test", "WebhookTest")
APIDOSTest = robust_import("aleopantest.modules.api_security.api_dos_test", "APIDOSTest")
APIInjection = robust_import("aleopantest.modules.api_security.api_injection", "APIInjection")
APIMassAssign = robust_import("aleopantest.modules.api_security.api_mass_assign", "APIMassAssign")
APIBrokenAuth = robust_import("aleopantest.modules.api_security.api_broken_auth", "APIBrokenAuth")
APIExcessiveData = robust_import("aleopantest.modules.api_security.api_excessive_data", "APIExcessiveData")
APIBOLA = robust_import("aleopantest.modules.api_security.api_bola", "APIBOLA")
APISSRF = robust_import("aleopantest.modules.api_security.api_ssrf", "APISSRF")
APIGraphQLDoS = robust_import("aleopantest.modules.api_security.api_graphql_dos", "APIGraphQLDoS")
APIResponseHeader = robust_import("aleopantest.modules.api_security.api_response_header", "APIResponseHeader")
APIErrorDisclosure = robust_import("aleopantest.modules.api_security.api_error_disclosure", "APIErrorDisclosure")
APIMethodTest = robust_import("aleopantest.modules.api_security.api_method_test", "APIMethodTest")
APIContentType = robust_import("aleopantest.modules.api_security.api_content_type", "APIContentType")
APIPagination = robust_import("aleopantest.modules.api_security.api_pagination", "APIPagination")
APIBatchTest = robust_import("aleopantest.modules.api_security.api_batch_test", "APIBatchTest")
APICachePoison = robust_import("aleopantest.modules.api_security.api_cache_poison", "APICachePoison")
APIRaceCondition = robust_import("aleopantest.modules.api_security.api_race_condition", "APIRaceCondition")
APIIdempotency = robust_import("aleopantest.modules.api_security.api_idempotency", "APIIdempotency")
APIFileUpload = robust_import("aleopantest.modules.api_security.api_file_upload", "APIFileUpload")
APIRedirect = robust_import("aleopantest.modules.api_security.api_redirect", "APIRedirect")

__all__ = [
    'GraphQLIntrospect',
    'RESTFuzzer',
    'APIKeyLeak',
    'SwaggerScan',
    'OAuthTest',
    'JWTAttack',
    'CORSTest',
    'SOAPAudit',
    'GRPCTest',
    'RateLimitTest',
    'APIAuthBypass',
    'APIEnum',
    'APIVersionCheck',
    'APIParamTamper',
    'APISchemaValidate',
    'WebhookTest',
    'APIDOSTest',
    'APIInjection',
    'APIMassAssign',
    'APIBrokenAuth',
    'APIExcessiveData',
    'APIBOLA',
    'APISSRF',
    'APIGraphQLDoS',
    'APIResponseHeader',
    'APIErrorDisclosure',
    'APIMethodTest',
    'APIContentType',
    'APIPagination',
    'APIBatchTest',
    'APICachePoison',
    'APIRaceCondition',
    'APIIdempotency',
    'APIFileUpload',
    'APIRedirect',
]
