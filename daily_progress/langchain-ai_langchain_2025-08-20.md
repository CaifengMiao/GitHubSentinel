# langchain-ai/langchain - Daily Progress (2025-08-20)

## Issues

- **#32605** feat(docs): add composio integration documentation
  - State: open
  - Created: 2025-08-19T12:03:07Z
  - Updated: 2025-08-19T14:35:56Z

- **#32603** feat(core): Thread `RunnableConfig` through `AgentExecutor` and tools without exposing to LLM
  - State: open
  - Created: 2025-08-19T07:20:47Z
  - Updated: 2025-08-20T01:59:35Z

- **#32598** feat(docs): add Bigtable Key-value store doc
  - State: open
  - Created: 2025-08-18T19:49:37Z
  - Updated: 2025-08-19T14:25:04Z

- **#32596** fix(docs): `text-embedding-004` -> `gemini-embedding-001`
  - State: open
  - Created: 2025-08-18T18:40:10Z
  - Updated: 2025-08-18T18:50:48Z

- **#32593** fix(standard-tests): ensure non-negative token counts in usage metadata assertions
  - State: open
  - Created: 2025-08-18T17:49:15Z
  - Updated: 2025-08-18T17:56:02Z

- **#32588** docs: updating ConfidentAI callback handler docs
  - State: open
  - Created: 2025-08-18T13:24:20Z
  - Updated: 2025-08-18T18:41:44Z

- **#32585** chore: bump amannn/action-semantic-pull-request from 5 to 6
  - State: open
  - Created: 2025-08-18T11:41:35Z
  - Updated: 2025-08-20T01:59:55Z

- **#32584** chore: bump actions/checkout from 4 to 5
  - State: open
  - Created: 2025-08-18T11:41:28Z
  - Updated: 2025-08-20T02:00:04Z

- **#32582** feat(text-splitters): add support for batched length function in TextSplitter
  - State: open
  - Created: 2025-08-17T23:24:39Z
  - Updated: 2025-08-18T14:18:06Z

- **#32581** fix(langchain): prevent index desync causing `invalid_tool_calls`
  - State: open
  - Created: 2025-08-16T18:51:57Z
  - Updated: 2025-08-18T14:18:20Z

- **#32579** fix(core): correct FAISS cosine similarity scoring in vector stores
  - State: open
  - Created: 2025-08-16T17:42:53Z
  - Updated: 2025-08-18T14:19:38Z

- **#32578** fix(core): resolve infinite recursion in `_dereference_refs_helper` with mixed `$ref` objects
  - State: open
  - Created: 2025-08-16T17:05:58Z
  - Updated: 2025-08-18T14:20:32Z

- **#32576** chore(cli): add ruff rules ANN401 and D1
  - State: open
  - Created: 2025-08-16T15:01:52Z
  - Updated: 2025-08-18T18:43:09Z

- **#32572** refactor: enhance OpenAI data block handling and normalize message formats
  - State: open
  - Created: 2025-08-15T21:03:39Z
  - Updated: 2025-08-19T20:57:17Z

- **#32571** docs: support for YugabyteDB Distributed SQL database
  - State: open
  - Created: 2025-08-15T21:02:05Z
  - Updated: 2025-08-18T18:49:45Z

- **#32569** v1: standard content, IDs, & translators
  - State: open
  - Created: 2025-08-15T18:31:36Z
  - Updated: 2025-08-19T16:26:15Z

- **#32567** v1
  - State: open
  - Created: 2025-08-15T18:04:08Z
  - Updated: 2025-08-19T15:26:20Z

- **#32566** chore: v1 formatting
  - State: open
  - Created: 2025-08-15T17:58:59Z
  - Updated: 2025-08-19T20:05:40Z

- **#32565** refactor(core): remove `example` attribute from `AIMessage` and `HumanMessage`
  - State: open
  - Created: 2025-08-15T17:46:17Z
  - Updated: 2025-08-18T20:06:23Z

- **#32563** refactor(core): overload `convert_to_openai_messages` for clear typing
  - State: open
  - Created: 2025-08-15T16:13:15Z
  - Updated: 2025-08-15T22:17:34Z

- **#32562** Unexpected invalid_tool_calls when using a stream
  - State: open
  - Created: 2025-08-15T15:11:11Z
  - Updated: 2025-08-18T12:32:13Z

- **#32560** chore(core): fix some mypy `warn_unreachable` issues
  - State: open
  - Created: 2025-08-15T13:59:22Z
  - Updated: 2025-08-18T18:43:08Z

- **#32557** fix(openai): construct responses api input
  - State: open
  - Created: 2025-08-15T08:06:48Z
  - Updated: 2025-08-20T02:01:22Z

- **#32554** feat(docs): add Moorcheh (Vector DB) integration
  - State: open
  - Created: 2025-08-14T21:15:07Z
  - Updated: 2025-08-19T14:17:54Z

- **#32551** fix(openai): structured output
  - State: open
  - Created: 2025-08-14T17:24:41Z
  - Updated: 2025-08-18T14:05:27Z

- **#32549** feat(docs): Add hybrid search documentation to PGVectorStore
  - State: open
  - Created: 2025-08-14T12:40:23Z
  - Updated: 2025-08-19T21:25:02Z

- **#32541** feat(core): allow overriding `ls_model_name` from kwargs
  - State: open
  - Created: 2025-08-13T23:24:05Z
  - Updated: 2025-08-18T18:30:32Z

- **#32536** feat(core): add `output_version` parameter to chat model methods
  - State: open
  - Created: 2025-08-13T18:49:27Z
  - Updated: 2025-08-19T14:19:09Z

- **#32532** feat(core): Add opt-in `run_name` inheritance for child runnables
  - State: open
  - Created: 2025-08-13T15:10:37Z
  - Updated: 2025-08-14T13:29:48Z

- **#32531** fix(openai): Reuse cached httpx clients in `AzureChatOpenAI`
  - State: open
  - Created: 2025-08-13T15:09:29Z
  - Updated: 2025-08-13T18:03:01Z

## Pull Requests

- **#32605** feat(docs): add composio integration documentation
  - State: open
  - Created: 2025-08-19T12:03:07Z
  - Updated: 2025-08-19T14:35:56Z

- **#32603** feat(core): Thread `RunnableConfig` through `AgentExecutor` and tools without exposing to LLM
  - State: open
  - Created: 2025-08-19T07:20:47Z
  - Updated: 2025-08-20T01:59:35Z

- **#32598** feat(docs): add Bigtable Key-value store doc
  - State: open
  - Created: 2025-08-18T19:49:37Z
  - Updated: 2025-08-19T14:25:04Z

- **#32596** fix(docs): `text-embedding-004` -> `gemini-embedding-001`
  - State: open
  - Created: 2025-08-18T18:40:10Z
  - Updated: 2025-08-18T18:50:48Z

- **#32593** fix(standard-tests): ensure non-negative token counts in usage metadata assertions
  - State: open
  - Created: 2025-08-18T17:49:15Z
  - Updated: 2025-08-18T17:56:02Z

- **#32588** docs: updating ConfidentAI callback handler docs
  - State: open
  - Created: 2025-08-18T13:24:20Z
  - Updated: 2025-08-18T18:41:44Z

- **#32585** chore: bump amannn/action-semantic-pull-request from 5 to 6
  - State: open
  - Created: 2025-08-18T11:41:35Z
  - Updated: 2025-08-20T01:59:55Z

- **#32584** chore: bump actions/checkout from 4 to 5
  - State: open
  - Created: 2025-08-18T11:41:28Z
  - Updated: 2025-08-20T02:00:04Z

- **#32582** feat(text-splitters): add support for batched length function in TextSplitter
  - State: open
  - Created: 2025-08-17T23:24:39Z
  - Updated: 2025-08-18T14:18:06Z

- **#32581** fix(langchain): prevent index desync causing `invalid_tool_calls`
  - State: open
  - Created: 2025-08-16T18:51:57Z
  - Updated: 2025-08-18T14:18:20Z

- **#32579** fix(core): correct FAISS cosine similarity scoring in vector stores
  - State: open
  - Created: 2025-08-16T17:42:53Z
  - Updated: 2025-08-18T14:19:38Z

- **#32578** fix(core): resolve infinite recursion in `_dereference_refs_helper` with mixed `$ref` objects
  - State: open
  - Created: 2025-08-16T17:05:58Z
  - Updated: 2025-08-18T14:20:32Z

- **#32576** chore(cli): add ruff rules ANN401 and D1
  - State: open
  - Created: 2025-08-16T15:01:52Z
  - Updated: 2025-08-18T18:43:09Z

- **#32572** refactor: enhance OpenAI data block handling and normalize message formats
  - State: open
  - Created: 2025-08-15T21:03:39Z
  - Updated: 2025-08-19T20:57:17Z

- **#32571** docs: support for YugabyteDB Distributed SQL database
  - State: open
  - Created: 2025-08-15T21:02:05Z
  - Updated: 2025-08-18T18:49:45Z

- **#32569** v1: standard content, IDs, & translators
  - State: open
  - Created: 2025-08-15T18:31:36Z
  - Updated: 2025-08-19T16:26:15Z

- **#32567** v1
  - State: open
  - Created: 2025-08-15T18:04:08Z
  - Updated: 2025-08-19T15:26:20Z

- **#32566** chore: v1 formatting
  - State: open
  - Created: 2025-08-15T17:58:59Z
  - Updated: 2025-08-19T20:05:40Z

- **#32565** refactor(core): remove `example` attribute from `AIMessage` and `HumanMessage`
  - State: open
  - Created: 2025-08-15T17:46:17Z
  - Updated: 2025-08-18T20:06:23Z

- **#32563** refactor(core): overload `convert_to_openai_messages` for clear typing
  - State: open
  - Created: 2025-08-15T16:13:15Z
  - Updated: 2025-08-15T22:17:34Z

- **#32560** chore(core): fix some mypy `warn_unreachable` issues
  - State: open
  - Created: 2025-08-15T13:59:22Z
  - Updated: 2025-08-18T18:43:08Z

- **#32557** fix(openai): construct responses api input
  - State: open
  - Created: 2025-08-15T08:06:48Z
  - Updated: 2025-08-20T02:01:22Z

- **#32554** feat(docs): add Moorcheh (Vector DB) integration
  - State: open
  - Created: 2025-08-14T21:15:07Z
  - Updated: 2025-08-19T14:17:54Z

- **#32551** fix(openai): structured output
  - State: open
  - Created: 2025-08-14T17:24:41Z
  - Updated: 2025-08-18T14:05:27Z

- **#32549** feat(docs): Add hybrid search documentation to PGVectorStore
  - State: open
  - Created: 2025-08-14T12:40:23Z
  - Updated: 2025-08-19T21:25:02Z

- **#32541** feat(core): allow overriding `ls_model_name` from kwargs
  - State: open
  - Created: 2025-08-13T23:24:05Z
  - Updated: 2025-08-18T18:30:32Z

- **#32536** feat(core): add `output_version` parameter to chat model methods
  - State: open
  - Created: 2025-08-13T18:49:27Z
  - Updated: 2025-08-19T14:19:09Z

- **#32532** feat(core): Add opt-in `run_name` inheritance for child runnables
  - State: open
  - Created: 2025-08-13T15:10:37Z
  - Updated: 2025-08-14T13:29:48Z

- **#32531** fix(openai): Reuse cached httpx clients in `AzureChatOpenAI`
  - State: open
  - Created: 2025-08-13T15:09:29Z
  - Updated: 2025-08-13T18:03:01Z

- **#32526** fix(core): preserve ordering in RunnableRetry batch/abatch results
  - State: open
  - Created: 2025-08-13T11:14:34Z
  - Updated: 2025-08-13T14:19:31Z

