#!/usr/bin/env python3
"""Audit kien-*.tex resumes against their spec header + house rules.
Usage: audit.py FILE.tex [FILE2.tex ...] [--no-compile] [--json]
Exit 1 if any FAIL."""
import json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CV = os.path.expanduser("~/cv")
FACT_SOURCES = ["AUDIT-2026-09-21.md", "HANDOFF.md", "lab.md", "kien-swe.tex", "devops/kien-devops.tex"]
MEMORY = os.path.expanduser("~/.claude/projects/-home-k1en-cv/memory")
ATS_TARGET = 80


def load_rules():
    forb, alias = [], {}
    for line in open(os.path.join(HERE, "forbidden.txt"), encoding="utf-8"):
        if line.strip() and not line.startswith("#"):
            rx, sev, why = [p.strip() for p in line.split("|", 2)] if line.count("|") >= 2 else (None,) * 3
            # regex itself may contain '|': re-split on the last two pipes
            parts = line.rsplit("|", 2)
            rx, sev, why = parts[0].strip(), parts[1].strip(), parts[2].strip()
            forb.append((re.compile(rx, re.I), sev, why))
    for line in open(os.path.join(HERE, "aliases.txt"), encoding="utf-8"):
        if "->" in line and not line.startswith("#"):
            keys, vals = line.split("->", 1)
            for k in keys.split("|"):
                alias[k.strip().lower()] = [v.strip().lower() for v in vals.split(",")]
    return forb, alias


def strip_comments(tex):
    return "\n".join(re.sub(r"(?<!\\)%.*", "", l) for l in tex.splitlines())


def plain(tex):
    t = strip_comments(tex)
    t = re.sub(r"\\href\{[^}]*\}\{([^}]*)\}", r"\1", t)
    t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", t)
    return re.sub(r"[{}$~]", " ", t).lower()


def header(tex):
    head = tex.split("\\documentclass", 1)[0]
    fields = {}
    for l in head.splitlines():
        m = re.match(r"%\s*([A-Za-z /(),]+?):\s*(.*)", l)
        if m:
            fields[m.group(1).strip().lower()] = m.group(2).strip()
    return head, fields


def split_terms(s):
    return [t.strip() for t in re.split(r",|;", s) if t.strip()]


def fact_corpus():
    txt = ""
    for f in FACT_SOURCES:
        p = os.path.join(CV, f)
        if os.path.exists(p):
            txt += open(p, encoding="utf-8", errors="ignore").read()
    if os.path.isdir(MEMORY):
        for f in os.listdir(MEMORY):
            txt += open(os.path.join(MEMORY, f), encoding="utf-8", errors="ignore").read()
    return re.sub(r"[{}$~\\]", "", txt).lower()


def numbers(text):
    return set(re.findall(r"\d[\d,.]*\d|\d", text))


def compile_pages(path):
    tect = os.path.join(CV, "tectonic")
    if not os.path.exists(tect):
        tect = "tectonic"
    d = os.path.dirname(os.path.abspath(path))
    r = subprocess.run([tect, os.path.basename(path)], cwd=d, capture_output=True, text=True)
    if r.returncode:
        return None, (r.stderr or r.stdout)[-600:]
    pdf = os.path.splitext(os.path.abspath(path))[0] + ".pdf"
    info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", info)
    return (int(m.group(1)) if m else None), None


def audit(path, forb, alias, corpus, do_compile):
    tex = open(path, encoding="utf-8").read()
    body = strip_comments(tex.split("\\begin{document}", 1)[-1])
    ptxt = plain(tex.split("\\begin{document}", 1)[-1])
    head, f = header(tex)
    out = []
    add = lambda sev, check, msg="": out.append((sev, check, msg))

    # 1 spec header contract
    is_base = os.path.basename(path) in ("kien-swe.tex", "kien-devops.tex")
    has = lambda *pre: any(k.startswith(pre) for k in f)
    checks = {"url": "http" in head, "keywords": has("keywords", "jd hits"), "gaps": has("gaps"),
              "cut order": "cut in this order" in head.lower() or has("cut order")}
    for key, ok in checks.items():
        if is_base and key != "cut order":
            continue
        add("PASS" if ok else "WARN", f"header:{key}", "" if ok else "missing in header comment (see assets/header.tex)")

    # 2 placeholders
    phs = re.findall(r"\\ph\{([^}]*)\}", body)
    add("FAIL" if phs else "PASS", "placeholders", ", ".join(phs))

    # 3 format
    add("PASS" if "tgtermes" in tex else "FAIL", "font:tgtermes")
    add("PASS" if re.search(r"documentclass\[[^\]]*10pt", tex) else "WARN", "font:10pt")
    add("PASS" if not re.search(r"\\includegraphics|\\phototrue", tex) else "FAIL", "no photo")

    # 4 forbidden claims
    for rx, sev, why in forb:
        for m in rx.finditer(body):
            ln = body[: m.start()].count("\n") + 1
            add(sev, "claim", f"L{ln} '{m.group(0)[:40]}' : {why}")

    # 5 gaps must not appear
    gaps = split_terms(next((f[k] for k in f if k.startswith("gaps")), ""))
    for g in gaps:
        g2 = re.sub(r"\(.*?\)", "", g).strip()
        if len(g2) > 1 and re.search(r"(?<![a-z])" + re.escape(g2.lower()) + r"(?![a-z])", ptxt):
            add("WARN", "gap-in-body", f"'{g2}' appears in body; allowed only as 'learning' or '-compatible'")

    # 6 ATS keyword coverage
    kws = split_terms(f.get("keywords", "") or f.get("jd hits", ""))
    kws = [re.sub(r"\(.*?\)", "", k).strip() for k in kws]
    kws = [k for k in kws if k]
    if kws:
        miss = []
        for k in kws:
            kl = k.lower()
            cands = {kl, *alias.get(kl, [])}
            for ak, av in alias.items():
                if re.search(r"(?<![a-z.])" + re.escape(ak) + r"(?![a-z])", kl):
                    cands.update(av)
            if not any(re.search(r"(?<![a-z])" + re.escape(c) + r"(?![a-z])", ptxt) for c in cands):
                miss.append(k)
        pct = round(100 * (len(kws) - len(miss)) / len(kws))
        add("PASS" if pct >= ATS_TARGET else "WARN", f"ats:{pct}%", ("missing: " + ", ".join(miss)) if miss else "")
    else:
        add("WARN", "ats", "no 'Keywords:' line in header, cannot score")

    # 7 numbers must exist in fact sources
    skip = {"2023", "2024", "2025", "2026", "2027", "84", "924", "244", "510", "05", "19", "1"}
    unknown = sorted(n for n in numbers(ptxt) if n not in skip and len(n) >= 2 and n not in corpus)
    add("WARN" if unknown else "PASS", "numbers", ("not in AUDIT/HANDOFF/base: " + ", ".join(unknown)) if unknown else "")

    # 8 bullets per block
    for i, blk in enumerate(re.findall(r"\\begin\{itemize\}(?!\[label=\{\}\])(.*?)\\end\{itemize\}", body, re.S)):
        n = blk.count("\\item")
        if n > 5:
            add("WARN", "bullets", f"block {i+1} has {n} bullets (target 2 to 3, max 5)")

    # 9 compile + 1 page
    if do_compile:
        pages, err = compile_pages(path)
        if err:
            add("FAIL", "compile", err.strip().splitlines()[-1] if err.strip() else "error")
        else:
            add("PASS" if pages == 1 else "FAIL", f"pages:{pages}", "" if pages == 1 else "ONE PAGE STRICT, apply header cut order")
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    do_compile = "--no-compile" not in sys.argv
    as_json = "--json" in sys.argv
    if not args:
        print(__doc__); sys.exit(2)
    forb, alias = load_rules()
    corpus = fact_corpus()
    worst = 0
    report = {}
    for p in args:
        res = audit(p, forb, alias, corpus, do_compile)
        report[p] = res
        fails = [r for r in res if r[0] == "FAIL"]
        worst = max(worst, 1 if fails else 0)
        if not as_json:
            print(f"\n== {p}  ({'FAIL' if fails else 'OK'}: {len(fails)} fail, {sum(r[0]=='WARN' for r in res)} warn)")
            for sev, chk, msg in res:
                if sev != "PASS" or chk.startswith(("ats", "pages")):
                    print(f"  {sev:4} {chk:14} {msg}")
    if as_json:
        print(json.dumps(report, indent=1))
    sys.exit(worst)


if __name__ == "__main__":
    main()
