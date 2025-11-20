#!/usr/bin/env python3
"""
Generate a batch of diverse synthetic DOT graph examples.
Runs in background to produce 50+ pairs while FSM extraction happens.
"""

import subprocess
import json
from pathlib import Path
import time

# Diverse graph type prompts
prompts = [
    # FSM / State Machines (10)
    "User authentication flow (idle, logging_in, authenticated, logging_out, logged_out)",
    "HTTP request lifecycle (pending, sending, sent, receiving, received, error)",
    "Order processing (placed, confirmed, preparing, shipped, delivered, cancelled)",
    "Video player states (stopped, playing, paused, buffering, ended)",
    "Connection states (disconnected, connecting, connected, reconnecting, failed)",
    "Game character states (idle, walking, running, jumping, attacking, dead)",
    "Database transaction (begin, active, committing, committed, rolling_back, rolled_back)",
    "WebSocket connection (closed, connecting, open, closing, error)",
    "File upload (queued, uploading, processing, complete, failed)",
    "Payment processing (initiated, authorizing, authorized, capturing, captured, refunded)",
    
    # Workflows (10)
    "CI/CD pipeline (build → test → deploy → verify)",
    "Code review process (submitted → reviewing → approved → merged)",
    "Bug triage workflow (reported → triaged → assigned → in_progress → resolved → closed)",
    "Content publishing (draft → review → approved → published → archived)",
    "Employee onboarding (application → interview → offer → hired → training → active)",
    "Customer support ticket (open → assigned → investigating → resolved → closed)",
    "Invoice processing (received → validated → approved → paid → archived)",
    "Release management (development → staging → production → rollback)",
    "Data pipeline (extract → transform → validate → load → archive)",
    "Incident response (detected → investigating → mitigating → resolved → postmortem)",
    
    # Network/Architecture (10)
    "Microservices architecture (API Gateway → Auth Service → User Service → Database)",
    "Load balancer → Web Servers → Application Servers → Database cluster",
    "CDN → Origin Server → Cache Layer → Backend API",
    "Client → Proxy → Firewall → Application Server → Database",
    "Message Queue (Producer → Queue → Consumer → Result Store)",
    "Event-driven architecture (Event Source → Event Bus → Handlers → Storage)",
    "3-tier web app (Presentation → Business Logic → Data Access → Database)",
    "Distributed cache (Client → Cache Nodes → Database fallback)",
    "Service mesh (Services with sidecars and control plane)",
    "Data replication (Primary → Replicas with bidirectional sync)",
    
    # Dependencies (10)
    "Python package dependencies (numpy, pandas, scikit-learn, matplotlib)",
    "JavaScript module imports (React → ReactDOM, hooks, components)",
    "Build system dependencies (source → compile → link → test → package)",
    "Library dependency tree (core → utils → features → plugins)",
    "Microservice dependencies (auth-service, user-service, notification-service, payment-service)",
    "Docker image layers (base → runtime → dependencies → application → config)",
    "Database schema dependencies (users → posts → comments → likes)",
    "CSS framework dependencies (reset → base → components → utilities → themes)",
    "API versioning dependencies (v1 → v2 → v3 with deprecation paths)",
    "Feature flags dependency graph (base-features → experimental → beta → stable)",
    
    # Decision Trees (10)
    "User permission check (is_authenticated? → is_admin? → has_permission? → grant/deny)",
    "Error handling (try → success/error → retry? → log/escalate)",
    "Caching decision (in_cache? → valid? → return/fetch → update_cache)",
    "Request routing (path match? → method match? → auth check? → route to handler)",
    "Data validation (type_check → range_check → format_check → pass/fail)",
    "Search algorithm (exact_match? → fuzzy_match? → semantic_search → no_results)",
    "Pricing tier selection (usage → tier1/tier2/tier3/enterprise → calculate price)",
    "Feature availability (user_tier → region → device → enable/disable feature)",
    "Content moderation (scan → flagged? → review → approve/reject/escalate)",
    "Load shedding (load > threshold? → priority check → accept/reject/queue)",
]

print(f"Starting batch generation of {len(prompts)} synthetic pairs...")
print("This will run using the existing synthetic generator with Gemini...")

output_dir = Path("data/synthetic_batch")
output_dir.mkdir(exist_ok=True)

results = []
for i, prompt in enumerate(prompts):
    print(f"\n[{i+1}/{len(prompts)}] Generating: {prompt[:60]}...")
    
    # Use existing generator (modify as needed)
    # For now, just create placeholder structure
    result = {
        "id": f"synthetic_batch_{i:03d}",
        "prompt": prompt,
        "status": "queued",
        "timestamp": time.time()
    }
    results.append(result)
    
    # TODO: Actually call Gemini API here
    # For now, just track what we want to generate
    
print(f"\n✓ Queued {len(results)} synthetic pairs for generation")
print(f"  Output directory: {output_dir}")

# Save queue
with open(output_dir / "generation_queue.json", 'w') as f:
    json.dump(results, f, indent=2)

print("\nNOTE: This is a placeholder. To actually generate:")
print("  1. Implement Gemini API calls in this script")
print("  2. Or run existing generators/synthetic_diverse.py with these prompts")
