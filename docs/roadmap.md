# Project Roadmap: Cuisinise

## Overview
This document summarizes the major phases we followed to build the Cuisinise platform and outlines next steps for containerization and deployment. It references concrete code paths so contributors can trace decisions to implementation.

mermaid
flowchart LR
  subgraph Frontend [frontend/]
    UI[React App]
  end

  subgraph Backend [backend/]
    API[Express API]
    DB[(Database)]
  end

  subgraph Coordinator [coordinator/]
    COORD[Coordinator Service]
  end

  subgraph Agents [agents/]
    A1[cuisine_classifier]
    A2[menu_analyzer]
    A3[recipe_recommender]
    A4[restaurant_finder]
  end

  UI <--> API
  API <--> COORD
  COORD <--> A1
  COORD <--> A2
  COORD <--> A3
  COORD <--> A4
  API <--> DB


## Phase 1 — Developing Each Agent (agents/)
- *Goal*: Implement focused services for classification, menu analysis, recommendations, and restaurant discovery.
- *Structure*: Each agent kept self-contained data, models, and entrypoints.

- **agents/cuisine_classifier/**
  - *Key files*: cuisine_api.py, model artifacts (*.pkl), helper *.py modules.
  - *Outcome*: Exposed a simple API to classify cuisine types from text input.

- **agents/menu_analyzer/**
  - *Key files*: main.py, additional *.py utilities, input CSVs.
  - *Outcome*: Parsed and analyzed menus, extracting dish features and signals.

- **agents/recipe_recommender/**
  - *Key files*: models.py, other *.py modules.
  - *Outcome*: Produced recipe suggestions based on cuisine, ingredients, and user context.

- **agents/restaurant_finder/**
  - *Key files*: multiple *.py files for querying and ranking restaurants.
  - *Outcome*: Located and ranked restaurants relevant to user preferences and geography.

- *Cross-agent standards*
  - *Consistency*: Shared conventions for logging, error handling, and I/O contracts.
  - *Reproducibility*: Pinned dependencies in requirements.txt and provided enviroment.yml for Conda.

## Phase 2 — Developing the Coordinator (coordinator/)
- *Goal*: Orchestrate workflows across agents, provide a unified interface to the backend.
- *Structure*: Modular src/ with clearly defined client interfaces.
- *Key files*:
  - coordinator/src/__init__.py
  - coordinator/src/service_clients.py for agent/service clients
  - Other orchestration modules under coordinator/src/
- *Outcome*: Centralized routing and aggregation of agent outputs for API consumption.

## Phase 3 — Developing the Backend (backend/)
- *Goal*: Provide a REST API to the frontend, manage auth, chat context, and data persistence.
- *Stack*: Node.js/Express.
- *Key directories*:
  - backend/routes/ — authRoutes.js, chatRoutes.js
  - backend/models/ — User.js, Chat.js, Message.js
  - backend/middleware/ — auth.js
- *Outcome*: Authenticated endpoints to initiate coordinator flows and persist conversations.

## Phase 4 — Developing the Frontend (frontend/)
- *Goal*: Build a responsive React UI that interacts with the backend and showcases agent capabilities.
- *Structure*:
  - frontend/public/ — static assets and index.html
  - frontend/src/ — components, contexts, styles, and app bootstrapping
- *Outcome*: Users can sign in, chat/query, and view results produced by orchestrated agents.

## Phase 5 — Dockerization (Planned)
- *Goal*: Containerize services for consistent environments and simpler deployment.
- *Plan*:
  - *Agents*: Base Python image, copy code, install requirements.txt, expose service ports per agent.
  - *Coordinator*: Python image with the same dependency pins as agents; network with agents.
  - *Backend*: Node image, install dependencies, run production server.
  - *Frontend*: Node builder image to generate static build; serve via lightweight web server (e.g., nginx).
  - *Composition*: Introduce a docker-compose.yml to define service topology and networks.
- *Notes*: No Dockerfiles are committed yet; this phase captures the agreed approach before implementation.

## Phase 6 — Deployment (Planned)
- *Goal*: Provide reproducible CI/CD to staging and production.
- *Plan*:
  - *Registry*: Push images to a container registry (e.g., GHCR/ACR/ECR).
  - *Orchestration*: Deploy via a managed service (e.g., ECS, ACI, Kubernetes, or Docker Swarm) or PaaS alternatives for smaller scale.
  - *Frontend hosting*: Static hosting (e.g., Netlify/Vercel/S3+CloudFront) consuming the backend API.
  - *Secrets*: Manage via platform secret stores; never commit keys.
  - *CI/CD*: Add workflows to build, test, scan, and deploy on main branch merges.
- *Notes*: Concrete provider selection and infra code (IaC) will be added with this phase.

## Timeline Snapshot
- *1. Agents*: Implemented core logic and interfaces in agents/.
- *2. Coordinator*: Established orchestration in coordinator/src/.
- *3. Backend*: Exposed routes and models in backend/.
- *4. Frontend*: Built React UI in frontend/.
- *5. Dockerization*: Planned container strategy; to be executed next.
- *6. Deployment*: Planned CI/CD and hosting strategy; to be executed after dockerization.

## References
- *Python env*: Root requirements.txt, enviroment.yml
- *Agents*: agents/
- *Coordinator*: coordinator/src/
- *Backend*: backend/
- *Frontend*: frontend/