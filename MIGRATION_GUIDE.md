# Aleopantest V3.0 Migration Guide
<div style="font-size: 80%; color: #666666;">by Aleocrophic</div>

Welcome to Aleopantest V3.0! This guide will help you migrate your scripts and environments from previous versions (V3.3.x or older) to the new standardized V3.0 architecture.

## 1. Overview of Changes
V3.0 is a major patch focused on **consistency, accuracy, and power**. The entire tool suite has been updated to follow a strict structural standard.

- **Unified Versioning**: All modules are now version `3.0.0`.
- **Output Standardization**: `get_results()` is now the standard way to retrieve tool findings.
- **Enhanced JSON**: All JSON outputs now include comprehensive metadata and zero empty arrays.

## 2. Code Changes for Developers
If you have custom modules, please follow these steps:

### Update Metadata
Ensure your tool metadata uses `version="3.0.0"` and `author="Aleocrophic Team"`.

```python
metadata = ToolMetadata(
    name="Your Tool",
    version="3.0.0",
    author="Aleocrophic Team",
    # ...
)
```

### Adopt `get_results()`
The `BaseTool.get_results()` method has been upgraded. Instead of manually building dictionaries or returning `self.results`, simply return the result of `self.get_results()`.

**Old Way:**
```python
def run(self, **kwargs):
    # ... logic ...
    return self.results
```

**V3.0 Way:**
```python
def run(self, **kwargs):
    # ... logic ...
    return self.get_results()
```

## 3. Command Line Interface (CLI)
The command name is now strictly `aleopantest`.
- Previous: `python aleopantest_cli.py` or `aleocrophic`
- V3.0: `aleopantest`

To run a tool:
```bash
aleopantest run port-scan --host 127.0.0.1
```

## 4. Web Dashboard
The web API now uses the `/aleopantest` prefix for all routes.
- Ensure your scripts point to `http://localhost:8002/aleopantest/api/...`

## 5. TUI (Textual)
The TUI has been updated for better performance. Launch it via:
```bash
aleopantest tui
```

---
© 2025 Aleocrophic. All Rights Reserved.
