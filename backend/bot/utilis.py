"""
ForgeBot 🔨 - Utilities
Helper functions for logging, delays, and random behavior
"""

import random
import asyncio
import logging
from pathlib import Path
from datetime import datetime


# ============ LOGGING SETUP ============

def setup_logging():
    """Setup logging configuration"""
    
    # Create logs directory
    LOG_DIR = Path("logs")
    LOG_DIR.mkdir(exist_ok=True)
    
    # Create log file with date
    log_file = LOG_DIR / f"forgebot_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


# ============ LOGGER ============

logger = setup_logging()


# ============ DELAY FUNCTIONS ============

async def human_delay(delay_range):
    """
    Wait like a human with random delay
    
    Args:
        delay_range: Tuple of (min_seconds, max_seconds)
    """
    min_delay, max_delay = delay_range
    delay = random.randint(min_delay, max_delay)
    
    # Add some variation
    if random.random() < 0.1:
        delay = delay * 2
    
    logger.info(f"⏳ Waiting {delay} seconds...")
    await asyncio.sleep(delay)


async def random_sleep(min_seconds: float, max_seconds: float):
    """
    Short random sleep for micro-interactions
    
    Args:
        min_seconds: Minimum seconds
        max_seconds: Maximum seconds
    """
    delay = random.uniform(min_seconds, max_seconds)
    await asyncio.sleep(delay)


# ============ RANDOM HELPERS ============

def random_user_agent() -> str:
    """Return random user agent"""
    agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/17.1',
    ]
    return random.choice(agents)


def random_viewport() -> tuple:
    """Return random viewport size"""
    widths = [1280, 1366, 1440, 1536, 1600, 1920]
    heights = [720, 768, 800, 900, 1024, 1080]
    return (random.choice(widths), random.choice(heights))


# ============ PROGRESS FORMATTING ============

def progress_bar(current: int, total: int, width: int = 30) -> str:
    """Create a progress bar string"""
    progress = current / total
    filled = int(width * progress)
    bar = '█' * filled + '░' * (width - filled)
    return f"[{bar}] {current}/{total} ({progress*100:.1f}%)"


def format_time(seconds: int) -> str:
    """Format seconds into readable time"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"
