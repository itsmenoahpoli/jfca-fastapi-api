from src.config.settings import app_settings

def get_image_url(path: str) -> str:
    return f"{app_settings.app_url}/public/assets/images/{path}" 