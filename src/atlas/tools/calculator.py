from atlas.runtime.tool_result import ToolResult
from atlas.tools.schemas import CalculatorArguments


class CalculatorTool:

    @property
    def name(self) -> str:
        return "calculator"

    async def execute(
        self,
        arguments: dict,
    ) -> ToolResult:

        try:
            args = CalculatorArguments.model_validate(
                arguments
            )

        except Exception as exc:
            return ToolResult.fail(
                f"Invalid arguments: {exc}"
            )

        result = args.a * args.b

        return ToolResult.ok(
            str(result)
        )