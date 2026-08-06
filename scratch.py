"""Temporary scratch script to verify Settings loads correctly."""

from atlas.config import Settings

settings = Settings()

print(settings)
print(settings.atlas_provider)
print(settings.ollama_model)
