from atlas.providers.ollama import OllamaModelClient


def test_ollama_client_defaults():

    client = OllamaModelClient()

    assert client is not None