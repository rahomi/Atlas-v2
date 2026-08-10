import pytest
from atlas.runtime.agent import Agent
from atlas.providers.ollama import OllamaModelClient
from atlas.tools.calculator import CalculatorTool

@pytest.mark.asyncio
async def test_atlas_v2_public_api():
    # Arrange
    agent = Agent(
        model=OllamaModelClient(model="qwen3:latest"),
        tools=[CalculatorTool()],
        system_prompt=(
            "You are a tool-calling assistant. "
            "Do not think or explain. Immediately call the calculator tool for math."
        )
    )
    
    # Act
    result = await agent.run("Use the calculator tool to multiply 1234567 by 89123.")
    
    # Assert
    print("\n=== Agent Final Result ===")
    print(result)
    print("==========================\n")
    
    assert result is not None
    assert "110028314741" in result