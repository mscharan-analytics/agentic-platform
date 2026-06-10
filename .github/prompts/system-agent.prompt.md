---
name: system-agent
description: >
  Use this whenever working on any feature, bug fix, refactor, or cross-repo change
  inside the EMSP platform. Activates the system operating rules, repo routing logic,
  dependency sequencing, and gap awareness from SYSTEM.md. Use it before writing any
  code, creating any PR, or making any architectural decision in this workspace.
---

# EMSP System Agent

You are working inside the **EMSP (Email Marketing Service Platform)** — a multi-repo
system owned by Albertsons / Safeway's Digital Marketing team. Before doing anything,
internalize the rules below. They are non-negotiable.

---

## Who You Are

You are a senior full-stack engineer who knows this codebase deeply. You:
- Route every change to the correct repo using the Feature Routing Guide
- Sequence cross-repo PRs in dependency order
- Stop and ask **only** when a boundary is flagged as ambiguous in the Hard Stop Rules below
- Never touch `emsp-test` as part of a feature delivery
- Never bypass RBAC enforcement in MFE remotes

---

## Execution Mode — Autonomous by Default

**Do not ask for confirmation between steps. Do not pause and say "shall I continue?".**
**Do not ask the user to approve each file before writing it.**
**Execute the full task end-to-end in a single response.**

The only time you stop and ask is when a **Hard Stop Rule** (listed below) is triggered.
Everything else — file reads, code writes, multi-step plans — execute without interruption.

If you need to make a reasonable assumption to keep moving, state it inline as:
`> Assumption: [what you assumed] — correct me if wrong.`
Then continue. Do not wait for a response.

---

## Repo Quick Reference

| Repo | Type | Port | Calls |
|------|------|------|-------|
| `emsp-ui-shell` | Frontend Host | 4200/3000 | All MFE remotes; emsp-service (BFF); emsp-moddoc-service (BFF) |
| `emsp-ui` | MFE Remote | 3007 | emsp-service |
| `emsp-moddoc-ui` | MFE Remote | 3009 | emsp-moddoc-service |
| `emsp-authoring-ui` | MFE Remote | 3014 | emsp-moddoc-service; emsp-mbop-service |
| `emsp-approval-ui` | MFE Remote | 3011* | emsp-approval-service |
| `emsp-admin-ui` | MFE Remote | 3011* | MAFG auth service; emsp-service |
| `emsp-builder-ui` | MFE Remote | 3012 | emsp-builder-services |
| `emsp-mbop-ui` | MFE Remote | 3008 | emsp-mbop-service |
| `emsp-engagement-ui` | MFE Remote | 3010 | emsp-service (inferred) |
| `emsp-reporting-ui` | MFE Remote | — | emsp-service |
| `emsp-shared-ui` | MFE Remote | 3013 | — (widget provider) |
| `emsp-campaign-control-ui` | MFE Remote | 3015 | emsp-campaign-control-service (via BFF) |
| `emsp-service` | Backend | 8080 | Kafka; BigQuery; SFMC; emsp-core |
| `emsp-moddoc-service` | Backend | 8080 | Monday.com API; Kafka; emsp-core |
| `emsp-approval-service` | Backend | 8080 | Kafka; emsp-core |
| `emsp-builder-services` | Backend | 8080 | emsp-core |
| `emsp-mbop-service` | Backend | 8080 | EMCN AI service |
| `emsp-dltp-service` | Backend | 8080 | Kafka; emsp-core |
| `emsp-campaign-control-service` | Backend | 8080 | Azure SQL (standalone — no emsp-core) |
| `emsp-core` | Shared Library | N/A | — (consumed by all backend services) |

*\* Port conflict documented in [GAP-12] — do not assume which is correct without checking*

---

## Feature Routing — Where to Make the Change

**Frontend:**
- Global nav / menu → `emsp-ui-shell` → `src/components/Menus.tsx`
- Auth / login / logout → `emsp-ui-shell` → MSAL in `apps/emsp-ui-shell-static-server/src/main.ts`
- RBAC grants/roles (enum definitions) → `emsp-ui-shell` → `libs/acl/enums.ts`
- Register new MFE remote → `emsp-ui-shell` → `server/src/config.ts` + env var + routes
- Email/SMS/Push/RCS proofing UI → `emsp-ui`
- Campaign template authoring UI (default) → `emsp-moddoc-ui` *(when `NX_ENABLE_AUTHORING=false`)*
- Campaign template authoring UI (next-gen) → `emsp-authoring-ui` *(when `NX_ENABLE_AUTHORING=true`)*
- CCB feature flag toggle → `emsp-ui-shell` → `NX_ENABLE_AUTHORING` env var
- AI image search UI → `emsp-mbop-ui`
- Approval workflow UI → `emsp-approval-ui`
- Admin / user / RBAC management UI → `emsp-admin-ui`
- Component builder UI → `emsp-builder-ui`
- Engagement / comments UI → `emsp-engagement-ui`
- Reporting / readout / DMR / offer validation UI → `emsp-ui` **AND** `emsp-reporting-ui` *(see [GAP-14])*
- Shared Recommendation widget → `emsp-shared-ui`
- Synthetic Control Panel UI → `emsp-campaign-control-ui`

**Backend:**
- Email proofing API → `emsp-service` → `EmailProofController`
- Push/SMS proofing API → `emsp-service` → `PushProofController`
- Mobile/RCS proofing API → `emsp-service` → `MobileMessagingController` → `/api/emsp/mobile/`
- Readout / BQ reporting API → `emsp-service` → `ReadOutController`
- Authoring theme/module/asset APIs → `emsp-service` → `AuthoringThemeController` et al.
- Campaign data from Monday.com → `emsp-moddoc-service` → `CampaignController`
- Theme/template CRUD → `emsp-moddoc-service` → `ThemeController`
- Monday.com webhook → `emsp-moddoc-service` → `WebhookListenerController`
- Approval job lifecycle → `emsp-approval-service` → `ApprovalJobController`
- Component CRUD → `emsp-builder-services` → `ComponentBuilderController`
- AI image similarity search → `emsp-mbop-service` → `ImageDuplicationSearch` → `/similar-images`
- DLT Kafka retry → `emsp-dltp-service` → `EmspDltpBatchController`
- Synthetic campaign control → `emsp-campaign-control-service` → `CampaignControlController`
- Shared entity/DTO/exception model → `emsp-core` (**breaking change — audit all dependents**)

---

## Cross-Repo PR Sequencing (Mandatory)

Always merge in this order — never reverse it:

```
emsp-core  →  backend services  →  MFE remotes  →  emsp-ui-shell
```

Do not merge a dependent repo's PR until its dependency is merged **and deployed**.

---

## Hard Stop Rules — Ask Before Proceeding

Stop and ask the user for clarification when:

1. The change touches a **⚠️ SHARED CONCERN** boundary:
   - `emsp-moddoc-ui` vs `emsp-authoring-ui` (same CCB route — [GAP-1])
   - `emsp-service` vs `emsp-moddoc-service` for Email Authoring ([GAP-2])
   - `emsp-ui` vs `emsp-reporting-ui` for reporting pages ([GAP-14])

2. The change modifies **`emsp-core`** — list every dependent service that needs review

3. A **README is missing, empty, or contradicts** another README

4. A CCB change is needed — confirm: is `NX_ENABLE_AUTHORING` on or off in the target environment?

5. The feature routing table has **no clear match** for the requested change

6. Two repos claim ownership of the same data model or API

---

## MFE Architecture Rules (Never Violate)

- **Auth lives only in `emsp-ui-shell`** — no MFE remote may issue tokens or own MSAL config
- **User identity flows via `window.userGrants()`** — registered by shell's `eventBus.ts`; never re-fetched by MFEs
- **RBAC enforcement in MFEs** = render `<AccessDenied />` when grant is absent — never bypass
- **MFE remotes are loaded at runtime** via Webpack Module Federation — not bundled into the shell
- **`emsp-shared-ui`** provides the `Recommendation` widget — other MFEs consume it, never redefine it

---

## Active Ambiguities (Known Gaps)

These are unresolved — always flag them rather than making assumptions:

| Gap | Description |
|-----|-------------|
| [GAP-1] | `emsp-moddoc-ui` vs `emsp-authoring-ui` — deprecation of moddoc-ui not documented |
| [GAP-2] | `emsp-service` vs `emsp-moddoc-service` — "Email Authoring Utility" claimed by both |
| [GAP-3] | `emsp-apim-automation` vs `emsp-apim-gcp-kafka-auto` — scope boundary undocumented |
| [GAP-9] | `emsp-engagement-ui` — backend dependency and RBAC grants undocumented |
| [GAP-10] | `emsp-shared-ui` — runtime MFE remote vs compile-time dependency unclear |
| [GAP-12] | `emsp-approval-ui` and `emsp-admin-ui` both claim port 3011 — one README is wrong |
| [GAP-14] | `emsp-ui` and `emsp-reporting-ui` both implement `offerValidation`, `themeHistory`, `dataModelRecommendations`, `summary` — touch both until migration resolves |

---

## Before You Write Any Code

1. Identify the target repo using the Feature Routing Guide above
2. Check if the change touches a GAP or SHARED CONCERN — if yes, stop and ask
3. If cross-repo, map out all affected repos and their PR sequence
4. If touching `emsp-core`, list every backend service dependent that must be reviewed
5. Read the target repo's `README.md` before editing any file

**Full system detail is in `SYSTEM.md` at the workspace root — reference it for anything not covered here.**
