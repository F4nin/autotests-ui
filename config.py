from typing import Self

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr, FilePath, HttpUrl, DirectoryPath, BaseModel
from enum import Enum

class Browser(str, Enum):
    WEBKIT = "webkit"
    FIREFOX = "firefox"
    CHROMIUM = "chromium"

class TestUser(BaseModel):
    email: EmailStr
    username: str
    password: str

class TestData(BaseModel):
    image_png_file: FilePath

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="."

    )

    app_url: HttpUrl
    headless: bool
    network_logs: bool
    browsers: list[Browser]
    test_user: TestUser
    test_data: TestData
    videos_dir: DirectoryPath
    tracing_dir: DirectoryPath
    allure_results_dir: DirectoryPath
    browser_state_file: FilePath
    record_har_dir: DirectoryPath

    @classmethod
    def initialize(cls) -> Self:
        videos_dir = DirectoryPath("./videos")
        tracing_dir = DirectoryPath("./tracing")
        record_har_dir = DirectoryPath("./network")
        allure_results_dir = DirectoryPath("./allure-results")
        browser_state_file = FilePath("browser_state.json")

        videos_dir.mkdir(exist_ok=True)
        tracing_dir.mkdir(exist_ok=True)
        record_har_dir.mkdir(exist_ok=True)
        browser_state_file.touch(exist_ok=True)
        allure_results_dir.mkdir(exist_ok=True)

        return Settings(
            videos_dir = videos_dir,
            tracing_dir = tracing_dir,
            record_har_dir = record_har_dir,
            browser_state_file = browser_state_file,
            allure_results_dir = allure_results_dir
        )

    def get_base_url(self) -> str:
        return f"{self.app_url}/"

settings = Settings.initialize()
