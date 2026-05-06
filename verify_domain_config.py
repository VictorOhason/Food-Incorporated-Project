#!/usr/bin/env python3
"""
Domain Configuration Verification Script

This script verifies that your Food Incorporated application is properly
configured for domain-based deployment.

Usage:
    python verify_domain_config.py
"""

import os
import sys
import json
from pathlib import Path

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}{text}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ {text}{RESET}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print_success(f"{description}: {filepath}")
        return True
    else:
        print_error(f"{description} not found: {filepath}")
        return False

def check_file_contains(filepath, search_string, description):
    """Check if file contains a specific string"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if search_string in content:
                print_success(f"{description}")
                return True
            else:
                print_error(f"{description} (string not found)")
                return False
    except Exception as e:
        print_error(f"Error reading {filepath}: {e}")
        return False

def check_env_file(filepath):
    """Check .env file for required variables"""
    print(f"\nChecking {filepath}...")
    
    required_vars = {
        'API_PROTOCOL': 'API protocol configuration',
        'API_HOST': 'API host configuration',
        'API_PORT': 'API port configuration',
        'ALLOWED_ORIGINS': 'CORS origins configuration',
    }
    
    found_count = 0
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            for var_name, var_desc in required_vars.items():
                if var_name in content:
                    # Extract the value for display
                    for line in content.split('\n'):
                        if line.startswith(var_name):
                            print_success(f"{var_desc}: {line}")
                            found_count += 1
                            break
                else:
                    print_warning(f"Missing: {var_desc} ({var_name})")
    except FileNotFoundError:
        print_error(f".env file not found: {filepath}")
        return False
    except Exception as e:
        print_error(f"Error reading .env: {e}")
        return False
    
    if found_count == len(required_vars):
        return True
    else:
        print_warning(f"Found {found_count}/{len(required_vars)} required variables")
        return False

def main():
    print_header("Food Incorporated - Domain Configuration Verifier")
    
    # Get the project root directory
    script_dir = Path(__file__).parent.absolute()
    food_inc_dir = script_dir / "Food incorporated"
    kitchen_app_dir = food_inc_dir / "Kitchen_app"
    menu_dir = food_inc_dir / "Menu"
    
    results = {
        'config_files': [],
        'code_files': [],
        'env_config': [],
        'documentation': [],
        'total': 0,
        'passed': 0
    }
    
    print_header("1. Configuration Files")
    
    # Check config.js exists
    config_js = food_inc_dir / "config.js"
    if check_file_exists(config_js, "Frontend config.js"):
        results['config_files'].append(True)
    else:
        results['config_files'].append(False)
    results['total'] += 1
    
    # Check .env exists
    env_file = kitchen_app_dir / ".env"
    if check_file_exists(env_file, "Backend .env"):
        results['config_files'].append(True)
    else:
        results['config_files'].append(False)
    results['total'] += 1
    
    print_header("2. Code Updates")
    
    # Check menu.js uses CONFIG
    menu_js = menu_dir / "menu.js"
    if check_file_contains(menu_js, "CONFIG.ORDERS_URL", "menu.js uses CONFIG.ORDERS_URL"):
        results['code_files'].append(True)
    else:
        results['code_files'].append(False)
    results['total'] += 1
    
    # Check api.py uses environment variables
    api_py = kitchen_app_dir / "api.py"
    if check_file_contains(api_py, "os.getenv('API_HOST'", "api.py uses environment variables"):
        results['code_files'].append(True)
    else:
        results['code_files'].append(False)
    results['total'] += 1
    
    # Check server.py has security headers
    server_py = kitchen_app_dir / "server.py"
    if check_file_contains(server_py, "set_security_headers", "server.py has security headers"):
        results['code_files'].append(True)
    else:
        results['code_files'].append(False)
    results['total'] += 1
    
    # Check menu.html loads config.js
    menu_html = menu_dir / "menu.html"
    if check_file_contains(menu_html, "../config.js", "menu.html loads config.js"):
        results['code_files'].append(True)
    else:
        results['code_files'].append(False)
    results['total'] += 1
    
    # Check checkout.html loads config.js
    checkout_html = menu_dir / "checkout.html"
    if check_file_contains(checkout_html, "../config.js", "checkout.html loads config.js"):
        results['code_files'].append(True)
    else:
        results['code_files'].append(False)
    results['total'] += 1
    
    print_header("3. Environment Configuration")
    
    # Check .env file contents
    if check_env_file(env_file):
        results['env_config'].append(True)
    else:
        results['env_config'].append(False)
    results['total'] += 1
    
    print_header("4. Documentation")
    
    docs_to_check = [
        (food_inc_dir / "DOMAIN_CONFIGURATION.md", "Domain Configuration Guide"),
        (food_inc_dir / "CHANGES_SUMMARY.md", "Changes Summary"),
        (food_inc_dir / "QUICK_START.md", "Quick Start Guide"),
    ]
    
    for doc_path, doc_name in docs_to_check:
        if check_file_exists(doc_path, doc_name):
            results['documentation'].append(True)
        else:
            results['documentation'].append(False)
        results['total'] += 1
    
    print_header("Verification Summary")
    
    # Count passed checks
    for category in ['config_files', 'code_files', 'env_config', 'documentation']:
        passed = sum(results[category])
        total = len(results[category])
        if total > 0:
            results['passed'] += passed
            percentage = (passed / total) * 100
            if passed == total:
                print_success(f"{category.replace('_', ' ').title()}: {passed}/{total} ({percentage:.0f}%)")
            else:
                print_warning(f"{category.replace('_', ' ').title()}: {passed}/{total} ({percentage:.0f}%)")
    
    print()
    
    total_passed = results['passed']
    total_checks = results['total']
    percentage = (total_passed / total_checks) * 100 if total_checks > 0 else 0
    
    if percentage == 100:
        print_success(f"ALL CHECKS PASSED! {total_passed}/{total_checks} ({percentage:.0f}%)")
        print_info("Your application is ready for domain deployment!")
        return 0
    elif percentage >= 80:
        print_warning(f"MOSTLY COMPLETE: {total_passed}/{total_checks} ({percentage:.0f}%)")
        print_info("Review the failed checks above and update as needed.")
        return 1
    else:
        print_error(f"ISSUES FOUND: {total_passed}/{total_checks} ({percentage:.0f}%)")
        print_info("Review all failed checks above and follow the QUICK_START.md guide.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    
    print()
    print_header("Next Steps")
    
    print("""
1. Update your domain in .env:
   API_HOST=your-domain.com
   
2. Test in browser console:
   CONFIG.API_URL
   
3. Verify API health:
   curl https://your-domain.com/health
   
4. See QUICK_START.md for detailed deployment steps
""")
    
    sys.exit(exit_code)
