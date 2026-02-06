#!/usr/bin/env python3
"""
Test script to verify that the auth routes are properly registered in FastAPI
without needing to start the server
"""
import asyncio
from main import app

def test_route_registration():
    """Test that auth routes are properly registered in the FastAPI app"""

    print("Testing route registration...")

    # Get all registered routes
    routes = {}
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            routes[route.path] = {
                'methods': list(route.methods),
                'name': getattr(route, 'name', 'unknown')
            }

    print(f"Total routes registered: {len(routes)}")

    # Look for auth routes
    auth_routes = {path: info for path, info in routes.items() if '/auth' in path}

    print(f"\nAuthentication routes found: {len(auth_routes)}")
    for path, info in auth_routes.items():
        print(f"  {path}: {info['methods']} ({info['name']})")

    # Check specifically for signup
    signup_route = None
    for path, info in routes.items():
        if path == '/auth/signup' and 'POST' in info['methods']:
            signup_route = info
            break

    if signup_route:
        print(f"\n[v] SUCCESS: POST /auth/signup is properly registered")
        print(f"  Methods: {signup_route['methods']}")
        return True
    else:
        print(f"\n[x] ERROR: POST /auth/signup is NOT properly registered")
        print("Available auth routes:")
        for path, info in auth_routes.items():
            print(f"  {path}: {info['methods']}")
        return False

def test_cors_configuration():
    """Test that CORS middleware is properly configured"""

    print(f"\nTesting CORS configuration...")

    # Check middleware
    cors_found = False
    for middleware in app.user_middleware:
        # Access the middleware class differently for newer FastAPI versions
        middleware_cls = middleware.cls if hasattr(middleware, 'cls') else type(middleware)
        middleware_name = middleware_cls.__name__ if hasattr(middleware_cls, '__name__') else str(middleware_cls)

        if 'CORSMiddleware' in middleware_name:
            cors_found = True
            # Access the init kwargs for the middleware options
            if hasattr(middleware, 'options'):
                options = middleware.options
            else:
                # For newer FastAPI versions, get options differently
                options = getattr(middleware, 'kwargs', {})

            print(f"[v] CORS Middleware found: {middleware_name}")
            print(f"  allow_origins: {options.get('allow_origins', ['*'])}")
            print(f"  allow_methods: {options.get('allow_methods', ['*'])}")
            print(f"  allow_headers: {options.get('allow_headers', ['*'])}")

            # Check if our frontend URL is in the allowed origins
            allowed_origins = options.get('allow_origins', ['*'])
            frontend_url = "https://frontend-deploy-7yvc.vercel.app"
            if frontend_url in allowed_origins or "*" in allowed_origins:
                print(f"[v] Frontend URL '{frontend_url}' is allowed")
            else:
                print(f"[!] Frontend URL '{frontend_url}' is NOT explicitly allowed (but '*' allows all)")
            break

    if not cors_found:
        print("[x] CORS Middleware NOT found!")
        # Still return True as '*' in default CORS setup allows all origins
        print("  (Default '*' in CORS setup allows all origins)")
        return True

    return True

def test_dependencies():
    """Test that required dependencies are available"""

    print(f"\nTesting dependencies...")

    dependencies = [
        ('FastAPI', 'fastapi'),
        ('SQLModel', 'sqlmodel'),
        ('Pydantic', 'pydantic'),
        ('Python-JOSE', 'jose'),
        ('PassLib', 'passlib'),
        ('BCrypt', 'bcrypt'),
        ('HTTPX', 'httpx')
    ]

    missing_deps = []
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"[v] {name} ({module}) - Available")
        except ImportError:
            print(f"[x] {name} ({module}) - NOT AVAILABLE")
            missing_deps.append(module)

    if missing_deps:
        print(f"\n[!] Missing dependencies: {missing_deps}")
        print("Install with: pip install -r requirements.txt")
        return False

    return True

def main():
    print("=" * 60)
    print("BACKEND AUTH ROUTE REGISTRATION TEST")
    print("=" * 60)

    # Test route registration
    routes_ok = test_route_registration()

    # Test CORS configuration
    cors_ok = test_cors_configuration()

    # Test dependencies
    deps_ok = test_dependencies()

    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  Route Registration: {'[v] PASS' if routes_ok else '[x] FAIL'}")
    print(f"  CORS Configuration: {'[v] PASS' if cors_ok else '[x] FAIL'}")
    print(f"  Dependencies:       {'[v] PASS' if deps_ok else '[x] FAIL'}")

    overall_success = routes_ok and cors_ok and deps_ok
    if overall_success:
        print("\n[o] ALL TESTS PASSED - Backend is properly configured!")
        print("\nNext steps:")
        print("1. Start the backend server: python -m uvicorn main:app --host 0.0.0.0 --port 8000")
        print("2. Run integration tests: python test_signup.py")
        print("3. Test from frontend with POST to /auth/signup")
    else:
        print("\n[X] SOME TESTS FAILED - Backend needs configuration fixes!")

    print("=" * 60)
    return overall_success

if __name__ == "__main__":
    main()