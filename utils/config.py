import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    base_url: str = field(default_factory=lambda: os.getenv("BASE_URL", "https://the-internet.herokuapp.com"))
    headless: bool = field(default_factory=lambda: os.getenv("HEADLESS", "true").lower() == "true")
    browser_type: str = field(default_factory=lambda: os.getenv("BROWSER", "chromium"))
    timeout: int = field(default_factory=lambda: int(os.getenv("TIMEOUT", "30000")))