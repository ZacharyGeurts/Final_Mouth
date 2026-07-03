"""Hostess 7 Military EOL speech — mouth lane wired to sovereign vision + viseme."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parent
_SG = _ROOT.parent
_ENGINE = "Hostess7/MilitaryEOL/Mouth"
_SCHEMA = "zocr-military-eol-mouth/v1"


def _eye_military():
    eye = _SG / "Final_Eye" / "zocr_military_eol.py"
    if not eye.is_file():
        return None
    spec = importlib.util.spec_from_file_location("zocr_military_eol_mouth", eye)
    if not spec or not spec.loader:
        return None
    mod = importlib.util.module_from_spec(spec)
    if str(eye.parent) not in sys.path:
        sys.path.insert(0, str(eye.parent))
    spec.loader.exec_module(mod)
    return mod


def military_eol_ready() -> bool:
    mod = _eye_military()
    return bool(mod and mod.military_eol_ready())


def speak_glyph(path: Path | str) -> dict[str, Any]:
    mod = _eye_military()
    if not mod:
        return {"ok": False, "error": "final_eye_military_missing", "engine": _ENGINE}
    inspect = mod.inspect_image(path)
    neural = inspect.get("neural") or {}
    viseme = neural.get("top_label") or "rest"
    return {
        "ok": bool(inspect.get("ok")),
        "schema": _SCHEMA,
        "engine": _ENGINE,
        "sense": "mouth",
        "cross_wire": "Final_Eye.inspect_image",
        "inspect": inspect,
        "viseme": viseme,
        "utterance": f"@{viseme}",
    }


def military_ocr_image(path: Path | str, **kwargs: Any) -> str:
    row = speak_glyph(path)
    return str(row.get("utterance") or "") if row.get("ok") else ""