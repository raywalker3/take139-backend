TAKE 139 BACKEND — SESSION 6 DEPLOY (Walkthrough PDFs)
========================================================

Adds the Walkthrough PDF generation system. Two flavors:

  PERSONAL  — 25-page PDF for each submission, voice of Tim Keller
              (sent to user automatically as email attachment on /submit)

  COUPLES   — 25-page PDF for each paired bond, includes 6-round date night
              (sent to both partners as email attachment on /pair/connect)

  FALLBACK  — graceful "Your walkthrough is being prepared" PDF for any
              profile/pair combination we haven't written yet
              (so users always get SOMETHING, never an error)

CURRENTLY WRITTEN:
  Personal:  1 of 36  (Architect + Attorney — Chris's profile)
  Couples:   1 of 15  (Architect + Island — Chris + Carolyn pattern)

The other 49 are stub fallbacks until we write them.

DEPENDS ON: Sessions 3, 4, 5 (admin, gating, Stripe — all live).

FILES IN THIS ZIP:
  main.py                                  — modified (2 new endpoints, walkthrough hooks)
  email_service.py                         — modified (new send_couples_walkthrough)
  walkthroughs/__init__.py                 — NEW package exports
  walkthroughs/api.py                      — NEW dispatch + registry
  walkthroughs/base.py                     — NEW shared infra (fonts, palette, helpers)
  walkthroughs/fallback.py                 — NEW "being prepared" PDFs
  walkthroughs/personal/__init__.py        — NEW registry
  walkthroughs/personal/architect_attorney.py  — NEW (Chris's profile)
  walkthroughs/couples/__init__.py         — NEW registry
  walkthroughs/couples/architect_island.py — NEW (Chris+Carolyn pattern)

NEW PUBLIC ENDPOINTS:
  GET /walkthrough/personal/{pair_code}
     Returns the personal Walkthrough PDF as application/pdf.
     Available to anyone holding the pair code (their own data).

  GET /walkthrough/couples/{pair_code_a}/{pair_code_b}
     Returns the couples Walkthrough PDF.
     Requires the pair to already be bonded in CouplePair (returns 403 otherwise).

BEHAVIORAL CHANGES:
  POST /submit       — now ALSO emails the personal Walkthrough PDF
                       to the user (as a second attachment).
  POST /pair/connect — now ALSO emails the couples Walkthrough PDF
                       to BOTH partners (using emails on file from
                       their original submissions).

DEPLOY STEPS (terminal):
  1. cd ~/take139-backend
  2. mv ~/Downloads/take139-backend-session6-walkthroughs-may20.zip .
  3. unzip -o take139-backend-session6-walkthroughs-may20.zip
  4. cp -R take139-backend-session6-walkthroughs-may20/* .
  5. rm -rf take139-backend-session6-walkthroughs-may20*
  6. git add main.py email_service.py walkthroughs/
  7. git commit -m "Session 6: Walkthrough PDF generation system (personal + couples)"
  8. git push

Railway auto-deploys. Build will take a bit longer than usual the first time
(fonts download on cold start). Subsequent requests use cached fonts in /tmp.

POST-DEPLOY VERIFICATION:
  After deploy, hit your existing pair code:
    https://take139-backend-production.up.railway.app/walkthrough/personal/STEADFAST-4342
  (Replace STEADFAST-4342 with one of your real pair codes from /admin)
  Should return a PDF (browser will offer to view or download).

  If the profile is Architect+Attorney, you get the full walkthrough.
  Any other profile gets the "preparing" fallback.

WRITING MORE WALKTHROUGHS:
  Each new personal walkthrough is a new file in walkthroughs/personal/,
  exposing a build(submission) function, then added to PERSONAL_REGISTRY
  in walkthroughs/personal/__init__.py.

  Same pattern for couples in walkthroughs/couples/.

  The shared base.py handles all design/typography/page setup. New
  walkthroughs only contain the prose + page composition.
