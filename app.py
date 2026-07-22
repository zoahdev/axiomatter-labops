from __future__ import annotations

import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from ai4s_lab.ai_client import parse_design_brief
from ai4s_lab.engine import MaterialEngine
from ai4s_lab.orchestrator import LabOpsOrchestrator


ROOT = Path(__file__).resolve().parent
ENGINE = MaterialEngine(ROOT / "data" / "demo_cathodes.csv")
ORCHESTRATOR = LabOpsOrchestrator(ENGINE)


class AppHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path: str) -> str:
        clean = urlparse(path).path
        if clean == "/":
            return str(ROOT / "static" / "index.html")
        return str(ROOT / "static" / clean.lstrip("/"))

    def do_GET(self) -> None:
        if self.path == "/health":
            self._json({"status": "ok", "materials": len(ENGINE.materials)})
            return
        super().do_GET()

    def do_POST(self) -> None:
        if self.path not in {"/api/screen", "/api/run"}:
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            brief = str(payload.get("brief", "")).strip()
            if not brief:
                raise ValueError("brief is required")
            if len(brief) > 4000:
                raise ValueError("brief is too long")
            target = parse_design_brief(brief, ROOT)
            result = ORCHESTRATOR.run(brief, target)
            self._json(result)
        except (ValueError, json.JSONDecodeError) as exc:
            self._json({"error": str(exc)}, status=400)

    def _json(self, payload: object, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        print(f"[ai4s] {self.address_string()} - {format % args}")


def main() -> None:
    host = os.environ.get("AXIOMATTER_HOST", "127.0.0.1")
    port = int(os.environ.get("AXIOMATTER_PORT", "8765"))
    server = ThreadingHTTPServer((host, port), AppHandler)
    print(f"AI4S materials lab running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()

