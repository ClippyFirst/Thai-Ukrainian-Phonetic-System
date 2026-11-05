#!/usr/bin/env python3
"""Parse workflow YAML and syntax-check literal bash run blocks."""
from __future__ import annotations

import subprocess
from pathlib import Path

import yaml


def main() -> None:
    files = sorted(Path(".github/workflows").glob("*.y*ml"))
    if not files:
        raise SystemExit("No GitHub Actions workflow files found")
    checked_blocks = 0
    for path in files:
        document = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        if not isinstance(document, dict) or not isinstance(document.get("jobs"), dict):
            raise SystemExit(f"Invalid workflow structure: {path}")
        for job_name, job in document["jobs"].items():
            if not isinstance(job, dict):
                raise SystemExit(f"Invalid job {job_name} in {path}")
            for index, step in enumerate(job.get("steps", []), start=1):
                if not isinstance(step, dict):
                    raise SystemExit(f"Invalid step {index} in {path}:{job_name}")
                script = step.get("run")
                if not script or step.get("shell", "bash") not in ("bash", "sh"):
                    continue
                if "${{" in script:
                    continue
                subprocess.run(
                    ["bash", "-n"],
                    input=script,
                    text=True,
                    check=True,
                    capture_output=True,
                )
                checked_blocks += 1
    print(f"Workflow YAML parsed; {checked_blocks} literal bash run blocks passed bash -n across {len(files)} workflows")


if __name__ == "__main__":
    main()
