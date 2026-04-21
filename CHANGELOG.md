# Change log

## Version 21.0.0 (2026-04-21)
- feat: add local development automation with a branding-aligned `Makefile` and pinned dev requirements
- feat: replace legacy CI with branding-style GitHub Actions test and publish workflows
- ref: simplify `pyproject.toml` packaging metadata for modern hatch builds
- breaking: require Python 3.11 or newer
- chore: ignore generated Tutor `config.yml` and `env/` artifacts from local test runs
- chore: Upgrade Tutor compatibility to Ulmo (`>=21.0.0,<22.0.0`).
- chore: Refresh development requirements to `tutor==21.0.2`.

## Version 20.0.0 (2026-03-17)
- chore: Upgrade Tutor compatibility to Teak (`>=20.0.0,<21.0.0`).
- fix: Pin `openedx-webhooks==20.0.0` from the package version to avoid version drift.
- ci: Add a wheel install and plugin import smoke test.

## Version 19.0.1 (2025-05-08)
- fix: Set webhook app version to 19.0.1. Fix signal argument names.

## Version 19.0.0 (2025-04-28)
- chore: Update dependencies for Sumac

## Version 18.0.0 (2025-04-22)
- First release, Redwood
