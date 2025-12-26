"""Cross-platform compatibility layer for AloPantest"""
import os
import sys
import platform
import subprocess
from typing import Dict, Any, Optional

class PlatformDetector:
    """Detect and handle platform-specific configurations"""
    
    @staticmethod
    def get_info() -> Dict[str, str]:
        """Get detailed platform information"""
        system = platform.system().lower()
        release = platform.release()
        version = platform.version()
        
        # Detect WSL
        is_wsl = False
        if system == 'linux':
            if 'microsoft' in version.lower() or 'microsoft' in release.lower():
                is_wsl = True
        
        # Detect Termux
        is_termux = False
        if system == 'linux' and os.environ.get('TERMUX_VERSION'):
            is_termux = True
            
        return {
            'system': system,
            'release': release,
            'version': version,
            'is_wsl': is_wsl,
            'is_termux': is_termux,
            'machine': platform.machine(),
            'python_version': platform.python_version()
        }

    @staticmethod
    def is_windows() -> bool:
        return platform.system().lower() == 'windows'

    @staticmethod
    def is_macos() -> bool:
        return platform.system().lower() == 'darwin'

    @staticmethod
    def is_linux() -> bool:
        return platform.system().lower() == 'linux'

    @staticmethod
    def is_wsl() -> bool:
        info = PlatformDetector.get_info()
        return info['is_wsl']

    @staticmethod
    def is_termux() -> bool:
        return os.environ.get('TERMUX_VERSION') is not None

    @staticmethod
    def get_platform_name() -> str:
        if PlatformDetector.is_termux():
            return "Android (Termux)"
        if PlatformDetector.is_wsl():
            return "Windows (WSL)"
        if PlatformDetector.is_windows():
            return "Windows"
        if PlatformDetector.is_macos():
            return "macOS"
        return f"Linux ({platform.freedesktop_os_release().get('NAME', 'Unknown')})" if hasattr(platform, 'freedesktop_os_release') else "Linux"

class PlatformOptimizer:
    """Optimize resource management based on platform"""
    
    @staticmethod
    def get_optimal_threads() -> int:
        """Get optimal number of threads for the current platform"""
        cpu_count = os.cpu_count() or 1
        
        if PlatformDetector.is_termux():
            # Termux is often on mobile devices, keep threads low
            return min(cpu_count, 4)
        if PlatformDetector.is_wsl() or PlatformDetector.is_windows():
            return min(cpu_count * 2, 16)
        
        return min(cpu_count * 2, 32)

    @staticmethod
    def check_dependencies(deps: list) -> Dict[str, bool]:
        """Check if external system dependencies are installed"""
        results = {}
        for dep in deps:
            try:
                # Use 'which' on Unix and 'where' on Windows
                cmd = ['which', dep] if not PlatformDetector.is_windows() else ['where', dep]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                results[dep] = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                results[dep] = False
        return results
