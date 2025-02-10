import duckdb
from rich import print
from dataclasses import dataclass


@dataclass
class LogEntry:
    type: str
    request_id: str
    timestamp: int
    body: dict

    def print(self):
        if self.type == "request":
            print("[bold blue]Request Messages:[/bold blue]")
            for msg in self.body["messages"]:
                role = msg["role"].title()
                print(f"\n[bold cyan][ROLE] {role}:[/bold cyan]")
                for content in msg["content"]:
                    print(content["text"])
                print("\n[dim]" + "=" * 120 + "[/dim]")
        elif self.type == "response":
            print("\n[bold green]Response Content:[/bold green]")
            print(self.body["choices"][0]["message"]["content"])


conn = duckdb.connect()

conn.execute(
    """
    SELECT 
        j.type,
        j.request_id,
        j.timestamp,
        j.body,
    FROM read_json_auto('openai_logs.jsonl') AS j
    ORDER BY j.timestamp
"""
).df()

rows = [
    LogEntry(*row)
    for row in conn.execute(
        """
    SELECT 
        j.type,
        j.request_id,
        j.timestamp,
        j.body,
    FROM read_json_auto('openai_logs.jsonl') AS j
    ORDER BY j.timestamp
"""
    ).fetchall()
]

for i, row in enumerate(rows):
    print(f"\n[bold magenta]{'*' * 40} Log Entry {i + 1} {'*' * 40}[/bold magenta]")
    row.print()
