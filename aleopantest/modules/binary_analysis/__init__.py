"""Binary module - Aleopantest V4.0.0"""
from aleopantest.core.tool_helper import robust_import

ELFAnalyzer = robust_import("aleopantest.modules.binary_analysis.elf_analyzer", "ELFAnalyzer")
DLLInjectDetect = robust_import("aleopantest.modules.binary_analysis.dll_inject_detect", "DLLInjectDetect")
ROPGadget = robust_import("aleopantest.modules.binary_analysis.rop_gadget", "ROPGadget")
FormatString = robust_import("aleopantest.modules.binary_analysis.format_string", "FormatString")
HeapAnalyzer = robust_import("aleopantest.modules.binary_analysis.heap_analyzer", "HeapAnalyzer")
FuzzerGen = robust_import("aleopantest.modules.binary_analysis.fuzzer_gen", "FuzzerGen")
ShellcodeGen = robust_import("aleopantest.modules.binary_analysis.shellcode_gen", "ShellcodeGen")
PackerDetect = robust_import("aleopantest.modules.binary_analysis.packer_detect", "PackerDetect")
AntiDebugDetect = robust_import("aleopantest.modules.binary_analysis.anti_debug_detect", "AntiDebugDetect")
BinaryDiff = robust_import("aleopantest.modules.binary_analysis.binary_diff", "BinaryDiff")
SymbolExtract = robust_import("aleopantest.modules.binary_analysis.symbol_extract", "SymbolExtract")
CallGraph = robust_import("aleopantest.modules.binary_analysis.call_graph", "CallGraph")
ControlFlow = robust_import("aleopantest.modules.binary_analysis.control_flow", "ControlFlow")
BinaryPatch = robust_import("aleopantest.modules.binary_analysis.binary_patch", "BinaryPatch")
ObfuscationDetect = robust_import("aleopantest.modules.binary_analysis.obfuscation_detect", "ObfuscationDetect")
ImportAnalyzer = robust_import("aleopantest.modules.binary_analysis.import_analyzer", "ImportAnalyzer")
EntropyAnalyzer = robust_import("aleopantest.modules.binary_analysis.entropy_analyzer", "EntropyAnalyzer")
BinaryStrings = robust_import("aleopantest.modules.binary_analysis.binary_strings", "BinaryStrings")
CodeCave = robust_import("aleopantest.modules.binary_analysis.code_cave", "CodeCave")
VTableAnalyzer = robust_import("aleopantest.modules.binary_analysis.vtable_analyzer", "VTableAnalyzer")
BinarySign = robust_import("aleopantest.modules.binary_analysis.binary_sign", "BinarySign")
Disassembler = robust_import("aleopantest.modules.binary_analysis.disassembler", "Disassembler")
Decompiler = robust_import("aleopantest.modules.binary_analysis.decompiler", "Decompiler")
BinaryVuln = robust_import("aleopantest.modules.binary_analysis.binary_vuln", "BinaryVuln")
FirmwareExtract = robust_import("aleopantest.modules.binary_analysis.firmware_extract", "FirmwareExtract")

__all__ = [
    'ELFAnalyzer',
    'DLLInjectDetect',
    'ROPGadget',
    'FormatString',
    'HeapAnalyzer',
    'FuzzerGen',
    'ShellcodeGen',
    'PackerDetect',
    'AntiDebugDetect',
    'BinaryDiff',
    'SymbolExtract',
    'CallGraph',
    'ControlFlow',
    'BinaryPatch',
    'ObfuscationDetect',
    'ImportAnalyzer',
    'EntropyAnalyzer',
    'BinaryStrings',
    'CodeCave',
    'VTableAnalyzer',
    'BinarySign',
    'Disassembler',
    'Decompiler',
    'BinaryVuln',
    'FirmwareExtract',
]
