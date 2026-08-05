"""
ForgeBot 🔨 - Instagram Bot
Instagram-specific logic for watching stories and reels
"""

import random
import asyncio
from bot.utils import logger, human_delay, random_sleep


class InstagramBot:
    """Instagram bot implementation"""
    
    def __init__(self, config, browser_manager):
        """Initialize Instagram bot"""
        self.config = config
        self.browser = browser_manager
        self.page = browser_manager.page
        self.views_given = 0
    
    async def login(self) -> bool:
        """Login to Instagram"""
        try:
            logger.info("🔐 Logging into Instagram...")
            
            # Go to login page
            await self.page.goto(
                'https://www.instagram.com/accounts/login/',
                wait_until='networkidle'
            )
            await random_sleep(2, 4)
            
            # Fill credentials
            await self.page.fill('input[name="username"]', self.config.username)
            await random_sleep(0.5, 1.5)
            await self.page.fill('input[name="password"]', self.config.password)
            await random_sleep(0.5, 1.5)
            
            # Click login
            await self.page.click('button[type="submit"]')
            await random_sleep(3, 5)
            
            # Handle "Save Info" popup
            try:
                await self.page.wait_for_selector(
                    'button:has-text("Not Now")',
                    timeout=5000
                )
                await self.page.click('button:has-text("Not Now")')
                await random_sleep(1, 2)
            except:
                pass
            
            # Handle "Turn On Notifications" popup
            try:
                await self.page.wait_for_selector(
                    'button:has-text("Not Now")',
                    timeout=3000
                )
                await self.page.click('button:has-text("Not Now")')
                await random_sleep(1, 2)
            except:
                pass
            
            # Wait for home page
            try:
                await self.page.wait_for_selector(
                    'svg[aria-label="Home"]',
                    timeout=10000
                )
                logger.info("✅ Instagram login successful!")
                return True
            except:
                logger.error("❌ Instagram login failed - home page not loaded")
                return False
                
        except Exception as e:
            logger.error(f"❌ Instagram login error: {e}")
            return False
    
    async def watch_story(self) -> bool:
        """Watch one Instagram story from target"""
        try:
            # Go to target profile
            await self.page.goto(
                f'https://www.instagram.com/{self.config.target}/',
                wait_until='networkidle'
            )
            await random_sleep(1.5, 3)
            
            # Check if story exists
            try:
                await self.page.wait_for_selector(
                    'div[role="button"] svg[aria-label="Story"]',
                    timeout=5000
                )
            except:
                logger.warning("No story available for this profile")
                return False
            
            # Click on story
            await self.page.click('div[role="button"] svg[aria-label="Story"]')
            await random_sleep(1, 2)
            
            # Watch story (5-15 seconds per slide)
            slides = random.randint(1, 3)
            for i in range(slides):
                watch_time = random.uniform(5, 15)
                logger.info(f"📖 Watching story slide {i+1} for {watch_time:.1f}s...")
                await asyncio.sleep(watch_time)
                
                if i < slides - 1:
                    try:
                        await self.page.click('div[role="button"]')
                        await random_sleep(0.5, 1)
                    except:
                        pass
            
            # Close story
            try:
                await self.page.click('button[aria-label="Close"]')
                await random_sleep(0.5, 1)
            except:
                await self.page.keyboard.press('Escape')
            
            self.views_given += 1
            logger.info(f"✅ View #{self.views_given}/{self.config.daily_views}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Instagram story error: {e}")
            return False
    
    async def watch_reel(self) -> bool:
        """Watch one Instagram Reel from target"""
        try:
            # Go to target profile
            await self.page.goto(
                f'https://www.instagram.com/{self.config.target}/',
                wait_until='networkidle'
            )
            await random_sleep(1.5, 3)
            
            # Find and click a reel
            try:
                reel = await self.page.wait_for_selector(
                    'div[role="link"] a[href*="/reel/"]',
                    timeout=5000
                )
                await reel.click()
                await random_sleep(1, 2)
            except:
                logger.warning("No reel available")
                return False
            
            # Watch reel (10-30 seconds)
            watch_time = random.uniform(10, 30)
            logger.info(f"🎬 Watching Instagram Reel for {watch_time:.1f}s...")
            await asyncio.sleep(watch_time)
            
            # Random like (optional)
            if random.random() < self.config.like_chance:
                try:
                    await self.page.click('svg[aria-label="Like"]')
                    logger.info("❤️ Liked reel!")
                except:
                    pass
            
            # Close reel
            try:
                await self.page.click('button[aria-label="Close"]')
                await random_sleep(0.5, 1)
            except:
                await self.page.keyboard.press('Escape')
            
            self.views_given += 1
            logger.info(f"✅ View #{self.views_given}/{self.config.daily_views}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Instagram reel error: {e}")
            return False
    
    async def run(self):
        """Main Instagram bot loop"""
        
        # Login first
        if not await self.login():
            logger.error("❌ Login failed. Exiting.")
            return
        
        logger.info(f"🎯 Starting Instagram views for @{self.config.target}")
        logger.info(f"📊 Target: {self.config.daily_views} views")
        
        # Wait before starting
        await human_delay(self.config.delay_range)
        
        # Main loop: give views
        while self.views_given < self.config.daily_views:
            
            # Mix stories and reels (70% stories, 30% reels)
            action = random.choices(
                ['story', 'reel'],
                weights=[0.7, 0.3]
            )[0]
            
            if action == 'story':
                success = await self.watch_story()
            else:
                success = await self.watch_reel()
            
            # If story failed, try reel
            if not success:
                logger.warning("Story failed, trying reel...")
                await self.watch_reel()
            
            # Take long break every 10 views
            if self.views_given % self.config.views_per_session == 0 and self.views_given > 0:
                long_break = random.randint(300, 600)
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
        
        logger.info(f"🎉 Instagram bot completed! {self.views_given} views given")
