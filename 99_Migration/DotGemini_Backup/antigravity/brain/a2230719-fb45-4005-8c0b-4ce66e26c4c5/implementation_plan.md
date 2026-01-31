# GENESIS v5 - Implementation Plan

## Goal
To build "GENESIS," an autonomous business ecosystem powered by a Python-based "Brain" on Google Cloud Run. The system will autonomously generate, deploy, and analyze Micro-SaaS ventures based on directives in GitHub Markdown files.

## User Review Required
> [!IMPORTANT]
> **Architecture Pivot**: We have shifted from a Next.js Web App to a Python-based Autonomous Agent.
> **Infrastructure**: This requires a Google Cloud Platform (GCP) project with Billing enabled.

## Proposed Architecture: "The Autonomous Core" (Dual Brain)
- **Brain (Planning & Chat)**: **Gemini 2.5 Flash** (`gemini-2.5-flash`)
    - Role: Understands user directives, plans tasks, and updates reports.
- **Hands (Execution)**: **Gemini 2.5 Flash** (`gemini-2.5-flash`)
    - Role: Writes code, executes builds, and analyzes data.
- **Interface**: GitHub Repository (Markdown files).
- **Auth**: Google AI Studio API Key (Environment Variable).

## Phase 1: The Foundation (Genesis Brain)
We will build the core agent that listens to GitHub and executes commands.
- [ ] **Repo Setup**: Create `genesis-monorepo` with `commands`, `reports`, `projects` structure.
- [ ] **GCP Setup**: Enable APIs (Run, Build, VertexAI) and setup Workload Identity.
- [ ] **Brain Implementation**:
    - `main.py`: FastAPI webhook handler.
    - `agents/brain.py`: Logic to plan tasks using Gemini 2.5 Flash.
    - `agents/hands.py`: Logic to generate code using Gemini 2.5 Flash.
    - `agents/github.py`: [NEW] Logic to commit files to GitHub using PyGithub.
    - `ops/deploy.py`: Logic to trigger Cloud Build.
- [ ] **Deployment**: Deploy the Brain to Cloud Run with `GITHUB_TOKEN`.

## Phase 2: The First Experiment (Pilot)
We will test the system by ordering it to build a simple tool.
- [ ] **Directive**: Write `[ ] Create: Readme-AI` in `user_directives.md`.
- [ ] **Execution**: Verify Genesis generates code, commits it, and deploys it.
- [ ] **Verification**: Check the deployed URL and GA4 data connection.

## Verification Plan
### Automated Tests
- **Unit Tests**: `pytest` for the Brain's logic (parsing markdown, calling mock GCP APIs).

### Manual Verification
- **E2E Flow**:
    1. User updates `user_directives.md`.
    2. GitHub Webhook triggers Cloud Run.
    3. Cloud Run commits new code to `projects/`.
    4. Cloud Build deploys the new project.
    5. User sees `[x] Deployed` in `reports/status.md`.
