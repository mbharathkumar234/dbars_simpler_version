# -*- coding: utf-8 -*-
"""Builds the standalone Master Revision Sheet in super ultra detail."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.shared import Pt, Inches  # noqa: E402

import style  # noqa: E402
from style import (ACCENT, GREY, NAVY, bullets, callout, code, h, numbered,  # noqa: E402
                   page_break, para, table)


def _qa(doc, items):
    for i, (q, a) in enumerate(items, 1):
        p = doc.add_paragraph()
        r = p.add_run(f"{i}. {q}")
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = NAVY
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        p2 = doc.add_paragraph()
        r2 = p2.add_run(a)
        r2.font.size = Pt(9.5)
        p2.paragraph_format.space_after = Pt(6)
        p2.paragraph_format.left_indent = Inches(0.2)


def build():
    doc = style.new_document()

    # Title & Subtitle
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("DBARS - MASTER REVISION SHEET")
    r.font.size = Pt(24); r.bold = True; r.font.color.rgb = NAVY
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Demand Based Bus Allocation & Routing System   |   Complete Super Ultra Detailed Project Mastery")
    r.font.size = Pt(10); r.italic = True; r.font.color.rgb = GREY
    doc.add_paragraph()

    # 1. EXECUTIVE SUMMARY (ELI5 TO COMPLETE MASTERY)
    h(doc, 1, "1. Project Overview & Problem Statement (Explain Like I'm Five)")
    para(doc, "Bengaluru Metropolitan Transport Corporation (BMTC) is one of the largest urban bus operators in the world, "
              "operating ~6,737 route-directions, 3,940 physical buses, and 4,883 stops across Bengaluru. However, public "
              "transport in Bengaluru suffers from three fundamental structural problems:")
    numbered(doc, [
        ("The Commuter Discovery Problem:", "With thousands of bus routes, complex branch codes (e.g., 500-D, 335-A, KIA-8), "
         "and ambiguous Kannada/English stop names that repeat across the city (e.g. multiple distinct locations named Avalahalli "
         "or Kodihalli), commuters cannot reliably discover direct or transfer bus options, verify fares, or track buses."),
        ("The Operator Inefficiency Problem:", "BMTC schedules buses 'by route name' in isolated silos. If a route runs only "
         "morning and evening peaks, that bus sits completely idle at terminals during midday. Across 44 depots, this requires "
         "over 13,850 theoretical bus assignments. Without automated vehicle interlining, depot managers have had no automated "
         "way to chain trips across different routes."),
        ("The Transit Open Data Gap:", "Bengaluru lacked an open, standardized General Transit Feed Specification (GTFS) "
         "pipeline that third-party journey planners (like Google Maps or Apple Maps) could consume to show accurate live schedules."),
    ])
    para(doc, "DBARS (Demand Based Bus Allocation & Routing System) solves all three challenges simultaneously:", bold=True)
    bullets(doc, [
        ("Commuter Journey Planner:", "An intelligent web app that resolves fuzzy stop names, searches direct and 1-transfer "
         "chains in under 1 second, integrates Namma Metro stations, enables e-ticketing and digital travel passes, and shows live bus tracking."),
        ("Depot Optimization & Interlining Engine:", "A graph-theoretic vehicle scheduling algorithm that chains trips across "
         "routes sharing the same depot. It proves mathematically that the entire published timetable can be operated with just "
         "6,849 buses instead of 13,850—releasing 7,001 buses (a 51% reduction in fleet requirement) without cutting a single trip!"),
        ("Conductor Offline Ticketing & QR Verification:", "An offline-first mobile web app for conductors that cryptographically "
         "verifies commuter passes and issues tickets using HMAC-SHA256, syncing idempotently when network reconnects."),
        ("Standardized GTFS Export:", "Generates both official GTFS Static Zip (1.46M stop times) and GTFS-Realtime Service Alerts feeds."),
    ])

    table(doc, ["Key Metric / Dimension", "Measured Value / Exact Technical Figure"], [
        ["Total Dataset Scope", "6,737 route-directions | 4,883 unique bus stops | 46,470 scheduled trips"],
        ["Search Index Scale", "655,438 ordered stop pairs across 3,946,744 route segments"],
        ["Search Latency", "Median 0.94 s | p90 1.19 s (sub-second in-memory graph search)"],
        ["Fleet Optimization Result", "13,850 baseline buses -> 6,849 interlined buses (7,001 buses released across 44 depots)"],
        ["Theoretical Concurrency Floor", "5,723 simultaneous peak trips (hard physical floor on network fleet)"],
        ["Crew Scheduling Result", "21,453 block pieces -> 15,636 legal crew duties (crew-to-bus ratio 2.28)"],
        ["GTFS Open Data Size", "3,713 routes | 47,295 trips | 1,459,066 stop_times | ~14.4 MB Zip streamed in ~11 s"],
        ["Backend Architecture", "FastAPI 0.115, Python 3.11/3.12, Pydantic 2.10, Motor (async MongoDB), Docker"],
        ["Frontend Architecture", "React 19, TypeScript 5.7, Vite 6, Leaflet 1.9, Recharts 3, Tailwind/Bento CSS"],
        ["Automated Test Suite", "31 core predictor/ranking tests passing in CI; 161 backend regression tests total"],
    ], widths=[2.2, 4.6])

    # 2. THE THREE GOLDEN INVARIANTS
    h(doc, 1, "2. The Three Architectural Invariants (Must Memorize)")
    para(doc, "The entire technical design of DBARS is anchored around three uncompromising design invariants. "
              "If asked 'Why did you build it this way?', these three principles defend every major engineering decision:")

    callout(doc, "Invariant 1: Algorithmic Engines Read CSV Files, NOT MongoDB",
            "The search engine (predictor.py), fleet blocking engine (blocking.py), crew scheduling engine (crew.py), "
            "and GTFS builder (builder.py) are pure mathematical functions over files on disk (routes_cleaned.csv, stops_cleaned.csv, "
            "bmtc_depots.xlsx). They NEVER touch the database. train() executes BEFORE init_db(), and init_db() cannot crash startup. "
            "Result: If MongoDB crashes, experiences network timeouts, or is completely offline, bus route search, depot blocking, "
            "crew scheduling, and GTFS exports CONTINUE RUNNING FLAWLESSLY.", warn=False)

    callout(doc, "Invariant 2: Offline-First Cryptographic Verification for Conductors",
            "Buses in Bengaluru constantly pass through cellular dead zones (underpasses, basements, peripheral tech parks). "
            "Conductors cannot depend on an active internet connection to validate commuter passes. Travel passes and tickets are "
            "cryptographically signed HMAC-SHA256 tokens. The conductor's scanner validates the cryptographic signature locally on "
            "device with zero network calls. Ticket sales are assigned client-generated UUIDs and stored locally, syncing to MongoDB "
            "idempotently whenever a network connection becomes available.", warn=False)

    callout(doc, "Invariant 3: Zero AI Hallucinations in Route Search",
            "The bus route predictor contains NO generative LLMs, neural networks, or probabilistic black boxes. It uses deterministic "
            "information retrieval: an inverted stop index, an ordered stop-pair dictionary, Levenshtein edit distance, and a two-pass "
            "anchored geometric sequence validator. A bus prediction will NEVER invent non-existent stops or suggest physically impossible "
            "connections. Every result is grounded in BMTC's published timetable.", warn=False)

    # 3. COMPLETE TECHNOLOGY STACK
    h(doc, 1, "3. Complete Technology Stack (Layer-by-Layer)")
    table(doc, ["Layer", "Technology", "Exact Role & Responsibility in DBARS"], [
        ["Frontend UI", "React 19 & TypeScript 5.7", "Type-safe Single Page Application (SPA), component architecture, state management."],
        ["Frontend Build", "Vite 6 & Rollup", "Sub-second Hot Module Replacement (HMR) and optimized production asset bundling."],
        ["Styling & Design", "Vanilla CSS + Bento Grid", "Modern transport dashboard UI tokens, responsive layouts, zero heavy UI frameworks."],
        ["Interactive Maps", "Leaflet 1.9 & React-Leaflet", "Renders bus routes, stop sequences, and live bus positions on OpenStreetMap."],
        ["Charts & Analytics", "Recharts 3", "Interactive SVG charts for commuter hourly trends, language distribution, and depot metrics."],
        ["Backend API", "FastAPI 0.115.6 & Starlette", "High-performance asynchronous REST API framework with native OpenAPI docs (/docs)."],
        ["Runtime Server", "Uvicorn 0.34", "ASGI asynchronous web server worker hosting the FastAPI application."],
        ["Data Validation", "Pydantic 2.10.4", "Strict schema enforcement and input sanitization (rejects malformed inputs with HTTP 422)."],
        ["Database", "MongoDB 7.0 & Motor 3.6", "Async document database for user accounts, commuter votes, tickets, and waybills."],
        ["Search & Math", "NumPy 1.24+, SciPy, Scikit-learn", "TF-IDF matrix calculations, sparse cosine similarity, and statistical evaluations."],
        ["Cryptography", "HMAC-SHA256 & PBKDF2", "Handcrafted secure token generation with 3 isolated keys; salted password hashing."],
        ["Open Data Transit", "gtfs-realtime-bindings 2.2", "Google Transit Protobuf serializers for publishing GTFS-RT service alerts."],
        ["Containerization", "Docker & Docker Compose", "Multi-container orchestration for backend API, frontend web, and MongoDB."],
    ], widths=[1.5, 1.8, 3.5])

    para(doc, "Explicitly NOT Used in DBARS (Explain why during defense):", bold=True)
    bullets(doc, [
        ("No ORM (Object-Relational Mapper):", "ORM libraries like SQLAlchemy or Beanie add unnecessary abstraction layers and "
         "slow down document queries. Motor is used directly with raw pymongo queries for maximum speed."),
        ("No Generative LLMs in Transit Search:", "Prevents catastrophic hallucinations where a commuter is guided to non-existent buses."),
        ("No Third-Party JWT Library:", "JWT signing and verification is written from scratch using Python's standard hmac, hashlib, "
         "and base64 libraries to avoid vulnerable dependency bloat and guarantee complete control over token structure."),
        ("No External Payment Gateway:", "DBARS models closed-loop BMTC digital ticketing (like Namma Pass / Shakti Scheme) with server-side "
         "wallet/token accounting rather than integrating an external credit card gateway."),
    ])

    page_break(doc)

    # 4. STEP-BY-STEP WORKFLOWS (THE 4 USER JOURNEYS)
    h(doc, 1, "4. End-to-End System Workflows (How the Project Works)")

    h(doc, 2, "4.1 Workflow 1: Commuter Route Search & Ticketing Journey")
    code(doc,
         "  [Commuter Enters Search] -> Types 'Silk Board' and 'Marathahalli' in PredictPage.tsx\n"
         "      |\n"
         "  [Autocomplete] -> GET /autocomplete?q=... -> Inverted prefix trie returns matches in <5ms\n"
         "      |\n"
         "  [API Request] -> POST /predict with {'current_stop': 'Silk Board', 'destination': 'Marathahalli'}\n"
         "      |\n"
         "  [Pydantic Validation] -> PredictRequest cleans text, strips special chars, verifies min_length\n"
         "      |\n"
         "  [Async Offloading] -> asyncio.to_thread(predictor.predict) -> Runs on thread pool to protect event loop\n"
         "      |\n"
         "  [Stop Resolution] -> Alias mapping + Levenshtein distance resolves stop names to canonical IDs\n"
         "      |\n"
         "  [Direct Route Lookup] -> Checks stop_pair_to_segments[(origin, dest)] in memory\n"
         "      |\n"
         "  [1-Transfer Search] -> If needed, intersects routes at walkable interchange (<1.2 km walk guard)\n"
         "      |\n"
         "  [Two-Pass Anchoring] -> resolve_stop_sequence() validates coordinates, eliminating route teleportation\n"
         "      |\n"
         "  [Multi-Objective Rank] -> Ranks routes by span efficiency, trip frequency (log1p), and headway\n"
         "      |\n"
         "  [Metro Integration] -> Finds 3 nearest Namma Metro stations to destination using Haversine distance\n"
         "      |\n"
         "  [UI Render] -> Displays best match, transfer steps, route polyline map, fares, and active alerts\n"
         "      |\n"
         "  [Ticket Purchase] -> Commuter buys digital ticket/pass -> Issues cryptographically signed HMAC token & QR")

    h(doc, 2, "4.2 Workflow 2: Depot Manager Vehicle Blocking & Re-block Approval")
    code(doc,
         "  [Depot Login] -> Depot Manager logs in with credentials depot@bmtc.gov.in / depot123\n"
         "      |\n"
         "  [Fetch Plan] -> GET /depot/blocking-plan (Bearer Token authenticated)\n"
         "      |\n"
         "  [Graph Vehicle Chaining] -> BlockingEngine reads 46,470 departures from routes_cleaned.csv\n"
         "      |\n"
         "  [Dilworth Bound] -> Computes concurrency lower bound: peak simultaneous trips across Bengaluru = 5,723\n"
         "      |\n"
         "  [Interlining Algorithm] -> Chains trips across routes belonging to the same home depot\n"
         "      |\n"
         "  [Savings Calculation] -> 13,850 buses isolated -> 6,849 buses interlined (7,001 buses released, 51% reduction!)\n"
         "      |\n"
         "  [Proposals Table] -> Displays top re-block opportunities (e.g. EXP-298MP, 89-D, 238-U, 225-C)\n"
         "      |\n"
         "  [Decision Action] -> Manager clicks 'Approve' or 'Reject' -> POST /depot/blocking-decision\n"
         "      |\n"
         "  [Advisory Record] -> Records decision with user ID and timestamp (advisory: no physical fleet dispatch)")

    h(doc, 2, "4.3 Workflow 3: Conductor Offline QR Scanner & Idempotent Sync")
    code(doc,
         "  [Shift Sign-On] -> Conductor signs on at start of shift -> Assigns waybill ID and route number\n"
         "      |\n"
         "  [Passenger Scans Pass] -> Conductor points phone camera at passenger's digital QR pass\n"
         "      |\n"
         "  [Local Crypto Verification] -> Parses token segments: header.payload.signature\n"
         "      |-- Verifies HMAC-SHA256 signature using PASS_VERIFICATION_SECRET (no internet required!)\n"
         "      |-- Validates expiry date (exp) and token type ('travel_pass')\n"
         "      '-- Screen displays instantaneous GREEN 'PASS VALID' or RED 'INVALID / EXPIRED'\n"
         "      |\n"
         "  [Offline Cash Ticketing] -> Conductor issues ticket on bus -> Generated client UUID stored in IndexedDB\n"
         "      |\n"
         "  [Reconnection & Sync] -> POST /tickets/sync sends batch array of ticket sales\n"
         "      |\n"
         "  [Idempotent Write] -> MongoDB unique compound index on (waybill_id, client_ticket_uuid)\n"
         "      '-- Replayed or duplicate network packets are rejected silently without double-counting revenue!")

    h(doc, 2, "4.4 Workflow 4: Administrator Audit & Shakti Scheme Reimbursement")
    code(doc,
         "  [Admin Login] -> System Administrator logs in with admin@bmtc.gov.in / admin123\n"
         "      |\n"
         "  [Executive Overview] -> GET /admin/dashboard shows active commuters, votes, fraud rate, response time\n"
         "      |\n"
         "  [Citywide Fleet Overview] -> BlockingSummaryCard renders citywide depot rollup (12 largest depots)\n"
         "      |\n"
         "  [Shakti Scheme Audit] -> GET /admin/shakti/claim audits free-travel claims for women commuters\n"
         "      |-- Filters zero-fare tickets issued with verified Karnataka resident status\n"
         "      '-- Generates audit-ready reimbursement invoice for Karnataka State Government\n"
         "      |\n"
         "  [Security Audit] -> GET /admin/audit reviews security and auth events across the platform\n"
         "      |\n"
         "  [Retrain Trigger] -> POST /train forces re-computation and validation of search indexes")

    page_break(doc)

    # 5. CORE BUS SEARCH ENGINE DEEP DIVE (THE 8 PROGRAM FILES)
    h(doc, 1, "5. The Core Route Search Engine (The 8 Protected Files)")
    para(doc, "The heart of DBARS is its bus route search and ranking engine. It is strictly encapsulated within 8 files. "
              "Understanding these 8 files gives you complete mastery of the core product:")

    table(doc, ["#", "File Path", "Exact Purpose & Internal Working"], [
        ["1", "backend/app/ml/predictor.py",
         "The master search engine (1,600+ lines). Builds the 655,438 ordered stop-pair index at startup. "
         "Executes predict(), finding direct routes, evaluating 1-transfer changeovers, running the walkable transfer "
         "filter (_interchange_is_walkable), and applying the multi-objective span-band ranking algorithm."],
        ["2", "backend/app/ml/tfidf.py",
         "N-gram TF-IDF vectorizer and sparse matrix cosine similarity calculator. Converts raw user stop queries "
         "into TF-IDF vectors to match against canonical stop names in the dataset."],
        ["3", "backend/app/ml/text.py",
         "Text normalization and cleaning. Lowercases strings, removes punctuation, normalizes spacing, and handles "
         "common Bengaluru stop naming quirks (e.g. KBS vs Majestic vs Kempegowda Bus Station)."],
        ["4", "backend/app/ml/distance.py",
         "Distance calculations. Contains Haversine spherical distance formulas and cached Google Maps road distance "
         "service. Converts straight-line stop coordinates to accurate road kilometers using circuity factors."],
        ["5", "backend/app/ml/stop_registry.py",
         "Maintains canonical stop definitions, geographical latitude/longitude coordinates, and hashed stop IDs "
         "across all 4,883 stops in Bengaluru. Resolves aliases and stop name collisions."],
        ["6", "backend/app/ml/data_loader.py",
         "Loads and parses routes_cleaned.csv into strongly typed RouteRecord objects. Extracts trip lists, "
         "departure timetables, stop counts, and direction IDs."],
        ["7", "backend/app/api/routes.py",
         "FastAPI router exposing POST /predict, GET /autocomplete, and GET /routes. Offloads CPU-bound search "
         "to thread pools using asyncio.to_thread, keeping the async event loop responsive."],
        ["8", "frontend/src/pages/PredictPage.tsx",
         "The commuter journey UI. Features real-time stop autocomplete, route visualizers, transfer step badges, "
         "fare calculators, interactive Leaflet route maps, and e-ticket purchase triggers."],
    ], widths=[0.3, 2.2, 4.3])

    h(doc, 2, "5.1 The Two-Pass Anchored Geometric Stop Resolution (The 'Avalahalli Bug')")
    para(doc, "The most difficult bug in the project's development was the 'Avalahalli Teleportation Bug'. In Bengaluru, "
              "multiple distinct locations share identical or similar names (e.g. Avalahalli on Mysore Road vs Avalahalli near "
              "Yelahanka, 28.6 km apart). Initial fuzzy string matching matched solely on stop name text, causing the map to draw "
              "a bizarre 69 km zigzag line across the city for a simple 19 km commute!")
    para(doc, "How DBARS solved it (Two-Pass Anchored Resolution):", bold=True)
    numbered(doc, [
        ("Pass 1 (Anchor Detection):", "Locate unambiguous terminal stops (route origin and destination) whose coordinates "
         "are known with 100% certainty."),
        ("Pass 2 (Geometric Proximity Constrained Matching):", "For every intermediate stop in the sequence, search candidate "
         "coordinates and select the stop candidate that minimizes deviation from the route's forward progress corridor. "
         "Candidate stops farther than 1.2 km from the logical trajectory are rejected."),
    ])

    # 6. MATHEMATICAL MODELS & FORMULAS
    h(doc, 1, "6. Mathematical Models & Formulas Explained Simply")

    h(doc, 2, "6.1 Dilworth's Theorem & The Minimum Fleet Lower Bound")
    para(doc, "How do we prove mathematically that BMTC does not need 13,850 buses? We compute the concurrency lower bound:")
    code(doc,
         "  Let T = {t_1, t_2, ..., t_n} be the set of all scheduled trips across Bengaluru.\n"
         "  Each trip t_i has a start time s(t_i) and an end time e(t_i).\n"
         "  At any given clock minute m, the number of active trips running simultaneously is:\n"
         "      C(m) = sum(1 for t in T if s(t) <= m < e(t))\n"
         "\n"
         "  The Theoretical Fleet Floor (Lower Bound) is:\n"
         "      Buses_Floor = max_{0 <= m < 1440} C(m) = 5,723 buses.\n"
         "\n"
         "  By Dilworth's Theorem on partially ordered sets (posets), no valid schedule can physically\n"
         "  operate the timetable with fewer buses than this peak concurrency. Our interlining algorithm\n"
         "  achieves 6,849 buses across 44 depots—within 19% of the absolute mathematical optimum!")

    h(doc, 2, "6.2 Haversine Great-Circle Distance Formula")
    para(doc, "Used to calculate straight-line distance between stops (lat1, lon1) and (lat2, lon2) on Earth (R = 6,371 km):")
    code(doc,
         "  d_lat = radians(lat2 - lat1)\n"
         "  d_lon = radians(lon2 - lon1)\n"
         "  a = sin^2(d_lat / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin^2(d_lon / 2)\n"
         "  c = 2 * arcsin(sqrt(a))\n"
         "  distance_km = R * c\n"
         "  road_distance_km = distance_km * circuity_factor (1.25)")

    h(doc, 2, "6.3 Multi-Objective Span-Band Route Ranking Formula")
    para(doc, "Direct candidates are ranked using a multi-objective scoring function:")
    code(doc,
         "  Score = w_span * Span_Efficiency + w_freq * log1p(Trip_Count) - w_penalty * Excess_Span_Penalty\n"
         "    - Span_Efficiency: Ratio of requested journey distance to total route distance.\n"
         "    - log1p(Trip_Count): Rewards high-frequency trunk corridors (diminishing returns with log).\n"
         "    - Excess_Span_Penalty: Heavily penalizes circuitous routes that meander through suburbs.")

    page_break(doc)

    # 7. DATABASE ARCHITECTURE & MONGODB SCHEMA
    h(doc, 1, "7. Database Architecture (MongoDB 7.0)")
    para(doc, "MongoDB is accessed asynchronously through Motor. There are 14 operational collections, designed around document isolation:")

    table(doc, ["Collection Name", "Key Fields & Schema Structure", "Indexes & Operational Rules"], [
        ["users", "email, password_hash, role, preferred_lang, shakti_eligible, created_at", "Unique index on email. Roles: admin, depot_manager, conductor, commuter."],
        ["votes", "user_id, current_stop, destination, time_preference, flagged, created_at", "Compound index on (current_stop, destination). Drives dispatch recommendations."],
        ["travel_passes", "pass_id, user_id, pass_type, valid_until, qr_code_payload, status", "Index on pass_id. Cryptographically signed tokens verified offline by conductors."],
        ["conductor_tickets", "waybill_id, client_ticket_uuid, fare, source, destination, issued_at", "UNIQUE compound index on (waybill_id, client_ticket_uuid) for idempotent offline sync."],
        ["waybills", "waybill_id, conductor_id, route_no, bus_no, sign_on_time, cash_collected", "Tracks shift revenue, tickets issued, and cash reconciliation per conductor shift."],
        ["trip_shares", "share_id, user_id, trip_details, emergency_contacts, expires_at", "TTL index on expires_at physically deletes shared journeys after 6 hours (privacy)."],
        ["usage_events", "event_type, payload, timestamp", "TTL index deletes analytics after 90 days. Logs search queries and feature usage."],
        ["audit_events", "action, user_id, ip_address, timestamp, status", "DELIBERATELY NO TTL. Permanent audit log for security, administrative actions, and claims."],
        ["service_alerts", "alert_id, severity, header_text, description_text, active_period", "Published live to GTFS-Realtime Protobuf service alert feeds for operators."],
    ], widths=[1.8, 2.6, 2.4])

    # 8. SECURITY & CRYPTOGRAPHY MODEL
    h(doc, 1, "8. Security, Cryptography & Auth Architecture")
    bullets(doc, [
        ("Password Security:", "Passwords are never stored in plaintext. They are hashed using PBKDF2-SHA256 with 100,000 iterations "
         "and a cryptographically secure 16-byte random salt (os.urandom(16))."),
        ("Three Isolated Cryptographic Key Domains:", "To prevent privilege escalation, three separate secrets exist in .env: "
         "(1) JWT_SECRET_KEY for login session tokens; (2) PASS_VERIFICATION_SECRET for commuter travel passes; "
         "(3) E-ticket verification keys. Even if an attacker decompiles a conductor scanner and extracts the pass key, "
         "they CANNOT forge user session tokens or administrative credentials!"),
        ("Token Structure (Header.Payload.Signature):", "Handcrafted HMAC-SHA256 tokens contain base64url encoded headers and payloads, "
         "sealed with an HMAC signature. Tampering with any byte of the payload immediately invalidates the cryptographic signature."),
        ("Strict Role-Based Access Control (RBAC):", "Endpoints are protected via FastAPI dependencies: Depends(require_role(UserRole.ADMIN)) "
         "or Depends(require_role(UserRole.DEPOT_MANAGER)). During public registration (/auth/register), the role is hardcoded to 'commuter', "
         "preventing privilege escalation attacks."),
        ("Rate Limiting Middleware:", "Custom in-memory sliding-window rate limiter restricted to 120 requests/minute per client IP."),
    ])

    page_break(doc)

    # 9. TOP 25 PROFESSOR & VIVA QUESTIONS
    h(doc, 1, "9. Top 25 Professor & Defense Viva Questions (Word-for-Word Answers)")
    _qa(doc, [
        ("What is DBARS in one clear sentence?",
         "DBARS is an end-to-end intelligent transit platform for Bengaluru that provides commuters with sub-second journey planning, "
         "gives depot managers an optimization engine that reduces fleet requirements by 51% through vehicle interlining, and exports "
         "open GTFS feeds for smart city integration."),

        ("What specific problem does this project solve?",
         "It solves two major problems: for commuters, finding optimal bus and metro connections across 6,737 routes in Bengaluru; "
         "for BMTC operators, eliminating empty idle buses by mathematically chaining trips across routes sharing the same depot."),

        ("Explain your system architecture.",
         "It is a four-tier architecture: (1) React 19 Single Page Application frontend; (2) FastAPI asynchronous REST API layer; "
         "(3) Pure mathematical algorithmic engines in Python (app/ml) reading CSV timetable files; and (4) MongoDB document database "
         "for user state, ticketing, and voting."),

        ("Why do the algorithmic engines read CSV files instead of MongoDB?",
         "This is our key design invariant: decoupling computation from database availability. If MongoDB is down or unreachable, "
         "core bus routing, depot blocking, crew scheduling, and GTFS exports continue working 100% without error."),

        ("How does your bus route prediction algorithm work?",
         "At startup, the engine pre-indexes 655,438 ordered stop pairs across all 6,737 routes. When a commuter enters two stops, "
         "we resolve stop names using alias mapping and Levenshtein distance, perform an in-memory dictionary lookup for direct buses, "
         "evaluate 1-transfer options via walkable interchange nodes (<1.2 km), and rank candidates using multi-objective span-band scoring."),

        ("Why do you store 'ordered' stop pairs instead of simple stop sets?",
         "Because bus routes are directional. A bus traveling from Majestic to Electronic City passes both stops, but traveling in reverse "
         "from Electronic City to Majestic requires the opposite direction. An unordered set would suggest buses traveling the wrong way."),

        ("What was the hardest bug you encountered and how did you fix it?",
         "The Avalahalli stop collision bug. Bengaluru has multiple distinct stops with identical names located 28.6 km apart. Fuzzy text "
         "matching originally caused routes to jump across the city. We fixed it by inventing Two-Pass Anchored Geometric Resolution: "
         "identifying unambiguous terminus anchor stops first, then constraining intermediate stop selection to a geographic corridor."),

        ("How did you achieve a 51% fleet reduction in the blocking plan?",
         "BMTC historically schedules buses isolated by route name, requiring 13,850 buses. Our BlockingEngine implements vehicle "
         "interlining: when Bus A completes a morning trip on Route 1, instead of sitting idle for 3 hours, it immediately pulls out on "
         "Route 2 from the same terminal. Across 44 depots, this chains 46,470 trips into just 6,849 vehicle blocks, saving 7,001 buses."),

        ("How do you know 6,849 buses is a valid number and not just an arbitrary guess?",
         "We compute the theoretical concurrency lower bound based on Dilworth's Theorem: the maximum number of simultaneous trips running "
         "at peak minute across Bengaluru is 5,723 buses. No schedule can beat 5,723 buses. Our interlined schedule of 6,849 is within 19% "
         "of the theoretical physical limit."),

        ("What is the difference between a vehicle 'block' and a crew 'duty'?",
         "A block is a bus's day (from morning depot pull-out to night pull-in, often 14–16 hours). A crew duty is a human driver's legal "
         "work shift (capped at 8 hours of driving by Indian Motor Transport Workers Act regulations). A vehicle block must be cut into "
         "legal crew pieces and paired into continuous or split duties."),

        ("How does offline ticketing work for bus conductors?",
         "Buses frequently lose mobile connectivity. Travel passes are cryptographically signed HMAC-SHA256 tokens. The conductor's phone "
         "validates the cryptographic signature locally without internet access. When conductors issue tickets, each ticket receives a "
         "client-generated UUID; when reconnected, tickets sync idempotently to MongoDB using a unique compound index."),

        ("What does idempotency mean in your sync endpoint?",
         "It means if a conductor's device sends the same batch of 50 ticket sales multiple times due to poor cellular connectivity, "
         "MongoDB's unique index on (waybill_id, client_ticket_uuid) accepts the first write and silently ignores duplicate replays. "
         "Revenue and passenger counts are never double-counted."),

        ("How is user authentication handled?",
         "Passwords are encrypted with PBKDF2-SHA256 using 100,000 iterations and 16-byte random salts. Sessions use HMAC-SHA256 signed "
         "Bearer JWT tokens verified on protected routes by FastAPI's Depends(require_role)."),

        ("Why do you have three separate signing secrets?",
         "To maintain cryptographic isolation between domains: session tokens, commuter travel passes, and e-tickets use separate keys. "
         "If a commuter pass key is somehow compromised, an attacker still cannot forge administrative sessions."),

        ("What is the Shakti Scheme feature in DBARS?",
         "The Shakti Scheme is the Karnataka Government's policy providing free bus travel for women. DBARS enables eligible women "
         "commuters to book zero-fare tickets, and provides BMTC with an automated government reimbursement audit dashboard."),

        ("How is live bus tracking implemented?",
         "Via a simulated AVL (Automatic Vehicle Location) GPS feed that updates bus coordinates along real route geometry. The server "
         "honestly flags tracking as simulated (is_live=False), preventing synthetic telemetry from being misrepresented as real AVL data."),

        ("What is GTFS and why does your project export it?",
         "General Transit Feed Specification is the international open data standard for public transit. DBARS generates static GTFS "
         "zip files and GTFS-Realtime Protobuf service alert feeds, enabling third-party apps like Google Maps to ingest BMTC schedules."),

        ("Why did you choose MongoDB over PostgreSQL?",
         "Transit entities like route stop lists, waybills, and flexible commuter votes are document-oriented and evolve rapidly. "
         "MongoDB's schema flexibility and Motor's high-speed async I/O provided the ideal match without heavyweight SQL migrations."),

        ("What happens if 10,000 commuters query routes at the exact same second?",
         "Currently, the server is single-process with in-memory caching and a 120 req/min rate limit per IP. Scaling to 10,000 concurrent "
         "requests would require moving the in-memory rate limiter and search index caches to Redis and spawning multi-worker Uvicorn clusters."),

        ("What is the weakest part of this project?",
         "The complete absence of automated frontend tests across our 8,459 lines of React code, contrasted with our 161 backend tests. "
         "Adding Vitest/Playwright tests for the frontend offline sync queue is our top technical debt priority."),

        ("How long does it take for the backend to start up?",
         "Approximately 7 to 10 seconds. In those seconds, it loads 6,737 routes, builds the 655,438 stop-pair index, warms the blocking "
         "plan, streams the GTFS feed, and establishes the MongoDB connection."),

        ("Is there any AI or LLM in your bus route search?",
         "No. The bus routing engine is built entirely with deterministic information retrieval: TF-IDF vectorization, Levenshtein distance, "
         "ordered graph indexes, and geometric two-pass anchoring. It contains no generative models or probabilistic hallucinations."),

        ("How did you test the backend?",
         "We wrote 161 pytest automated unit and integration tests covering route prediction accuracy, stop alias resolution, span-band "
         "ranking quality, blocking plan mathematical bounds, and cryptographic token verification."),

        ("What are the primary ranking metrics in your predictor?",
         "We measure rank quality using Best Option Rate (71.7%), Within-2-Stops Rate (99.2%), and Normalized Discounted Cumulative Gain "
         "(NDCG@5 = 0.982), prioritizing direct routes, high-frequency trunk corridors, and short stop spans."),

        ("If you had another month, what would you add?",
         "Three things: (1) automated frontend end-to-end tests; (2) multi-leg transfers supporting two changes; and (3) real hardware "
         "AVL GPS hardware integration via MQTT."),
    ])

    page_break(doc)

    # 10. RECRUITER & TECHNICAL INTERVIEW GUIDE
    h(doc, 1, "10. Top 15 Technical Interviewer & Recruiter Questions")
    _qa(doc, [
        ("Tell me about an architectural trade-off you made in this project.",
         "I chose to decouple the computational engines from MongoDB completely. The trade-off was that route data cannot be dynamically "
         "edited through database writes—it requires updating the timetable CSV and calling /train. But the massive benefit is fault "
         "tolerance: database crashes never bring down core route search or depot optimization."),

        ("How did you optimize performance in the crew scheduling algorithm?",
         "Initially, pairing 21,453 crew pieces into split duties was quadratic O(N^2), taking over 36 seconds per depot. I replaced it "
         "with a binary search over the spreadover window combined with a path-compressed skip list, reducing execution time to 1.6 seconds."),

        ("How do you handle race conditions in offline ticket synchronization?",
         "Instead of relying on server-side autoincrement IDs, the client generates a unique UUID (crypto.randomUUID()) for every ticket. "
         "The backend enforces a unique compound index on (waybill_id, client_ticket_uuid). Any duplicate packet sent during retry storms "
         "is rejected by MongoDB at the database engine level."),

        ("How do you prevent memory leaks when running background startup tasks?",
         "In Python's asyncio, background tasks referenced only by local variables can be garbage-collected mid-execution. In app/main.py, "
         "I store background warming tasks as strong references on app.state (e.g. app.state.blocking_warm_task), ensuring they complete."),

        ("Why did you avoid using an ORM?",
         "Transit datasets are read-heavy and document-shaped. ORMs add 20–30% serialization overhead and obscure raw query performance. "
         "Using Motor directly gave us clean, explicit async query execution with zero overhead."),

        ("What would be your strategy to scale this horizontally?",
         "First, externalize all in-memory state: move the IP rate limiter, session tracking, and precomputed search caches into a Redis "
         "cluster. Second, containerize the FastAPI app behind an Nginx or AWS ALB reverse proxy with auto-scaling ECS/Kubernetes pods."),

        ("Explain your testing philosophy on this project.",
         "I focused on black-box invariant testing. For example, testing whether a direct bus always outranks an otherwise attractive "
         "transfer bus, and asserting mathematical bounds on the blocking engine rather than mocking internal helper functions."),

        ("How do you protect against SQL/NoSQL injection?",
         "All input payloads are strictly validated using Pydantic schemas. Text fields have custom field_validators that strip forbidden "
         "characters (<, >, {, }, [, ], \\), and MongoDB queries use parameterized dictionary filters, eliminating NoSQL injection."),

        ("What was your role and individual contribution?",
         "I designed and implemented the full-stack architecture: building the FastAPI backend, developing the graph search and "
         "interlining algorithms, integrating Namma Metro data, crafting the React 19 UI, and creating the offline conductor sync engine."),

        ("What did this project teach you about production systems?",
         "That making a system honest is far harder than making it work. Several early algorithms produced confident, plausible-looking "
         "numbers that were mathematically wrong upon close inspection. Rigorous verification against mathematical bounds is essential."),
    ])

    style.add_header(doc, "DBARS - Master Revision Sheet")
    style.add_page_numbers(doc)
    out = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                                       "DBARS_Master_Revision_Sheet.docx"))
    doc.save(out)
    print("Output: %s" % out)
    print("Size:   %.1f KB" % (os.path.getsize(out) / 1024.0))


if __name__ == "__main__":
    build()
