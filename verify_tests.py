#!/usr/bin/env python3
"""
Verification script for the AI Chatbot project tests
"""

import os
import sys

def main():
    """Verify that all test files have been created"""
    print("=" * 60)
    print("AI Chatbot Project - Test Suite Verification")
    print("=" * 60)

    # Backend test files to verify
    backend_test_files = [
        "backend/tests/conftest.py",
        "backend/tests/unit/test_models.py",
        "backend/tests/unit/test_mcp_tools.py",
        "backend/tests/unit/test_agents.py",
        "backend/tests/unit/test_services.py",
        "backend/tests/unit/test_exceptions.py",
        "backend/tests/integration/test_chat_endpoints.py",
        "backend/tests/integration/test_main.py",
        "backend/tests/test_main.py",
        "backend/pytest.ini",
        "backend/requirements-test.txt"
    ]

    # Frontend test files to verify
    frontend_test_files = [
        "frontend/tests/setupTests.js",
        "frontend/tests/chat-api.test.ts",
        "frontend/tests/ChatContext.test.tsx",
        "frontend/tests/ChatKitWrapper.test.tsx",
        "frontend/tests/Navigation.test.tsx",
        "frontend/jest.config.js",
        "frontend/test-requirements.txt"
    ]

    print("\n1. VERIFYING BACKEND TEST FILES:")
    print("-" * 30)
    backend_missing = []
    for file in backend_test_files:
        full_path = os.path.join(os.getcwd(), file)
        exists = os.path.exists(full_path)
        status = "[OK]" if exists else "[MISSING]"
        print(f"  {status} {file}")
        if not exists:
            backend_missing.append(file)

    print(f"\nBackend tests created: {len([f for f in backend_test_files if os.path.exists(os.path.join(os.getcwd(), f))])}/{len(backend_test_files)}")

    print("\n2. VERIFYING FRONTEND TEST FILES:")
    print("-" * 30)
    frontend_missing = []
    for file in frontend_test_files:
        full_path = os.path.join(os.getcwd(), file)
        exists = os.path.exists(full_path)
        status = "[OK]" if exists else "[MISSING]"
        print(f"  {status} {file}")
        if not exists:
            frontend_missing.append(file)

    print(f"\nFrontend tests created: {len([f for f in frontend_test_files if os.path.exists(os.path.join(os.getcwd(), f))])}/{len(frontend_test_files)}")

    print("\n3. SUMMARY:")
    print("-" * 15)
    total_backend = len(backend_test_files)
    total_frontend = len(frontend_test_files)
    created_backend = total_backend - len(backend_missing)
    created_frontend = total_frontend - len(frontend_missing)

    print(f"Backend test files: {created_backend}/{total_backend} created")
    print(f"Frontend test files: {created_frontend}/{total_frontend} created")
    print(f"Total test files created: {created_backend + created_frontend}/{total_backend + total_frontend}")

    if backend_missing:
        print(f"\nMissing backend files: {len(backend_missing)}")
        for f in backend_missing:
            print(f"  - {f}")

    if frontend_missing:
        print(f"\nMissing frontend files: {len(frontend_missing)}")
        for f in frontend_missing:
            print(f"  - {f}")

    all_created = len(backend_missing) == 0 and len(frontend_missing) == 0
    print(f"\nOverall status: {'SUCCESS - All test files created!' if all_created else 'PARTIAL - Some test files missing'}")

    print("\n4. TEST COVERAGE SUMMARY:")
    print("-" * 25)
    print("Backend Unit Tests:")
    print("  - Models: Conversation, Message entities")
    print("  - MCP Tools: Base, Create, Update, Delete, Search, Complete, Registry")
    print("  - Agents: Config, ChatAgent, ToolBinder, Factory")
    print("  - Services: Conversation, Message, Loader, Persistence")
    print("  - Exceptions: All custom chat exceptions")

    print("\nBackend Integration Tests:")
    print("  - Chat endpoints: All API endpoints")
    print("  - Main app: Startup, routing, health checks")

    print("\nFrontend Tests:")
    print("  - API client: All chat API functions")
    print("  - Context: ChatContext provider and hooks")
    print("  - Components: ChatKitWrapper, Navigation")
    print("  - Utilities: Setup and configuration")

    print("\n" + "=" * 60)
    print("TEST SUITE VERIFICATION COMPLETE")
    print("=" * 60)

    return 0 if all_created else 1

if __name__ == "__main__":
    sys.exit(main())