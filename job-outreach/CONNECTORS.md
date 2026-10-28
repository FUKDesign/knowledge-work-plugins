# Connectors

## How tool references work

Unlike the tool-agnostic team plugins in this repo, this personal plugin is written against specific connectors, because the pipeline is stored as Gmail labels and Upwork has its own job tools. Equivalent tools in the same category can be swapped in, but the skills name these tools directly.

## Connectors for this plugin

| Category | Connector | Required | Tools used | Other options |
|----------|-----------|----------|------------|---------------|
| Email | Gmail | Yes | `search_threads`, `get_thread`, `list_labels`, `create_label`, `label_thread`, `unlabel_thread`, `label_message`, `list_drafts`, `create_draft` | None (labels are Gmail-specific) |
| Freelance marketplace | Upwork | Recommended | `find_jobs`, `save_job`, `find_saved_jobs` | — |
| Web search | Built-in web search / fetch | Yes | Search and page fetch | Tavily, Bright Data, Nimble |
| Calendar | Google Calendar | Optional | `list_events`, `search_events` (read-only, to confirm interviews) | Microsoft 365 |

## Tools this plugin must never call

The plugin is drafts-only. These tools exist on the connectors but are off-limits to every skill and the agent:

- Gmail: `send_message`, `reply`, `forward`, `trash_thread`, `trash_message`, `delete_draft`, `delete_label`
- Upwork: `manage_proposals`, `send_message`, `respond_to_offer`
- Google Calendar: `create_event`, `respond_to_event` (unless the user explicitly asks)
