"""Platform detection and resource optimization for Aleopantest V4.0.0"""
import platform
import os
import sys
import shutil
import multiprocessing


class PlatformDetector:
    """Detect operating system and specific environments like WSL, Termux, Kali"""
    
    _cached_info = None
    
    @staticmethod
    def get_info():
        """Get detailed platform information with caching"""
        if PlatformDetector._cached_info:
            return PlatformDetector._cached_info
            
        system = platform.system().lower()
        is_wsl = False
        is_termux = 'TERMUX_VERSION' in os.environ or os.path.exists('/data/data/com.termux')
        is_kali = False
        is_parrot = False
        is_macos = system == 'darwin'
        is_windows = system == 'windows'
        is_linux = system == 'linux'
        
        if is_linux:
            try:
                with open('/proc/version', 'r') as f:
                    version_str = f.read().lower()
                    if 'microsoft' in version_str or 'wsl' in version_str:
                        is_wsl = True
            except (OSError, IOError):
                pass
            
            # Detect Kali Linux
            try:
                with open('/etc/os-release', 'r') as f:
                    os_release = f.read().lower()
                    if 'kali' in os_release:
                        is_kali = True
                    elif 'parrot' in os_release:
                        is_parrot = True
            except (OSError, IOError):
                pass
        
        PlatformDetector._cached_info = {
            'system': system,
            'is_wsl': is_wsl,
            'is_termux': is_termux,
            'is_kali': is_kali,
            'is_parrot': is_parrot,
            'is_macos': is_macos,
            'is_windows': is_windows,
            'is_linux': is_linux,
            'release': platform.release(),
            'machine': platform.machine(),
            'python_version': platform.python_version(),
            'arch': platform.architecture()[0],
        }
        return PlatformDetector._cached_info
    
    @staticmethod
    def get_platform_name():
        """Get a human-readable platform name"""
        info = PlatformDetector.get_info()
        if info['is_termux']:
            return "Termux (Android)"
        if info['is_wsl']:
            return "Windows Subsystem for Linux (WSL)"
        if info['is_kali']:
            return "Kali Linux"
        if info['is_parrot']:
            return "Parrot Security OS"
        if info['is_macos']:
            return "macOS"
        if info['is_windows']:
            return "Windows"
        return platform.system()
    
    @staticmethod
    def get_platform_emoji():
        """Get platform-specific emoji"""
        info = PlatformDetector.get_info()
        if info['is_kali']:
            return "🐉"
        if info['is_termux']:
            return "📱"
        if info['is_wsl']:
            return "🪟🐧"
        if info['is_macos']:
            return "🍎"
        if info['is_windows']:
            return "🪟"
        return "🐧"
    
    @staticmethod
    def check_tool_available(tool_name):
        """Check if an external tool/binary is available on PATH"""
        return shutil.which(tool_name) is not None
    
    @staticmethod
    def get_available_tools():
        """Return dict of common pentest tools and their availability"""
        tools = [
            'nmap', 'masscan', 'nikto', 'sqlmap', 'hydra', 'john',
            'hashcat', 'aircrack-ng', 'metasploit', 'msfconsole',
            'gobuster', 'dirb', 'wfuzz', 'ffuf', 'nuclei',
            'subfinder', 'amass', 'theHarvester', 'recon-ng',
            'wireshark', 'tshark', 'tcpdump', 'netcat', 'nc',
            'curl', 'wget', 'git', 'docker', 'kubectl',
        ]
        return {t: PlatformDetector.check_tool_available(t) for t in tools}


class PlatformOptimizer:
    """Optimize resource usage based on platform capabilities"""
    
    @staticmethod
    def get_optimal_threads():
        """Calculate optimal thread count based on CPU cores and platform"""
        try:
            cores = multiprocessing.cpu_count()
            info = PlatformDetector.get_info()
            
            if info['is_termux']:
                return min(cores, 4)  # Termux: conservative
            elif info['is_wsl']:
                return min(cores * 2, 30)  # WSL: moderate
            else:
                return min(cores * 2, 50)  # Full OS: standard
        except Exception:
            return 10  # Safe default
    
    @staticmethod
    def get_data_dir():
        """Get the appropriate data directory per platform"""
        info = PlatformDetector.get_info()
        
        if info['is_termux']:
            base = os.path.expanduser('~/.aleopantest')
        elif info['is_windows']:
            base = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'aleopantest')
        elif info['is_macos']:
            base = os.path.expanduser('~/Library/Application Support/aleopantest')
        else:
            base = os.path.expanduser('~/.local/share/aleopantest')
        
        os.makedirs(base, exist_ok=True)
        return base
    
    @staticmethod
    def get_output_dir():
        """Get the appropriate output/results directory"""
        data_dir = PlatformOptimizer.get_data_dir()
        output_dir = os.path.join(data_dir, 'results')
        os.makedirs(output_dir, exist_ok=True)
        return output_dir


class EnvironmentAdapter:
    """Adapt behavior based on deployment environment"""
    
    @staticmethod
    def get_env():
        """Detect current execution environment"""
        env = os.environ.get("ALEO_ENV")
        if env:
            return env.lower()
        
        if os.environ.get("KUBERNETES_SERVICE_HOST"):
            return "prod"
        if os.environ.get("CI"):
            return "ci"
        if os.path.exists(".git"):
            return "local"
        
        return "local"  # Default
    
    @staticmethod
    def is_root():
        """Check if running as root/admin"""
        if os.name == 'nt':
            try:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except Exception:
                return False
        else:
            return os.geteuid() == 0 if hasattr(os, 'geteuid') else False
