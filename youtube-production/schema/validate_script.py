#!/usr/bin/env python3
"""
BUILT Video Script Validator
Validates a video script JSON against the canonical schema.

Checks:
  1. STRUCTURAL  — All required schema fields present
  2. CONTENT     — No empty strings/arrays on required fields
  3. CONSISTENCY — Passage numbers sequential, refs point to existing IDs
  4. COMPLETENESS — story always filled, source_registry has retrieved_at, etc.

Usage:
  python3 validate_script.py <path-to-script.json>
"""

import json
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).parent / "video_skript_schema.json"

# Fields where empty string / null is acceptable
NULLABLE_FIELDS = {
    "phase_anchor", "text_overlay", "source_overlay", "camera_tip",
    "fallback", "teleprompter", "title_alt",
}

# Fields where empty array is acceptable
NULLABLE_ARRAYS = {
    "talking_points", "stage_directions", "graphic_refs", "prompt_refs",
    "retention_markers", "term_brands",
}


class ValidationResult:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    @property
    def ok(self):
        return len(self.errors) == 0


def get_schema_keys(obj, prefix=""):
    """Extract all key paths from the schema template."""
    keys = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.startswith("$"):
                continue
            full = f"{prefix}.{k}" if prefix else k
            keys[full] = type(v).__name__
            if isinstance(v, dict):
                keys.update(get_schema_keys(v, full))
            elif isinstance(v, list) and v and isinstance(v[0], dict):
                keys.update(get_schema_keys(v[0], f"{full}[]"))
    return keys


def get_data_keys(obj, prefix=""):
    """Extract all key paths from actual data."""
    keys = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.startswith("$"):
                continue
            full = f"{prefix}.{k}" if prefix else k
            keys.add(full)
            if isinstance(v, dict):
                keys.update(get_data_keys(v, full))
            elif isinstance(v, list) and v and isinstance(v[0], dict):
                # Check first item as representative
                keys.update(get_data_keys(v[0], f"{full}[]"))
    return keys


def check_structural(schema, data, result):
    """Check 1: All schema fields present in data."""
    schema_keys = set(get_schema_keys(schema).keys())
    data_keys = get_data_keys(data)

    missing = sorted(schema_keys - data_keys)
    for key in missing:
        result.error(f"[STRUCTURAL] Missing field: {key}")

    extra = sorted(data_keys - schema_keys)
    # Filter out sub-keys of open objects (style, verified_api_details)
    open_objects = {"style", "verified_api_details"}
    for key in extra:
        parts = key.replace("[]", "").split(".")
        if any(p in open_objects for p in parts):
            continue
        result.warn(f"[STRUCTURAL] Extra field not in schema: {key}")


def check_content(data, result):
    """Check 2: No empty strings/arrays on required fields."""
    # meta
    meta = data.get("meta", {})
    for field in ["title", "format", "cluster", "date", "editing_pattern"]:
        val = meta.get(field)
        if not val or (isinstance(val, str) and not val.strip()):
            result.error(f"[CONTENT] meta.{field} is empty")

    # a1_concept
    concept = data.get("a1_concept", {})
    for field in ["title", "target_audience", "core_promise", "magic_moment",
                  "target_persona", "emotional_target", "differentiation"]:
        val = concept.get(field)
        if not val or (isinstance(val, str) and not val.strip()):
            result.error(f"[CONTENT] a1_concept.{field} is empty")

    if not concept.get("stack"):
        result.error("[CONTENT] a1_concept.stack is empty")

    # hook
    hook = concept.get("hook", {})
    for field in ["type", "opening_line", "rationale", "engagement_question"]:
        val = hook.get(field)
        if not val or (isinstance(val, str) and not val.strip()):
            result.error(f"[CONTENT] a1_concept.hook.{field} is empty")

    pas = hook.get("pas", {})
    for field in ["problem", "agitation", "solution"]:
        val = pas.get(field)
        if not val or (isinstance(val, str) and not val.strip()):
            result.error(f"[CONTENT] a1_concept.hook.pas.{field} is empty")

    # snowball_keywords
    kw = concept.get("snowball_keywords", {})
    if not kw.get("main_keyword"):
        result.error("[CONTENT] a1_concept.snowball_keywords.main_keyword is empty")

    # source_registry
    registry = concept.get("source_registry", [])
    if not registry:
        result.warn("[CONTENT] a1_concept.source_registry is empty — no sources documented")

    # a2_roadmap
    roadmap = data.get("a2_roadmap", [])
    if not roadmap:
        result.error("[CONTENT] a2_roadmap is empty")

    # a3_script
    script = data.get("a3_script", [])
    if not script:
        result.error("[CONTENT] a3_script is empty")

    # a4_visuals
    visuals = data.get("a4_visuals", [])
    if not visuals:
        result.warn("[CONTENT] a4_visuals is empty — no graphics defined")

    # a5_prompts (may be empty for explainer videos)
    prompts = data.get("a5_prompts", [])
    if not prompts:
        result.warn("[CONTENT] a5_prompts is empty")

    # a7_cheat_sheet
    cheat = data.get("a7_cheat_sheet", [])
    if not cheat:
        result.error("[CONTENT] a7_cheat_sheet is empty")

    # a8_upload
    upload = data.get("a8_upload", {})
    if not upload.get("title_variants"):
        result.error("[CONTENT] a8_upload.title_variants is empty")
    if not upload.get("description"):
        result.error("[CONTENT] a8_upload.description is empty")
    if not upload.get("tags"):
        result.error("[CONTENT] a8_upload.tags is empty")


def check_consistency(data, result):
    """Check 3: Passage numbers sequential, refs point to existing IDs."""
    script = data.get("a3_script", [])
    visuals = data.get("a4_visuals", [])
    prompts = data.get("a5_prompts", [])

    # Passage numbers sequential
    passage_nums = [p.get("passage") for p in script]
    expected = list(range(1, len(script) + 1))
    if passage_nums != expected:
        result.error(f"[CONSISTENCY] Passage numbers not sequential: {passage_nums}")

    # Collect valid IDs
    visual_ids = {v.get("id") for v in visuals}
    prompt_ids = {p.get("id") for p in prompts}

    # Check graphic_refs and prompt_refs in script
    for p in script:
        num = p.get("passage", "?")
        for ref in p.get("graphic_refs", []):
            if ref not in visual_ids:
                result.error(f"[CONSISTENCY] Passage {num}: graphic_ref '{ref}' not found in a4_visuals")
        for ref in p.get("prompt_refs", []):
            if ref not in prompt_ids:
                result.error(f"[CONSISTENCY] Passage {num}: prompt_ref '{ref}' not found in a5_prompts")

    # Check visual passage references
    for v in visuals:
        vid = v.get("id", "?")
        vpassage = v.get("passage")
        if vpassage and vpassage not in [p.get("passage") for p in script]:
            result.warn(f"[CONSISTENCY] Visual {vid}: references passage {vpassage} which doesn't exist")

    # Check prompt passage references
    for pr in prompts:
        pid = pr.get("id", "?")
        ppassage = pr.get("passage")
        if ppassage and ppassage not in [p.get("passage") for p in script]:
            result.warn(f"[CONSISTENCY] Prompt {pid}: references passage {ppassage} which doesn't exist")

    # Timing plausibility check
    target_min = data.get("meta", {}).get("length_min", 0)
    if target_min and script:
        total_sec = sum(p.get("duration_sec", 0) for p in script)
        target_sec = target_min * 60
        deviation = abs(total_sec - target_sec) / target_sec if target_sec else 0
        if deviation > 0.15:
            direction = "over" if total_sec > target_sec else "under"
            result.error(
                f"[TIMING] Total passage duration ({total_sec}s = {total_sec/60:.1f} min) "
                f"is {deviation:.0%} {direction} target ({target_sec}s = {target_min} min). "
                f"Tolerance: ±15%"
            )
        else:
            # Info line in report (not error/warning)
            result.warn(
                f"[TIMING] Total: {total_sec}s ({total_sec/60:.1f} min) vs target "
                f"{target_sec}s ({target_min} min) — deviation {deviation:.0%} ✓"
            )


def check_completeness(data, result):
    """Check 4: story always filled, modes correct, source_registry complete."""
    script = data.get("a3_script", [])

    for p in script:
        num = p.get("passage", "?")
        mode = p.get("mode")
        story = p.get("story")
        teleprompter = p.get("teleprompter")
        talking_points = p.get("talking_points", [])

        # story must ALWAYS be filled
        if not story or (isinstance(story, str) and not story.strip()):
            result.error(f"[COMPLETENESS] Passage {num}: story is empty (must always be filled)")

        # mode validation
        if mode not in ("teleprompter", "story"):
            result.error(f"[COMPLETENESS] Passage {num}: mode is '{mode}', must be 'teleprompter' or 'story'")

        # teleprompter mode: teleprompter text required
        if mode == "teleprompter":
            if not teleprompter or (isinstance(teleprompter, str) and not teleprompter.strip()):
                result.error(f"[COMPLETENESS] Passage {num}: mode is 'teleprompter' but teleprompter text is empty")

        # story mode: talking_points required
        if mode == "story":
            if not talking_points:
                result.warn(f"[COMPLETENESS] Passage {num}: mode is 'story' but talking_points is empty")
            if teleprompter:
                result.warn(f"[COMPLETENESS] Passage {num}: mode is 'story' but teleprompter is filled (should be null)")

        # block_type required
        if not p.get("block_type"):
            result.error(f"[COMPLETENESS] Passage {num}: block_type is empty")

        # duration_sec > 0
        if not p.get("duration_sec") or p.get("duration_sec", 0) <= 0:
            result.warn(f"[COMPLETENESS] Passage {num}: duration_sec is 0 or missing")

    # source_registry entries complete
    registry = data.get("a1_concept", {}).get("source_registry", [])
    for i, entry in enumerate(registry):
        if not entry.get("source"):
            result.error(f"[COMPLETENESS] source_registry[{i}]: source is empty")
        if not entry.get("retrieved_at"):
            result.warn(f"[COMPLETENESS] source_registry[{i}]: retrieved_at is empty")

    # a6_rehearsal checks
    rehearsal = data.get("a6_rehearsal", {})
    if not rehearsal.get("prerequisites"):
        result.warn("[COMPLETENESS] a6_rehearsal.prerequisites is empty")
    if not rehearsal.get("checklist_before"):
        result.warn("[COMPLETENESS] a6_rehearsal.checklist_before is empty")
    if not rehearsal.get("checklist_shoot_day"):
        result.warn("[COMPLETENESS] a6_rehearsal.checklist_shoot_day is empty")

    # Consulting anchor check
    upload = data.get("a8_upload", {})
    anchor = upload.get("consulting_anchor", {})
    if not anchor.get("text"):
        result.warn("[COMPLETENESS] a8_upload.consulting_anchor.text is empty — min. 1 required")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_script.py <path-to-script.json>")
        sys.exit(1)

    script_path = Path(sys.argv[1])
    if not script_path.exists():
        print(f"Error: File not found: {script_path}")
        sys.exit(1)

    if not SCHEMA_PATH.exists():
        print(f"Error: Schema not found: {SCHEMA_PATH}")
        sys.exit(1)

    with open(SCHEMA_PATH) as f:
        schema = json.load(f)

    with open(script_path) as f:
        data = json.load(f)

    result = ValidationResult()

    check_structural(schema, data, result)
    check_content(data, result)
    check_consistency(data, result)
    check_completeness(data, result)

    # Report
    print(f"\n{'='*60}")
    print(f"  BUILT Video Script Validator")
    print(f"  File: {script_path.name}")
    print(f"{'='*60}\n")

    if result.errors:
        print(f"  ERRORS ({len(result.errors)}):\n")
        for e in result.errors:
            print(f"    ❌ {e}")
        print()

    if result.warnings:
        print(f"  WARNINGS ({len(result.warnings)}):\n")
        for w in result.warnings:
            print(f"    ⚠️  {w}")
        print()

    if result.ok:
        print(f"  ✅ VALIDATION PASSED ({len(result.warnings)} warnings)\n")
    else:
        print(f"  ❌ VALIDATION FAILED ({len(result.errors)} errors, {len(result.warnings)} warnings)\n")

    sys.exit(0 if result.ok else 1)


if __name__ == "__main__":
    main()
