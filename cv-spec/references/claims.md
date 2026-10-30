# Claims ledger (what may go on a kien-*.tex)

Sources of truth, in priority order. Read before writing any bullet:
1. `~/cv/AUDIT-2026-09-21.md` sections 1 to 3: every number, date, team size, with evidence.
2. `~/cv/HANDOFF.md` "MoMo note" + "21 Sep pass 2": cross-file consistency rules, number fixes, Oct 2026 additions (OpenSSF 8.2/10, release-please).
3. `~/cv/lab.md`: homelab, proven vs NOT proven list.
4. Memory `cv-format-rules.md`, `agile-facts.md`: user-approved renames and real tools.
5. Base files `~/cv/kien-swe.tex`, `~/cv/devops/kien-devops.tex`: already audited wording. A fork may only reword, reorder, cut.

## Rename rules (real work -> JD vocabulary), machine copy in `scripts/aliases.txt`
Hono/Elysia/Express -> Node.js. D1 -> SQLite/SQL. Drizzle -> ORM. Workers -> serverless. Vitest -> unit testing (Jest-compatible). GitHub Actions -> CI/CD. REST -> RESTful APIs. Ansible -> configuration management / IaC. kubeadm lab -> Kubernetes. Docker -> containers. R2 -> S3-compatible object storage.
AWS: any Cloudflare or AWS service the JD names may sit in the skills line. Experience bullets stay true: prod = Cloudflare; AWS = workshop/lab only (EC2, API Gateway, S3, Route 53, Terraform).
Real, may list: Redux, MySQL, Figma, Claude Code, Search Console/Analytics, GoDaddy/DNS, Prometheus + Grafana (homelab), Jenkins (host installed, never "pipelines built"), Agile (Scrum weekly sprints, standups, retros; Kanban on ClickUp; GitHub Issues).

## Never claim, machine copy in `scripts/forbidden.txt`
Jenkins pipelines, Helm, Nginx, ArgoCD/GitOps, on-call, Prometheus alerting rules, Terraform or AWS in prod, Jira/Trello, any cert, coverage %, Lighthouse after-score, homelab NodePort/2nd worker/app deploy, C, Spring (only "learning"), Kafka/Oracle/Redis/Postgres (study level or absent), Java above university level.
Stale numbers: 411 tests, 890 commits, 75k LOC, 205 endpoints, 44 migrations, 47 pages, 200M rows/day, 50k queries/day, HRM Mar 2026.

## Fixed facts
- Name, contact, links: copy header block from base, never edit.
- Titles: CTLD Software Engineer Aug to Oct 2025, Team Lead Oct 2025 to present (user choice 21 Oct 2026). Never "sole developer" at CTLD; write "joined as the only developer", team of 5, 73% of 2,300+ commits, 340+ PRs.
- Education: HUFLIT B.Sc. SE, Aug 2023 to Jun 2027 expected. No GPA line.
- An Binh Hotel: paid client, Aug 2025 to Jun 2026, React 19 + Vite, Lighthouse baseline 72 / LCP 6.2s, 3 root causes, no after score.
- Friday rule: SWE track cannot work Friday, DevOps track any schedule. Never written on the CV, raise at offer stage.
- Commit share counts dinhtrungkien05 + k1enn only.
