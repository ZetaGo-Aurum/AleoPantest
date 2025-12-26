"""Session and security management for AloPantest V3.0"""
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from .logger import logger

class SessionManager:
    """Manage user sessions and enforce security limits"""
    
    # 10-minute session quota (600 seconds)
    SESSION_QUOTA_SECONDS = 600
    
    def __init__(self):
        self.start_time: float = time.time()
        self.session_id: str = datetime.now().strftime("%Y%m%d%H%M%S")
        self.is_active: bool = True
        
    def get_elapsed_time(self) -> float:
        """Get elapsed session time in seconds"""
        return time.time() - self.start_time
    
    def get_remaining_time(self) -> float:
        """Get remaining session time in seconds"""
        remaining = self.SESSION_QUOTA_SECONDS - self.get_elapsed_time()
        return max(0, remaining)
    
    def check_quota(self) -> bool:
        """Check if session is still within quota"""
        if self.get_elapsed_time() > self.SESSION_QUOTA_SECONDS:
            self.is_active = False
            return False
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """Get current session status"""
        elapsed = self.get_elapsed_time()
        remaining = self.get_remaining_time()
        
        return {
            "session_id": self.session_id,
            "elapsed_formatted": str(timedelta(seconds=int(elapsed))),
            "remaining_formatted": str(timedelta(seconds=int(remaining))),
            "is_active": self.is_active and remaining > 0,
            "quota_reached": remaining <= 0
        }

class SecurityGuard:
    """Enforce safety limits and anti-DDoS protections"""
    
    @staticmethod
    def enforce_limits(tool_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Apply safety limits to tool parameters"""
        sanitized = params.copy()
        
        # Enhanced Anti-DDoS safety limits
        if tool_id == 'ddos-sim':
            # Cap duration to 60 seconds max per attack
            if 'duration' in sanitized:
                sanitized['duration'] = min(int(sanitized['duration']), 60)
            else:
                sanitized['duration'] = 30 # Default safe duration
                
            # Cap threads to prevent local resource exhaustion
            from .platform import PlatformOptimizer
            max_threads = PlatformOptimizer.get_optimal_threads()
            if 'threads' in sanitized:
                sanitized['threads'] = min(int(sanitized['threads']), max_threads)
            else:
                sanitized['threads'] = min(max_threads, 10)
                
            # Ensure authorization is present
            if not sanitized.get('authorized'):
                logger.warning(f"Unauthorized DDoS simulation attempted for {sanitized.get('target')}")
                # We don't block here, but the tool should check this flag
        
        # General limits for other tools
        if 'threads' in sanitized:
            from .platform import PlatformOptimizer
            max_threads = PlatformOptimizer.get_optimal_threads() * 2
            sanitized['threads'] = min(int(sanitized['threads']), max_threads)
            
        return sanitized
