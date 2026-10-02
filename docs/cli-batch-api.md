# CLI, batch processing and JSON API

The research core is exposed through the `thai-ua` command without changing the linguistic model.

## Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

Excel support:

```powershell
pip install -e ".[excel]"
```

## Single analysis

```powershell
thai-ua analyze "กา"
```

Compact JSON:

```powershell
thai-ua analyze "กา" --compact
```

The output is structured JSON and retains graphemic analysis, tone, IPA, warnings, Ukrainian candidate output and status.

## Batch mode

### TXT

One non-empty Thai input per line:

```powershell
thai-ua batch input.txt -o output.jsonl
```

### CSV

The CLI uses a `thai` column automatically when present:

```powershell
thai-ua batch input.csv -o output.csv
```

Or specify a column:

```powershell
thai-ua batch input.csv -c word -o output.xlsx
```

### Excel

```powershell
thai-ua batch input.xlsx -c Thai -o output.xlsx
```

Select a sheet explicitly:

```powershell
thai-ua batch input.xlsx --sheet Words -c Thai -o results.xlsx
```

Supported output formats are `.json`, `.jsonl`, `.csv` and `.xlsx`.

The batch layer preserves the full structured analysis in JSON/JSONL. CSV/XLSX provide a practical tabular summary with input, status, IPA, tone, Ukrainian candidates and warnings.

## Local JSON API

Start the server:

```powershell
thai-ua serve
```

Default address: `http://127.0.0.1:8787`

Health check:

```powershell
curl http://127.0.0.1:8787/health
```

Analyze:

```powershell
curl -X POST http://127.0.0.1:8787/analyze -H "Content-Type: application/json" -d '{"text":"กา"}'
```

Request:

```json
{"text":"กา"}
```

The response is the same structured analysis envelope used by the batch layer. The server is intentionally local by default and uses Python's standard-library HTTP server; it is not presented as a production internet-facing service.

## Important boundary

The CLI/API is an interface layer, not a new transliteration algorithm. It does not invent word segmentation, override unresolved analyses, or convert project-specific Ukrainian candidates into an official Ukrainian transliteration standard.

For research workflows, `status`, `warnings`, `analyses`, and provenance-bearing fields should be retained rather than reduced to a single output string.
