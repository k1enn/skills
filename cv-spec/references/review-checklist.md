# Review checklist (run after `audit.py` is clean)

Play 3 rounds as the TA from AUDIT-2026-09-21.md section 4. Each item PASS or FAIL with the line quoted. Fix, rerun audit.py, repeat until a round has 0 FAIL.

## Round 1: truth
- Every number traces to AUDIT/HANDOFF/lab.md or the base file. `audit.py numbers` WARN list must be explained or removed.
- No gap term promoted into a skill or bullet. Gap list in header matches what is absent in body.
- No tool claimed above its real level (see claims.md "Never claim").
- Cross-file consistency: Java university level, MongoDB real (An Binh), Postgres/Redis/Kafka absent or study, same titles and dates as base.
- Nothing in the fork that the base does not support: new projects, new metrics, new dates = FAIL.

## Round 2: spec fit (JD as the spec)
- Summary: 1 to 2 sentences, names the JD title, JD stack, years (1 year production), graduation Jun 2027. No buzzwords.
- Skills: JD terms first, grouped, only JD-relevant, under 5 lines. Renamed per claims.md.
- Each role: 2 to 3 bullets (CTLD max 5), "did X using Y, resulting in Z", 1 JD keyword per bullet where honest.
- ATS score from audit.py between 80 and 90. Above 90 usually means keyword stuffing, reread.
- Project order: the project that proves the JD's main stack comes first.
- Cut order in header names real bullets of this file, so a 2 page fork can be fixed without rereading.

## Round 3: format (Sistilli checklist)
- 1 page, 10pt tgtermes, single column, no photo, consistent sizes. `audit.py pages:1` PASS.
- Header: name, city, phone, email, LinkedIn, GitHub, site. Untouched from base.
- Dates right aligned and unambiguous. Links only to public things (anbinhhotel.com, solitar.link, k1en.me blog).
- Grammar B2 level, no jargon without a number next to it. No `\ph{}` left.
- Vietnamese forks (`-vi.tex`): same facts, numbers may use `.`/`,` VN style; audit.py numbers WARN is expected there.

## Record
Add or update the row in the track's job table: `~/cv/APPLY.md` or `~/cv/LIVE-JOBS.md` (SWE), `~/cv/devops/DEVOPS-JOBS.md` (DevOps): company, role, where, CV file, link, deadline, gaps. Never run git commit.
