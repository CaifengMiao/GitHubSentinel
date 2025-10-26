# langchain-ai/langchain - Progress (2025-10-19 ~ 2025-10-26)

范围：最近 7 天（更新时间在 2025-10-19 后）

## Issues（最近更新）

- **#33674** refactor(core): Minor refactor for code readability
  - State: open
  - Created: 2025-10-26T02:01:42Z
  - Updated: 2025-10-26T02:04:37Z

- **#33673** refactor(core): Improve performance and code simplicity
  - State: open
  - Created: 2025-10-26T00:58:37Z
  - Updated: 2025-10-26T01:01:23Z

- **#33672** langchain-openai 无法读取到 qwen3 think 的过程 希望 支持 qwen3 像 支持 deepseek一样（initChatModel）
  - State: open
  - Created: 2025-10-26T00:01:51Z
  - Updated: 2025-10-26T00:01:51Z

- **#33671** refactor(anthropic): Code readability and simplicity
  - State: open
  - Created: 2025-10-25T23:51:47Z
  - Updated: 2025-10-26T01:00:14Z

- **#33670** feat(perplexity): Created Dedicated Output Parser to Support Reasoning Model Output for perplexity
  - State: open
  - Created: 2025-10-25T23:49:57Z
  - Updated: 2025-10-26T00:04:22Z

- **#33668** fix(openai): Respect 300k token limit for embeddings API requests
  - State: open
  - Created: 2025-10-25T12:38:27Z
  - Updated: 2025-10-25T12:38:43Z

- **#33666** feat: Add Serpex partner package for web search
  - State: open
  - Created: 2025-10-25T03:38:09Z
  - Updated: 2025-10-25T05:33:48Z

- **#33663** feat: support structured output retry middleware
  - State: open
  - Created: 2025-10-24T16:22:11Z
  - Updated: 2025-10-24T17:57:10Z

- **#33662** fix(openai): Improve vLLM API compatibility and error messages
  - State: open
  - Created: 2025-10-24T15:13:18Z
  - Updated: 2025-10-24T15:20:30Z

- **#33656** `summarizationMiddleware` leads message order unsupported by Gemini
  - State: open
  - Created: 2025-10-24T13:07:12Z
  - Updated: 2025-10-24T13:17:32Z

- **#33654** fix: Add video support to convert_to_openai_data_block function
  - State: open
  - Created: 2025-10-24T02:48:51Z
  - Updated: 2025-10-24T03:11:07Z

- **#33653** [LangChain v1] Built-in Middleware for Recursion limit fallback
  - State: open
  - Created: 2025-10-24T01:52:37Z
  - Updated: 2025-10-25T09:08:59Z

- **#33652** [LangChain-Core v1]Did the openai:convert_to-openai_data-block function miss the processing of video? And other providers' converters also do not handle videos
  - State: open
  - Created: 2025-10-24T01:46:52Z
  - Updated: 2025-10-24T02:50:39Z

- **#33651** [LangChain v1] LLMToolSelectorMiddleware selects a tool that is not in the provided tool list. seems like the middleware is not receiving the correct tool list.
  - State: open
  - Created: 2025-10-24T00:39:14Z
  - Updated: 2025-10-25T12:43:08Z

- **#33649** fix(core): preserve injected arguments when args_schema is BaseModel
  - State: open
  - Created: 2025-10-23T19:11:49Z
  - Updated: 2025-10-23T19:14:33Z

- **#33646** runtime is not passed to tool function if the args_schema is defined with Pydantic BaseModel
  - State: open
  - Created: 2025-10-23T06:17:22Z
  - Updated: 2025-10-23T19:17:01Z

- **#33645** docs: add Notion Write Toolkit integration
  - State: open
  - Created: 2025-10-23T00:00:53Z
  - Updated: 2025-10-23T00:59:07Z

- **#33643** OpenRouter and LiteLLM integrations with LangChain v1
  - State: open
  - Created: 2025-10-22T22:30:22Z
  - Updated: 2025-10-22T22:30:22Z

- **#33642** Add support for CockroachDB Vector Data and Indexing
  - State: open
  - Created: 2025-10-22T22:11:37Z
  - Updated: 2025-10-22T22:11:52Z

- **#33641** feat(langchain_v1): add end_tools exit behavior to ToolCallLimitMiddleware
  - State: open
  - Created: 2025-10-22T20:41:47Z
  - Updated: 2025-10-22T21:05:00Z

- **#33640** chore(langchain_v1): Updated Signature for create_agent for system prompt
  - State: open
  - Created: 2025-10-22T19:50:38Z
  - Updated: 2025-10-25T11:17:55Z

- **#33635** [LangGraph v1.0] Support Bedrock Anthropic prompt caching (cache_control) in create_agent system prompt
  - State: open
  - Created: 2025-10-22T14:52:15Z
  - Updated: 2025-10-23T09:48:31Z

- **#33634** chore: move `ToolNode` improvements back to langgraph
  - State: open
  - Created: 2025-10-22T13:24:16Z
  - Updated: 2025-10-22T14:55:07Z

- **#33632** langchain-azure-dynamic-sessions is incompatible with other langchain V1 packages
  - State: open
  - Created: 2025-10-22T08:34:33Z
  - Updated: 2025-10-23T07:33:25Z

- **#33631** fix(core): implement ChatPromptTemplate.save() method (#32637)
  - State: open
  - Created: 2025-10-21T21:38:49Z
  - Updated: 2025-10-21T22:11:36Z

- **#33630** create_agent() system_prompt not supporting array needed for anthropic api
  - State: open
  - Created: 2025-10-21T21:26:11Z
  - Updated: 2025-10-24T14:49:06Z

- **#33622** Dependency Conflict: langgraph_supervisor incompatible with langgraph>=1.0.0
  - State: open
  - Created: 2025-10-21T07:17:49Z
  - Updated: 2025-10-22T01:44:23Z

- **#33617** fix(core): fix callback manager merge mixing handlers (#32028)
  - State: open
  - Created: 2025-10-20T23:15:16Z
  - Updated: 2025-10-21T00:16:55Z

- **#33597** langchain 1.0.0: add tool_call_id to on_tool_error event's data
  - State: open
  - Created: 2025-10-19T07:45:09Z
  - Updated: 2025-10-21T01:25:02Z

- **#33592** Access enable_thinking flag for langchain_huggingface models
  - State: open
  - Created: 2025-10-17T22:44:31Z
  - Updated: 2025-10-23T07:26:05Z

## Pull Requests（最近更新）

- **#33674** refactor(core): Minor refactor for code readability
  - State: open
  - Created: 2025-10-26T02:01:42Z
  - Updated: 2025-10-26T02:04:37Z

- **#33673** refactor(core): Improve performance and code simplicity
  - State: open
  - Created: 2025-10-26T00:58:37Z
  - Updated: 2025-10-26T01:01:23Z

- **#33671** refactor(anthropic): Code readability and simplicity
  - State: open
  - Created: 2025-10-25T23:51:47Z
  - Updated: 2025-10-26T01:00:14Z

- **#33670** feat(perplexity): Created Dedicated Output Parser to Support Reasoning Model Output for perplexity
  - State: open
  - Created: 2025-10-25T23:49:57Z
  - Updated: 2025-10-26T00:04:22Z

- **#33668** fix(openai): Respect 300k token limit for embeddings API requests
  - State: open
  - Created: 2025-10-25T12:38:27Z
  - Updated: 2025-10-25T12:38:43Z

- **#33666** feat: Add Serpex partner package for web search
  - State: open
  - Created: 2025-10-25T03:38:09Z
  - Updated: 2025-10-25T05:33:48Z

- **#33663** feat: support structured output retry middleware
  - State: open
  - Created: 2025-10-24T16:22:11Z
  - Updated: 2025-10-24T17:57:10Z

- **#33662** fix(openai): Improve vLLM API compatibility and error messages
  - State: open
  - Created: 2025-10-24T15:13:18Z
  - Updated: 2025-10-24T15:20:30Z

- **#33654** fix: Add video support to convert_to_openai_data_block function
  - State: open
  - Created: 2025-10-24T02:48:51Z
  - Updated: 2025-10-24T03:11:07Z

- **#33649** fix(core): preserve injected arguments when args_schema is BaseModel
  - State: open
  - Created: 2025-10-23T19:11:49Z
  - Updated: 2025-10-23T19:14:33Z

- **#33645** docs: add Notion Write Toolkit integration
  - State: open
  - Created: 2025-10-23T00:00:53Z
  - Updated: 2025-10-23T00:59:07Z

- **#33641** feat(langchain_v1): add end_tools exit behavior to ToolCallLimitMiddleware
  - State: open
  - Created: 2025-10-22T20:41:47Z
  - Updated: 2025-10-22T21:05:00Z

- **#33640** chore(langchain_v1): Updated Signature for create_agent for system prompt
  - State: open
  - Created: 2025-10-22T19:50:38Z
  - Updated: 2025-10-25T11:17:55Z

- **#33634** chore: move `ToolNode` improvements back to langgraph
  - State: open
  - Created: 2025-10-22T13:24:16Z
  - Updated: 2025-10-22T14:55:07Z

- **#33631** fix(core): implement ChatPromptTemplate.save() method (#32637)
  - State: open
  - Created: 2025-10-21T21:38:49Z
  - Updated: 2025-10-21T22:11:36Z

- **#33617** fix(core): fix callback manager merge mixing handlers (#32028)
  - State: open
  - Created: 2025-10-20T23:15:16Z
  - Updated: 2025-10-21T00:16:55Z

- **#33479** fix(core): Fix tool name check in name_dict for PydanticToolsParser
  - State: open
  - Created: 2025-10-14T16:10:19Z
  - Updated: 2025-10-25T11:20:40Z

- **#33450** fix(openai): "No call message found" bug with gpt-oss-120b when using responses API
  - State: open
  - Created: 2025-10-12T12:16:53Z
  - Updated: 2025-10-22T02:25:14Z

- **#33332** Fix config propagation in AgentExecutor
  - State: open
  - Created: 2025-10-07T10:29:36Z
  - Updated: 2025-10-23T12:28:34Z

- **#33291** fix(core): replace lambda functions to enable serialization (#33128)
  - State: open
  - Created: 2025-10-06T07:37:23Z
  - Updated: 2025-10-21T17:07:00Z

