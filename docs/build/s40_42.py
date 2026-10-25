# -*- coding: utf-8 -*-
"""Sections 40-42: Comprehensive Project Execution Walkthrough,
Core Routing & Optimization Algorithms Deep Dive, and Complete Project Defense Playbook.
"""
from style import bullets, callout, code, evidence, h, numbered, page_break, para, table


def section_40(doc):
    page_break(doc)
    h(doc, 1, "40. Comprehensive Project Architecture & End-to-End Execution Walkthrough")
    para(doc, "This section provides an exhaustive, step-by-step technical breakdown of the DBARS platform "
              "architecture for any student, developer, or examiner seeking complete codebase mastery from the ground up.")

    h(doc, 2, "40.1 System Architecture Blueprint")
    para(doc, "DBARS is structured as a strictly decoupled four-tier platform, enforcing a rigid one-way dependency rule:")
    code(doc,
         "  [Client Tier]              React 19 SPA (TypeScript 5.7, Vite 6, Leaflet, Recharts, Bento CSS)\n"
         "                                     |\n"
         "                                     v  HTTP / JSON with HMAC-SHA256 Bearer Token\n"
         "  [API Gateway & Router]     FastAPI 0.115 + Starlette (app/main.py, app/api/, app/auth/)\n"
         "                             - RateLimitMiddleware (120 req/min sliding window)\n"
         "                             - CORSMiddleware (strictly whitelisted origins)\n"
         "                             - Pydantic schema validation & sanitization\n"
         "                             - Depends(require_role) RBAC authorization chokepoints\n"
         "                                     |\n"
         "                   +-----------------+-----------------+\n"
         "                   |                                   |\n"
         "                   v                                   v\n"
         "  [State & Business Services]               [Pure Algorithmic Engines]\n"
         "  (app/services/, app/db/)                  (app/ml/, app/gtfs/, app/tracking/)\n"
         "  - waybill_service, alerts_service         - BMTCBusPredictor (predictor.py)\n"
         "  - Motor async MongoDB driver              - BlockingEngine (blocking.py)\n"
         "  - Users, Votes, Passes, Waybills          - CrewEngine (crew.py)\n"
         "                   |                        - GTFS Streaming Builder (builder.py)\n"
         "                   v                                   |\n"
         "  [MongoDB 7.0 Document Database]                      v\n"
         "  (14 operational collections)              [Physical Dataset Files on Disk]\n"
         "  * Optional: core engines bypass DB!       - routes_cleaned.csv (46,470 departures)\n"
         "                                            - stops_cleaned.csv (4,883 coordinates)\n"
         "                                            - bmtc_depots.xlsx (44 operating depots)",
         caption="Figure 40.1 - End-to-end multi-tier architectural data flow.")

    h(doc, 2, "40.2 Startup Sequence (Life of the Server)")
    para(doc, "When uvicorn starts the application (app.main:app), the lifespan(app: FastAPI) context manager "
              "executes in strict, deterministic order:")
    numbered(doc, [
        ("Step 1 (File Verification):", "Validates that routes_cleaned.csv, stops_cleaned.csv, bengaluru_metro_network.csv, "
         "and fares.json physically exist on disk. If any dataset file is missing, startup raises FileNotFoundError immediately."),
        ("Step 2 (Predictor Engine Initialization):", "Instantiates BMTCBusPredictor(settings.dataset_path, settings.artifact_dir) "
         "on app.state.predictor and triggers train(). In under 8 seconds, it parses 6,737 route-directions, normalizes 4,883 stop "
         "names, and constructs the 655,438 ordered stop-pair search index in RAM."),
        ("Step 3 (Asynchronous Blocking & Crew Warming):", "Spawns a background task (_warm_blocking_plan()) stored as a strong reference "
         "on app.state.blocking_warm_task. Precomputes the 13,850 -> 6,849 vehicle interlining plan across all 44 depots so the first "
         "depot manager request responds instantaneously."),
        ("Step 4 (GTFS Feed Generation):", "Spawns _warm_gtfs_feed() to adopt or stream the 1.46M stop_times static GTFS zip feed."),
        ("Step 5 (Vehicle Tracking Ingest):", "Initializes the simulated GPS telemetry tracking loop with 30 active buses."),
        ("Step 6 (Database Initialization):", "Calls init_db(). If MongoDB is online, establishes connection pool and seeds default "
         "admin/depot accounts. If MongoDB is offline, logs a warning and proceeds without crashing."),
    ])


def section_41(doc):
    page_break(doc)
    h(doc, 1, "41. Core Routing & Optimization Algorithms: Deep Dive & Formal Proofs")
    para(doc, "This section breaks down the computational mathematics, graph algorithms, and formal proofs that power "
              "the DBARS routing and fleet scheduling engines.")

    h(doc, 2, "41.1 Graph Vehicle Interlining & The Dilworth Fleet Floor")
    para(doc, "BMTC operates 46,470 scheduled trips per day. If scheduled in route isolation, 13,850 buses are required. "
              "DBARS models the timetable as a Minimum Path Cover problem on a Directed Acyclic Graph (DAG):")
    code(doc,
         "  Let G = (V, E) be a DAG where each vertex v_i in V represents a scheduled bus trip.\n"
         "  A directed edge (v_i, v_j) exists in E if and only if:\n"
         "      1. end_stop(v_i) == start_stop(v_j)  (compatible interchange terminal);\n"
         "      2. start_time(v_j) >= end_time(v_i) + layover_minutes (legal recovery buffer);\n"
         "      3. start_time(v_j) - end_time(v_i) <= max_idle_minutes (prevents terminal bloat); and\n"
         "      4. home_depot(v_i) == home_depot(v_j)  (buses return to their home depot at night).\n"
         "\n"
         "  Finding the minimum number of buses required to cover all trips is equivalent to finding\n"
         "  the minimum number of vertex-disjoint paths covering V. By Dilworth's Theorem, this equals\n"
         "  the maximum size of an antichain (the maximum number of pairwise unconnectable trips, which\n"
         "  corresponds to peak simultaneous trips running at the same minute across Bengaluru).\n"
         "\n"
         "  Measured Concurrency Peak: 5,723 simultaneous trips.\n"
         "  Interlined Fleet Scheduled: 6,849 buses across 44 depots.\n"
         "  Buses Released: 7,001 buses (51% fleet reduction!).",
         caption="Formal formulation of the vehicle blocking problem.")

    h(doc, 2, "41.2 The Walkable Interchange Transfer Filter")
    para(doc, "In earlier transit algorithms, 1-transfer routing allowed transfers between any two routes that shared a common stop name. "
              "However, stop names in large metropolitan areas are often assigned to broad neighborhoods (e.g. 'Yeshwanthpur'). "
              "DBARS introduces _interchange_is_walkable(leg1, leg2) which calculates the physical Haversine distance between the drop-off "
              "stop of leg 1 and the boarding stop of leg 2. If the interchange walking distance exceeds 1,200 meters (1.2 km), "
              "the transfer proposal is pruned immediately, protecting commuters from impossible physical changeovers.")


def section_42(doc):
    page_break(doc)
    h(doc, 1, "42. The Complete Project Defense Playbook & Codebase Mastery")
    para(doc, "This final section serves as the ultimate tactical defense manual for college vivas, final project reviews, "
              "and technical interviews.")

    h(doc, 2, "42.1 The Ten Defense Commandments")
    numbered(doc, [
        ("Never Claim Modern AI/LLMs in Route Search:", "Explain proudly that the route predictor is deterministic information retrieval "
         "and graph search. Deterministic search is faster (median 0.94s vs 15s LLM calls), costs zero API fees, and is provably immune "
         "to hallucinations."),
        ("Know the Core Numbers by Heart:", "6,737 routes, 4,883 stops, 44 depots, 46,470 departures, 13,850 baseline buses reduced to "
         "6,849 interlined buses (7,001 released), 5,723 concurrency floor."),
        ("Explain the Three Key Secret Domains:", "Know why JWT_SECRET_KEY, PASS_VERIFICATION_SECRET, and ticket keys are separate: "
         "cryptographic domain separation prevents an offline scanner vulnerability from compromising session auth."),
        ("Defend the CSV vs MongoDB Architecture:", "Engine separation means the core product survives total database outages. It also "
         "allowed writing 161 unit tests that run cleanly in CI without spinning up a heavy database container."),
        ("Explain the Offline Conductor Synchronization:", "Client-generated UUIDs + unique compound database indexes on (waybill_id, "
         "client_ticket_uuid) guarantee idempotency during network packet replays."),
        ("Acknowledge Project Weaknesses Openly:", "Highlight that frontend test automation is the clearest area for future work. "
         "Examiners respect candidates who know the limitations of their system far more than those who claim perfection."),
        ("Understand the Dilworth Fleet Floor:", "Be able to draw on a whiteboard: time on the x-axis, simultaneous trips on the y-axis, "
         "with peak concurrency at 5,723 buses."),
        ("Explain the Avalahalli Bug Resolution:", "Describe how two-pass anchored geometric resolution stopped 69 km route teleportation."),
        ("Detail the Shakti Scheme Audit:", "Explain how DBARS generates audit-ready zero-fare reports for Karnataka State Government reimbursement."),
        ("Articulate the GTFS Open Data Value:", "Show how static zip and real-time alert protobuf feeds connect BMTC with smart city transit ecosystems."),
    ])

    callout(doc, "Final Closing Defense Statement",
            "\"DBARS is not just a commuter journey planning website. It is a full-scale public transport platform that addresses "
            "both sides of urban mobility: commuter accessibility through fast, transparent multi-modal transit discovery, and operational "
            "sustainability through mathematically verified fleet and crew optimization on real-world open data.\"", warn=False)
