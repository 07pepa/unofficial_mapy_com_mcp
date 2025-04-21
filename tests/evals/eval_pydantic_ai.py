from __future__ import annotations

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import IsInstance, LLMJudge

test_ds = Dataset(
    cases=[
        Case(
            name='viena',
            inputs='Jak dlouho pojedu do Vídně z Brna autem za soucasneho provozu?',
            evaluators=[IsInstance(type_name='str')],
        ),
    ],
    evaluators=[
        IsInstance(type_name='str'),
        LLMJudge(rubric='response should be in Czech and include the time of the route'),
    ],
)

if __name__ == '__main__':
    server = MCPServerHTTP(url='http://localhost:8000/sse')
    agent = Agent('openai:gpt-4.1', mcp_servers=[server])

    async def get_directions(question: str) -> str:
        async with agent.run_mcp_servers():
            result = await agent.run(question)
            return result.output

    report = test_ds.evaluate_sync(get_directions)
    report.print(include_input=True, include_output=True, include_durations=False)
