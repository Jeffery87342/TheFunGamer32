#!/usr/bin/env python3
"""
Test script to verify all modules load correctly
"""

import sys

def test_imports():
    """Test that all modules can be imported"""
    tests = []
    
    # Test util
    try:
        from util import Util
        tests.append(("util.py", True, "OK"))
    except Exception as e:
        tests.append(("util.py", False, str(e)))
    
    # Test output
    try:
        from output import Output
        tests.append(("output.py", True, "OK"))
    except Exception as e:
        tests.append(("output.py", False, str(e)))
    
    # Test counter
    try:
        from counter import counter
        tests.append(("counter.py", True, "OK"))
    except Exception as e:
        tests.append(("counter.py", False, str(e)))
    
    # Test session
    try:
        from session import Session
        tests.append(("session.py", True, "OK"))
    except Exception as e:
        tests.append(("session.py", False, str(e)))
    
    # Test auth_intent
    try:
        from auth_intent import AuthIntent
        tests.append(("auth_intent.py", True, "OK"))
    except Exception as e:
        tests.append(("auth_intent.py", False, str(e)))
    
    # Test custom_solver
    try:
        from custom_solver import get_token
        tests.append(("custom_solver.py", True, "OK"))
    except Exception as e:
        tests.append(("custom_solver.py", False, str(e)))
    
    # Test group_joiner
    try:
        from group_joiner import GroupJoiner
        tests.append(("group_joiner.py", True, "OK"))
    except Exception as e:
        tests.append(("group_joiner.py", False, str(e)))
    
    # Print results
    print("="*60)
    print("Module Import Tests")
    print("="*60)
    
    all_passed = True
    for module, passed, message in tests:
        status = "✓" if passed else "✗"
        print(f"{status} {module:20s} {message}")
        if not passed:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("✅ All modules loaded successfully!")
        return 0
    else:
        print("❌ Some modules failed to load")
        return 1

def test_config():
    """Test configuration loading"""
    print("\n" + "="*60)
    print("Configuration Tests")
    print("="*60)
    
    from util import Util
    import os
    
    # Check config file
    if os.path.exists("input/config.json"):
        print("✓ config.json exists")
        config = Util.get_config()
        
        if config.get("solverKey"):
            key = config["solverKey"]
            if key == "YOUR_FUNBYPASS_API_KEY_HERE":
                print("⚠️  config.json exists but API key is placeholder")
            else:
                print(f"✓ FunBypass API key configured: {key[:10]}...")
        else:
            print("⚠️  No solverKey in config.json")
    else:
        print("✗ config.json not found")
    
    # Check proxy file
    proxy_files = ["proxies.txt", "input/proxies.txt"]
    found_proxies = False
    
    for proxy_file in proxy_files:
        if os.path.exists(proxy_file):
            with open(proxy_file, 'r') as f:
                lines = [l.strip() for l in f.readlines() if l.strip() and not l.strip().startswith('#')]
                if lines:
                    print(f"✓ {proxy_file}: {len(lines)} proxies found")
                    found_proxies = True
                else:
                    print(f"⚠️  {proxy_file} exists but is empty")
    
    if not found_proxies:
        print("⚠️  No proxy files found (proxies.txt or input/proxies.txt)")
        print("   Proxies are recommended for best performance")
    
    print("="*60)

def test_dependencies():
    """Test that required dependencies are installed"""
    print("\n" + "="*60)
    print("Dependency Tests")
    print("="*60)
    
    deps = [
        ("colorama", "Colored console output"),
        ("cryptography", "Authentication signature generation"),
        ("requests", "HTTP requests (fallback)"),
    ]
    
    optional_deps = [
        ("curl_cffi", "HTTP requests with browser impersonation (optional)"),
        ("tkinter", "GUI interface (optional, use main_console.py if not available)"),
    ]
    
    all_required = True
    
    # Test required dependencies
    for module, description in deps:
        try:
            __import__(module)
            print(f"✓ {module:20s} - {description}")
        except ImportError:
            print(f"✗ {module:20s} - {description} (REQUIRED)")
            all_required = False
    
    # Test optional dependencies
    for module, description in optional_deps:
        try:
            __import__(module)
            print(f"✓ {module:20s} - {description}")
        except ImportError:
            print(f"⚠️  {module:20s} - {description}")
    
    print("="*60)
    
    if not all_required:
        print("❌ Some required dependencies are missing")
        print("   Run: pip install -r requirements.txt")
        return 1
    else:
        print("✅ All required dependencies installed")
        return 0

def main():
    """Run all tests"""
    print("\n🧪 Running Roblox Auto-Group Joiner Tests\n")
    
    results = []
    
    # Run tests
    results.append(test_imports())
    test_config()
    results.append(test_dependencies())
    
    # Final summary
    print("\n" + "="*60)
    if all(r == 0 for r in results):
        print("✅ ALL TESTS PASSED")
        print("\nYou can now run the script:")
        print("  GUI version:     python main.py")
        print("  Console version: python main_console.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("\nPlease fix the issues above before running the script.")
        return 1
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
