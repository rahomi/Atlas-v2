from atlas.config import Settings


def test_default_provider():
    settings = Settings()
    assert settings.atlas_provider in {
        "ollama",
        "openai",
    }