from mitmproxy import ctx
import json
from pathlib import Path
import uuid
import time


def request(flow):
    """Store request body to jsonl file."""
    if "api.openai.com" in flow.request.pretty_url:
        try:
            body = flow.request.content
            if body:
                # Generate request ID and store in flow metadata
                request_id = str(uuid.uuid4())[:8]
                flow.metadata["request_id"] = request_id

                body_json = json.loads(body)
                log_entry = {
                    "type": "request",
                    "request_id": request_id,
                    "timestamp": int(time.time()),
                    "body": body_json,
                }
                with Path("openai_logs.jsonl").open("a") as f:
                    f.write(json.dumps(log_entry) + "\n")
        except json.JSONDecodeError:
            ctx.log.info(f"\nRequest Body (raw):\n{body.decode()}")


def response(flow):
    """Store response body to jsonl file."""
    if "api.openai.com" in flow.request.pretty_url:
        try:
            body = flow.response.content
            if body:
                # Get request ID from flow metadata
                request_id = flow.metadata.get("request_id", str(uuid.uuid4())[:8])

                body_json = json.loads(body)
                log_entry = {
                    "type": "response",
                    "request_id": request_id,
                    "timestamp": int(time.time()),
                    "body": body_json,
                }
                with Path("openai_logs.jsonl").open("a") as f:
                    f.write(json.dumps(log_entry) + "\n")
        except json.JSONDecodeError:
            ctx.log.info(f"\nResponse Body (raw):\n{body.decode()}")
