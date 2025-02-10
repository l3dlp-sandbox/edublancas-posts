from smolagents import CodeAgent, OpenAIServerModel


model = OpenAIServerModel(
    model_id="gpt-4o-mini",
    api_base="http://localhost:8080/v1",
)

agent = CodeAgent(tools=[], model=model, add_base_tools=False)


agent.run(
    "Could you give me the 118th number in the Fibonacci sequence?",
)


# agent.run(
#     "How much is 12 + 12 + 18?",
# )


# agent.run(
#     "How much is 2 * 21?",
# )
