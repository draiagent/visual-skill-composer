#!/usr/bin/env python3
"""Cross-check the packs, the registry, and the UI's embedded copy of the same data.

ui/index.html deliberately embeds its data so it runs with zero dependencies from a
file:// URL. That means the ids can drift away from the YAML packs. This catches it.

    python tools/check_consistency.py
"""
import glob
import io
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml")

import json

PROBLEMS = []


def problem(msg):
    PROBLEMS.append(msg)


def load_yaml(path):
    return yaml.safe_load(io.open(path, encoding="utf-8").read())


def ids_from_dir(pattern):
    out = {}
    for path in sorted(glob.glob(pattern)):
        doc = load_yaml(path)
        out[doc["id"]] = doc
        stem = os.path.splitext(os.path.basename(path))[0].replace(".example", "")
        if stem != doc["id"]:
            problem("filename/id mismatch: " + path + " declares id '" + doc["id"] + "'")
    return out


def ui_block(src, name):
    """Pull the id list out of one `var NAME = [ ... ];` block in the UI."""
    m = re.search(r"var " + name + r" = \[(.*?)\n\];", src, re.S)
    if not m:
        problem("UI: could not find block " + name)
        return []
    return re.findall(r"\{id:'([a-z0-9-]+)'", m.group(1))


def main():
    reg = json.load(io.open("registry/skills.json", encoding="utf-8"))
    skills = {s["id"]: s for s in reg["skills"]}
    cats = {c["id"] for c in reg["categories"]}

    projects = ids_from_dir("project-packs/*.yaml")
    styles = ids_from_dir("style-packs/*.yaml")
    qas = ids_from_dir("qa-packs/*.yaml")
    brands = ids_from_dir("brand-packs/*.yaml")

    # --- registry internals -------------------------------------------------
    for sid, s in skills.items():
        if s["category"] not in cats:
            problem("skill '" + sid + "' has unknown category '" + s["category"] + "'")
        for req in s["requires"]:
            if req not in skills:
                problem("skill '" + sid + "' requires unknown skill '" + req + "'")
        for lang in ("en", "zh-TW"):
            if not s["label"].get(lang) or not s["summary"].get(lang):
                problem("skill '" + sid + "' is missing a " + lang + " label or summary")
        if not os.path.exists("skills/" + sid + ".md"):
            problem("skill '" + sid + "' has no contract file (run tools/gen_skill_docs.py)")

    # --- project packs ------------------------------------------------------
    referenced = set()
    for pid, p in projects.items():
        listed = p.get("recommended_skills", []) + p.get("suggested_skills", [])
        referenced.update(listed)
        for sid in listed:
            if sid not in skills:
                problem("project '" + pid + "' references unknown skill '" + sid + "'")
                continue
            for req in skills[sid]["requires"]:
                if req not in listed:
                    problem(
                        "project '" + pid + "' offers '" + sid + "' but never offers its "
                        "prerequisite '" + req + "'"
                    )
        overlap = set(p.get("recommended_skills", [])) & set(p.get("suggested_skills", []))
        if overlap:
            problem("project '" + pid + "' lists " + str(sorted(overlap)) + " as both recommended and suggested")
        if p.get("default_style") not in styles:
            problem("project '" + pid + "' default_style '" + str(p.get("default_style")) + "' has no style pack")
        if p.get("default_qa") not in qas:
            problem("project '" + pid + "' default_qa '" + str(p.get("default_qa")) + "' has no qa pack")

    for sid in skills:
        if sid not in referenced and skills[sid]["category"] != "quality":
            problem("skill '" + sid + "' is not offered by any project pack, so it is unreachable")

    # --- style packs --------------------------------------------------------
    for stid, st in styles.items():
        if not st.get("avoid"):
            problem("style '" + stid + "' has no avoid list, so vision-judge cannot enforce it")
        for key in ("bg", "fg", "accent"):
            if key not in st.get("tokens", {}):
                problem("style '" + stid + "' is missing token '" + key + "'")

    # --- qa packs -----------------------------------------------------------
    for qid, q in qas.items():
        for sid in q["checks"]:
            if sid not in skills:
                problem("qa pack '" + qid + "' runs unknown check '" + sid + "'")
        if q["threshold"] > 60 and q["max_repair_rounds"] == 0 and "auto-repair" in q["checks"]:
            problem("qa pack '" + qid + "' enables auto-repair but allows zero rounds")

    # --- UI vs packs --------------------------------------------------------
    src = io.open("ui/index.html", encoding="utf-8").read()
    for name, truth, label in (
        ("PROJECTS", projects, "project pack"),
        ("STYLES", styles, "style pack"),
        ("QAS", qas, "qa pack"),
        ("SKILLS", skills, "skill"),
    ):
        seen = ui_block(src, name)
        for uid in seen:
            if uid not in truth:
                problem("UI " + name + " has '" + uid + "' with no matching " + label)
        for tid in truth:
            if tid not in seen:
                problem("UI " + name + " is missing '" + tid + "' which exists as a " + label)

    ui_brands = ui_block(src, "BRANDS")
    for bid in ui_brands:
        if bid != "upload" and bid not in brands:
            problem("UI BRANDS has '" + bid + "' with no matching brand pack")

    # --- doc links ----------------------------------------------------------
    for path in glob.glob("*.md") + glob.glob("docs/*/*.md"):
        text = io.open(path, encoding="utf-8").read()
        for link in re.findall(r"\]\((\.[^)]+)\)", text):
            target = os.path.normpath(os.path.join(os.path.dirname(path), link.split("#")[0]))
            if not os.path.exists(target):
                problem("broken link in " + path + ": " + link)

    if PROBLEMS:
        print(str(len(PROBLEMS)) + " problem(s):")
        for p in PROBLEMS:
            print("  - " + p)
        return 1
    print("consistency OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
