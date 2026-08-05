"""
ForgeBot 🔨 - Configuration Loader
Loads settings from config.json
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any, Tuple


class Config:
    """Load and manage configuration for ForgeBot"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize config loader"""
        
        if config_path is None:
            # Look for config.json in parent directory (two levels up from this file)
            self.config_path = Path(__file__).parent.parent.parent / "config.json"
        else:
            self.config_path = Path(config_path)
        
        self.data = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"❌ Config file not found: {self.config_path}\n"
                f"Please create config.json (see README for example)"
            )
        
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    # ===== Platform Settings =====
    
    @property
    def platform(self) -> str:
        """Platform: 'tiktok' or 'instagram'"""
        return self.data.get('platform', 'instagram')
    
    # ===== Bot Account =====
    
    @property
    def username(self) -> str:
        """Bot account username"""
        return self.data.get('bot_account', {}).get('username', '')
    
    @property
    def password(self) -> str:
        """Bot account password"""
        return self.data.get('bot_account', {}).get('password', '')
    
    # ===== Target =====
    
    @property
    def target(self) -> str:
        """Target username to boost"""
        return self.data.get('target', '')
    
    # ===== View Settings =====
    
    @property
    def daily_views(self) -> int:
        """Total views to give per day"""
        return self.data.get('daily_views', 100)
    
    @property
    def views_per_session(self) -> int:
        """Views before taking a long break"""
        return self.data.get('views_per_session', 10)
    
    @property
    def delay_range(self) -> Tuple[int, int]:
        """Min and max delay between views (seconds)"""
        delays = self.data.get('delay_range', [60, 300])
        return (delays[0], delays[1])
    
    # ===== Browser Settings =====
    
    @property
    def proxy(self) -> Optional[str]:
        """Proxy server (null = no proxy)"""
        return self.data.get('proxy', None)
    
    @property
    def headless(self) -> bool:
        """Run browser in headless mode (no GUI)"""
        return self.data.get('headless', False)
    
    # ===== Interaction Settings =====
    
    @property
    def like_chance(self) -> float:
        """Probability of liking content (0.0 - 1.0)"""
        return self.data.get('like_chance', 0.3)
    
    @property
    def scroll_chance(self) -> float:
        """Probability of scrolling (0.0 - 1.0)"""
        return self.data.get('scroll_chance', 0.2)
    
    # ===== Helper Methods =====
    
    def get(self, key: str, default=None):
        """Get any config value by key"""
        return self.data.get(key, default)
    
    def validate(self) -> bool:
        """Validate required config values"""
        errors = []
        
        if not self.platform:
            errors.append("'platform' is required (tiktok/instagram)")
        
        if not self.username:
            errors.append("'bot_account.username' is required")
        
        if not self.password:
            errors.append("'bot_account.password' is required")
        
        if not self.target:
            errors.append("'target' is required")
        
        if self.daily_views < 1:
            errors.append("'daily_views' must be at least 1")
        
        if errors:
            for error in errors:
                print(f"❌ Config error: {error}")
            return False
        
        return True
    
    def __repr__(self) -> str:
        return f"Config(platform={self.platform}, target={self.target}, views={self.daily_views})"
