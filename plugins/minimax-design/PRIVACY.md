# Privacy

MiniMax Design is a local plugin. It does not include telemetry, advertising, or a hosted data service.

What leaves the machine, and only when the user explicitly requests paid generation: the prompt, optional reference images (base64), and task parameters are sent to the MiniMax API gateway configured via `MINIMAX_BASE` (default `api.minimaxi.com`), authenticated with the user's own `MINIMAX_API_KEY`. The plugin never reads, stores, or transmits the key beyond that authentication header.

Generated videos, task ids, and logs remain under user-selected paths. The optional `mmx` CLI stores its own credentials at `~/.mmx/credentials.json` (outside this plugin). Users should review MiniMax platform privacy terms before enabling integrations.
