#!/usr/bin/env python3
"""
ForgeBot 🔨 - Main Entry Point
Run with: python -m bot.main
"""

import sys
import asyncio
from pathlib import Path

# Add parent directory to path if running directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.config import Config
from bot.browser import BrowserManager
from bot.tiktok import TikTokBot
from bot.instagram import InstagramBot
from bot.utils import logger, setup_logging


async def main():
    """Main entry point for ForgeBot"""
    
    # Setup logging
    setup_logging()
    
    try:
        # Load configuration
        config = Config()
        logger.info("🔥 ForgeBot starting...")
        logger.info(f"📱 Platform: {config.platform}")
        logger.info(f"🎯 Target: @{config.target}")
        logger.info(f"📊 Daily views: {config.daily_views}")
        logger.info("=" * 50)
        
        # Setup browser
        browser_manager = BrowserManager(config)
        await browser_manager.setup()
        logger.info("🌐 Browser ready")
        
        # Create platform-specific bot
        if config.platform == 'tiktok':
            bot = TikTokBot(config, browser_manager)
        elif config.platform == 'instagram':
            bot = InstagramBot(config, browser_manager)
        else:
            logger.error(f"❌ Unsupported platform: {config.platform}")
            return
        
        # Run the bot
        await bot.run()
        
        # Done!
        logger.info("=" * 50)
        logger.info(f"✅ ForgeBot completed!")
        logger.info(f"📊 Total views given: {bot.views_given}")
        logger.info("=" * 50)
        
    except KeyboardInterrupt:
        logger.info("🛑 ForgeBot stopped by user")
    except Exception as e:
        logger.error(f"❌ ForgeBot error: {e}")
    finally:
        await browser_manager.cleanup()
        logger.info("🧹 Cleanup complete")


if __name__ == "__main__":
    asyncio.run(main())
