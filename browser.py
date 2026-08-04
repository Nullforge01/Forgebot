"""
ForgeBot 🔨 - Browser Manager
Handles browser setup with anti-detection features
"""

import random
from typing import Optional
from playwright.async_api import async_playwright, Browser, Page, Playwright


class BrowserManager:
    """Manage browser instance with anti-detection"""
    
    def __init__(self, config):
        """Initialize browser manager"""
        self.config = config
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
    
    async def setup(self) -> Page:
        """Launch browser with anti-detection settings"""
        
        self.playwright = await async_playwright().start()
        
        # Browser launch arguments for anti-detection
        launch_args = [
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-gpu',
        ]
        
        # Add proxy if configured
        if self.config.proxy:
            launch_args.append(f'--proxy-server={self.config.proxy}')
        
        # Launch browser
        self.browser = await self.playwright.chromium.launch(
            headless=self.config.headless,
            args=launch_args,
        )
        
        # Create context with realistic settings
        context = await self.browser.new_context(
            viewport={
                'width': random.randint(1200, 1920),
                'height': random.randint(800, 1080)
            },
            user_agent=self._random_user_agent(),
            locale='en-US',
            timezone_id='America/New_York',
            permissions=['geolocation'],
        )
        
        self.page = await context.new_page()
        
        # Anti-detection: Hide automation fingerprint
        await self.page.add_init_script("""
            // Remove webdriver property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // Add plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // Set languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            
            // Override chrome property
            window.chrome = {
                runtime: {}
            };
        """)
        
        return self.page
    
    def _random_user_agent(self) -> str:
        """Return a random user agent to avoid detection"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36',
        ]
        return random.choice(user_agents)
    
    async def random_scroll(self):
        """Scroll like a human"""
        if not self.page:
            return
        
        scroll_amount = random.randint(100, 500)
        await self.page.evaluate(f"window.scrollBy(0, {scroll_amount})")
        await self.page.wait_for_timeout(random.randint(200, 800))
    
    async def random_mouse_move(self):
        """Move mouse randomly (stealth)"""
        if not self.page:
            return
        
        x = random.randint(100, 800)
        y = random.randint(100, 600)
        await self.page.mouse.move(x, y)
        await self.page.wait_for_timeout(random.randint(100, 400))
    
    async def cleanup(self):
        """Close browser and cleanup"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
