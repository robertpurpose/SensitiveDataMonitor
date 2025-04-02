import re
import os

# Simple sensitive data patterns
patterns = {
    "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
    "DOB": r"\b\d{2}/\d{2}/\d{4}\b",
    "HIPAA": r"(?i)patient|diagnosis|treatment|medical|health"
}

def scan_file(file_path):
    findings = []
    try:
        with open(file_path, 'r', errors='ignore') as f:
            content = f.read()
            for label, pattern in patterns.items():
                matches = re.findall(pattern, content)
                if matches:
                    findings.append((label, matches))
    except Exception as e:
        print(f"Error scanning {file_path}: {e}")
    return findings

def scan_directory(directory):
    report = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            path = os.path.join(root, filename)
            result = scan_file(path)
            if result:
                report[path] = result
    return report

if __name__ == "__main__":
    target_directory = input("Enter directory to scan: ")
    results = scan_directory(target_directory)
    for file, data in results.items():
        print(f"\nFile: {file}")
        for label, matches in data:
            print(f"  {label}: {matches}")
