# Requirements

Generated from `requirements.yaml`. Do not edit by hand.

| ID | Title | Priority | Source | Tags |
|---|---|---|---|---|
| REQ-001 | Signup entry point on the login page | High | QWA-2 | signup, ui |
| REQ-002 | Duplicate email is rejected on signup | High | QWA-2 | signup, ui, negative |
| REQ-003 | Account details page required fields | High | QWA-2 | signup, ui |
| REQ-004 | Company and Address2 are optional | High | QWA-2 | signup, ui |
| REQ-005 | Newsletter/offers checkboxes are optional | High | QWA-2 | signup, ui |
| REQ-006 | Successful signup logs the user in | High | QWA-2 | signup, ui |

## Details

### REQ-001 — Signup entry point on the login page

Given a user on /login with a unique name and email entered in the "New User Signup!" form, when they click Signup, then they are navigated to the account details page (/signup) with name and email carried over.

### REQ-002 — Duplicate email is rejected on signup

Given a user tries to sign up on /login with an email address that is already registered, when they submit, then an "Email Address already exist!" error is shown and the account details form ("Enter Account Information") is never reached. Corrected 2026-08-19 during test automation: the browser URL actually changes to /signup, but the server re-renders the login/signup page with the error there rather than the account details form — verified against the live site, the original "stays on /login" wording was an unverified assumption and turned out to be inaccurate about the URL.

### REQ-003 — Account details page required fields

The /signup account details form must include: Title (Mr/Mrs), Password, Date of birth (day/month/year dropdowns), and an address block (first name, last name, address, country, state, city, zipcode, mobile number). All of these are required for submission.

### REQ-004 — Company and Address2 are optional

Given the /signup form, the Company and Address2 fields are optional — account creation must succeed without them being filled.

### REQ-005 — Newsletter/offers checkboxes are optional

The "Sign up for our newsletter!" and "Receive special offers from our partners!" checkboxes are optional — account creation succeeds regardless of their checked state.

### REQ-006 — Successful signup logs the user in

Given all required /signup fields are filled correctly, when the user submits, then an "Account Created!" confirmation is shown; when they continue, they land on the home page already logged in (the header shows their logged-in state).

