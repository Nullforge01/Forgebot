"""
ForgeBot 🔨 - TikTok Bot
TikTok-specific logic for watching videos
"""

import random
import asyncio
from bot.utils import logger, human_delay, random_sleep


class TikTokBot:
    """TikTok bot implementation"""
    
    def __init__(self, config, browser_manager):
        """Initialize TikTok bot"""
        self.config = config
        self.browser = browser_manager
        self.page = browser_manager.page
        self.views_given = 0
    
    async def login(self) -> bool:
        """Login to TikTok"""
        try:
            logger.info("🔐 Logging into TikTok...")
            
            # Go to login page
            await self.page.goto('https://www.tiktok.com/login', wait_until='networkidle')
            await random_sleep(2, 4)
            
            # Click email/username login option
            try:
                await self.page.click('text=Use phone / email / username')
                await random_sleep(1, 2)
            except:
                pass
            
            # Fill credentials
            await self.page.fill('input[placeholder="Email or username"]', self.config.username)
            await random_sleep(0.5, 1.5)
            await self.page.fill('input[placeholder="Password"]', self.config.password)
            await random_sleep(0.5, 1.5)
            
            # Click login button
            await self.page.click('button[type="submit"]')
            await random_sleep(3, 5)
            
            # Wait for login to complete (user avatar appears)
            try:
                await self.page.wait_for_selector(
                    'div[data-e2e="user-avatar"]',
                    timeout=10000
                )
                logger.info("✅ TikTok login successful!")
                return True
            except:
                logger.error("❌ TikTok login failed - avatar not found")
                return False
                
        except Exception as e:
            logger.error(f"❌ TikTok login error: {e}")
            return False
    
    async def watch_video(self) -> bool:
        """Watch one TikTok video from target profile"""
        try:
            # Go to target profile
            await self.page.goto(
                f'https://www.tiktok.com/@{self.config.target}',
                wait_until='networkidle'
            )
            await random_sleep(1.5, 3)
            
            # Click on first video
            try:
                video = await self.page.wait_for_selector(
                    'div[data-e2e="user-post-item"]',
                    timeout=5000
                )
                await video.click()
                await random_sleep(1, 2)
            except:
                logger.warning("No video found on profile")
                return False
            
            # Watch video (5-30 seconds)
            watch_time = random.uniform(5, 30)
            logger.info(f"📺 Watching TikTok video for {watch_time:.1f}s...")
            await asyncio.sleep(watch_time)
            
            # Random scroll during video
            if random.random() < self.config.scroll_chance:
                await self.browser.random_scroll()
            
            # Random like (optional)
            if random.random() < self.config.like_chance:
                try:
                    await self.page.click('button[data-e2e="like-icon"]')
                    logger.info("❤️ Liked video!")
                except:
                    pass
            
            # Close video
            try:
                await self.page.keyboard.press('Escape')
                await asyncio.sleep(0.5)
            except:
                pass
            
            # Update view count
            self.views_given += 1
            logger.info(f"✅ View #{self.views_given}/{self.config.daily_views}")
            return True
            
        except Exception as e:
            logger.error(f"❌ TikTok watch error: {e}")
            return False
    
    async def run(self):
        """Main TikTok bot loop"""
        
        # Login first
        if not await self.login():
            logger.error("❌ Login failed. Exiting.")
            return
        
        logger.info(f"🎯 Starting TikTok views for @{self.config.target}")
        logger.info(f"📊 Target: {self.config.daily_views} views")
        
        # Wait before starting
        await human_delay(self.config.delay_range)
        
        # Main loop: give views
        while self.views_given < self.config.daily_views:
            
            # Watch a video
            success = await self.watch_video()
            
            # If failed, try alternative approach
            if not success:
                logger.warning("Video watch failed, trying profile view...")
                await self.page.goto(f'https://www.tiktok.com/@{self.config.target}')
                await random_sleep(2, 4)
                self.views_given += 1
            
            # Take long break every 10 views
            if self.views_given % self.config.views_per_session == 0 and self.views_given > 0:
                long_break = random.randint(300, 600)  # 5-10 minutes
                logger.info(f"☕ Long break: {long_break//60} minutes...")
                await asyncio.sleep(long_break)
            else:
                # Normal human delay
                await human_delay(self.config.delay_range)
            
            # Random behavior to look human
            if random.random() < 0.2:
                await self.browser.random_scroll()
            if random.random() < 0.1:
                await self.browser.random_mouse_move()
        
        logger.info(f"🎉 TikTok bot completed! {self.views_given} views given")
