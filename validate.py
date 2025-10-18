#!/usr/bin/env python3

import sys
import os
import ast


def check_python_syntax(filepath):
    try:
        with open(filepath, 'r') as f:
            ast.parse(f.read())
        return True, None
    except SyntaxError as e:
        return False, str(e)


def validate_project():
    print("=" * 60)
    print("Jason Project Validation")
    print("=" * 60)
    
    python_files = [
        "jason.py",
        "config.py",
        "scouting.py",
        "scraping.py",
        "training.py",
        "finalizing.py",
        "__init__.py",
        "setup.py",
        "example_usage.py",
        "test_structure.py",
    ]
    
    other_files = [
        "requirements.txt",
        "README.md",
        "USAGE.md",
        ".env.example",
        ".gitignore",
        "quick_start.sh",
    ]
    
    print("\n1. Checking Python file syntax...")
    all_valid = True
    for file in python_files:
        if os.path.exists(file):
            valid, error = check_python_syntax(file)
            if valid:
                print(f"  ✓ {file}")
            else:
                print(f"  ✗ {file}: {error}")
                all_valid = False
        else:
            print(f"  ✗ {file}: File not found")
            all_valid = False
    
    print("\n2. Checking other required files...")
    for file in other_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file}: File not found")
            all_valid = False
    
    print("\n3. Checking file executability...")
    executable_files = ["jason.py", "quick_start.sh", "example_usage.py", "test_structure.py"]
    for file in executable_files:
        if os.path.exists(file):
            is_executable = os.access(file, os.X_OK)
            if is_executable:
                print(f"  ✓ {file} is executable")
            else:
                print(f"  ⚠ {file} is not executable (this is optional)")
        else:
            print(f"  ✗ {file}: File not found")
            all_valid = False
    
    print("\n4. Checking project structure...")
    expected_structure = {
        "Core modules": [
            "jason.py",
            "config.py",
            "scouting.py",
            "scraping.py",
            "training.py",
            "finalizing.py",
        ],
        "Documentation": [
            "README.md",
            "USAGE.md",
        ],
        "Configuration": [
            ".env.example",
            ".gitignore",
            "requirements.txt",
            "setup.py",
        ],
        "Utilities": [
            "quick_start.sh",
            "example_usage.py",
            "test_structure.py",
        ],
    }
    
    for category, files in expected_structure.items():
        missing = [f for f in files if not os.path.exists(f)]
        if not missing:
            print(f"  ✓ {category}: All files present")
        else:
            print(f"  ✗ {category}: Missing {', '.join(missing)}")
            all_valid = False
    
    print("\n5. Checking configuration completeness...")
    try:
        with open("config.py", 'r') as f:
            config_content = f.read()
            required_classes = [
                "ScoutingConfig",
                "ScrapingConfig",
                "TrainingConfig",
                "JasonConfig",
            ]
            for cls in required_classes:
                if f"class {cls}" in config_content:
                    print(f"  ✓ {cls} defined")
                else:
                    print(f"  ✗ {cls} not found")
                    all_valid = False
    except Exception as e:
        print(f"  ✗ Error checking config: {e}")
        all_valid = False
    
    print("\n6. Verifying phase implementation...")
    phase_files = {
        "Phase 1 (Scouting)": "scouting.py",
        "Phase 2 (Scraping)": "scraping.py",
        "Phase 3 (Training)": "training.py",
        "Phase 4 (Finalizing)": "finalizing.py",
    }
    
    for phase, file in phase_files.items():
        if os.path.exists(file):
            size = os.path.getsize(file)
            if size > 500:
                print(f"  ✓ {phase}: Implemented ({size} bytes)")
            else:
                print(f"  ⚠ {phase}: File too small ({size} bytes)")
        else:
            print(f"  ✗ {phase}: File not found")
            all_valid = False
    
    print("\n7. Checking requirements.txt...")
    try:
        with open("requirements.txt", 'r') as f:
            requirements = f.read()
            required_packages = [
                "praw",
                "torch",
                "transformers",
                "tqdm",
                "python-dotenv",
            ]
            for package in required_packages:
                if package in requirements:
                    print(f"  ✓ {package} listed")
                else:
                    print(f"  ✗ {package} missing")
                    all_valid = False
    except Exception as e:
        print(f"  ✗ Error checking requirements: {e}")
        all_valid = False
    
    print("\n" + "=" * 60)
    if all_valid:
        print("✓ PROJECT VALIDATION PASSED")
        print("=" * 60)
        print("\nThe Jason project is properly structured and ready to use!")
        print("\nNext steps:")
        print("1. Run: ./quick_start.sh")
        print("2. Edit .env with your Reddit API credentials")
        print("3. Run: python3 jason.py")
        return 0
    else:
        print("✗ PROJECT VALIDATION FAILED")
        print("=" * 60)
        print("\nSome issues were found. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(validate_project())
