from typing import Any

from atlas.models import ToolCall
from atlas.runtime.tool_result import ToolResult
from atlas.tools.schemas import CalculatorArguments


class CalculatorTool:

    @property
    def name(self) -> str:
        return "calculator"

    async def execute(
        self,
        tool_call: ToolCall,
    ) -> ToolResult:

        try:
            args = CalculatorArguments.model_validate(
                tool_call.arguments
            )

        except Exception as exc:
            return ToolResult.fail(
                str(exc),
                tool_call_id=tool_call.id,
            )

        result = args.a * args.b

        return ToolResult.ok(
            str(result),
            tool_call_id=tool_call.id,
        )
    
    @property
    def definition(self) -> dict[str, Any]:
        return {
            "name": "calculator",
            "description": "Multiply two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The first number.",
                    },
                    "b": {
                        "type": "number",
                        "description": "The second number.",
                    },
                },
                "required": ["a", "b"],
            },
        }