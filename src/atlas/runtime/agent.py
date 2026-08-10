from __future__ import annotations

from atlas.models import (
    Conversation,
    Message,
    MessageRole,
)
from typing import List, Optional
from atlas.models import Conversation, Message, MessageRole
from atlas.runtime.contracts import ModelClient, Tool
from atlas.runtime.tool_result import ToolResult
from atlas.tools.registry import ToolRegistry


class AgentRuntime:

    def __init__(
        self,
        model: ModelClient,
        tools: ToolRegistry,
        max_iterations: int = 10,
    ):
        if max_iterations < 1:
            raise ValueError(
                "max_iterations must be at least 1"
            )

        self._model = model
        self._tools = tools
        self._max_iterations = max_iterations

    async def run(
        self,
        conversation: Conversation,
    ):
        current = conversation

        for _ in range(self._max_iterations):

            response = await self._model.chat(
                current,
                tools=tuple(
                    self._tools.get(name)
                    for name in self._tools.list()
                ),
            )

            if not response.tool_calls and not response.content:
                current = current.append(
                    Message(
                        role=MessageRole.USER,
                        content="You returned an empty response. Please use the calculator tool to answer the question."
                    )
                )
                continue

            if not response.tool_calls:
                return response

            current = await self._execute_tool_calls(
                current,
                response,
            )

        raise RuntimeError(
            "Agent exceeded maximum iterations"
        )
        
    async def _execute_tool_calls(
        self,
        conversation: Conversation,
        response,
    ) -> Conversation:

        current = conversation

        current = current.append(
            Message(
                role=MessageRole.ASSISTANT,
                content=(
                    response.content
                    or "Tool call requested."
                ),
                tool_calls=response.tool_calls,
            )
        )

        for tool_call in response.tool_calls:

            try:
                tool = self._tools.get(
                    tool_call.tool_name
                )

                print(
                    f"[TOOL CALL] {tool_call.tool_name}"
                    f" arguments={tool_call.arguments}"
                )

                result = await tool.execute(
                    tool_call
                )

                print(
                    f"[TOOL RESULT] {result.output}"
                )

            except KeyError as exc:
                result = ToolResult.fail(
                    error=str(exc),
                    tool_call_id=tool_call.id,
                )

            except Exception as exc:
                result = ToolResult.fail(
                    error=f"Tool error: {exc}",
                    tool_call_id=tool_call.id,
                )

            current = current.append(
                Message(
                    role=MessageRole.TOOL,
                    content=(
                        result.output
                        if result.success
                        else result.error
                        or "Tool execution failed."
                    ),
                    tool_call_id=tool_call.id,
                )
            )

        return current

class Agent:
    """
    The public API for Atlas v0.2.
    """
    def __init__(
        self,
        model: ModelClient,
        tools: Optional[List[Tool]] = None,
        system_prompt: Optional[str] = None,
        max_iterations: int = 10
    ):
        # 1. Setup Tools
        self._tool_registry = ToolRegistry()
        if tools:
            for tool in tools:
                self._tool_registry.register(tool)
        
        # 2. Setup Conversation/Memory
        self._conversation = Conversation()
        if system_prompt:
            self._conversation = self._conversation.append(
                Message(role=MessageRole.SYSTEM, content=system_prompt)
            )
            
        # 3. Setup Runtime
        self._runtime = AgentRuntime(
            model=model,
            tools=self._tool_registry,
            max_iterations=max_iterations
        )

    async def run(self, user_input: str) -> str:
        """
        The main method developers will call.
        """
        # Add user message
        self._conversation = self._conversation.append(
            Message(role=MessageRole.USER, content=user_input)
        )
        
        # Run the agent loop
        final_response = await self._runtime.run(self._conversation)
        
        # Update conversation history with the final assistant response
        if final_response and final_response.content:
            self._conversation = self._conversation.append(
                Message(
                    role=MessageRole.ASSISTANT,
                    content=final_response.content
                )
            )
            
        return final_response.content if final_response else ""