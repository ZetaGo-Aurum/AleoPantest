"""Platform detection and resource optimization for Aleopantest V3.0.0"""
import platform
import os
import multiprocessing

class PlatformDetector:
    """Detect operating system and specific environments like WSL or Termux"""
    
    @staticmethod
    def get_info():
        """Get detailed platform information"""
        system = platform.system().lower()
        is_wsl = False
        is_termux = 'TERMUX_VERSION' in os.environ
        
        if system == 'linux':
            try:
                with open('/proc/version', 'r') as f:
                    if 'microsoft' in f.read().lower():
                        is_wsl = True
            except:
                pass
                
        return {
            'system': system,
            'is_wsl': is_wsl,
            'is_termux': is_termux,
            'release': platform.release(),
            'machine': platform.machine()
        }
        
    @staticmethod
    def get_platform_name():
        """Get a human-readable platform name"""
        info = PlatformDetector.get_info()
        if info['is_wsl']:
            return "Windows Subsystem for Linux (WSL)"
        if info['is_termux']:
            return "Termux (Android)"
        return platform.system()

class PlatformOptimizer:
    """Optimize resource usage based on platform capabilities"""
    
    @staticmethod
    def get_optimal_threads():
        """Calculate optimal thread count based on CPU cores"""
        try:
            cores = multiprocessing.cpu_count()
            # Standard optimization: 2 threads per core, max 50 for safety
            return min(cores * 2, 50)
        except:
            return 10 # Safe default

class EnvironmentAdapter:
    """Adapt behavior based on deployment environment"""
    
    @staticmethod
    def get_env():
        """Detect current execution environment"""
        # Priority: Environment variable > Heuristics
        env = os.environ.get("ALEO_ENV")
        if env:
            return env.lower()
            
        # Heuristics
        if os.path.exists(".git"):
            return "local"
        if os.environ.get("KUBERNETES_SERVICE_HOST"):
            return "prod"
            
        return "local" # Default
