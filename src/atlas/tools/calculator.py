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