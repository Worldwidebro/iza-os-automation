#!/usr/bin/env python3
"""
SAFE CLEANUP VERIFICATION SYSTEM
Verifies GitHub commits before allowing file deletion to prevent data loss
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Tuple

class SafeCleanupVerifier:
    def __init__(self):
        self.github_org = "Worldwidebro"
        self.verification_log = []
        
    def verify_file_in_github(self, filename: str) -> Tuple[bool, str]:
        """Verify if a file exists in any GitHub repository"""
        try:
            # Search for file in all repositories
            result = subprocess.run([
                'gh', 'search', 'code', f'filename:{filename}', 
                '--owner', self.github_org, '--json', 'repository'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                if data:
                    repos = [repo['repository']['name'] for repo in data]
                    return True, f"Found in repositories: {', '.join(repos)}"
                else:
                    return False, "File not found in any GitHub repository"
            else:
                return False, f"Search failed: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, "Search timed out"
        except Exception as e:
            return False, f"Error searching: {str(e)}"
    
    def get_repository_contents(self, repo_name: str) -> List[str]:
        """Get list of files in a specific repository"""
        try:
            result = subprocess.run([
                'gh', 'api', f'repos/{self.github_org}/{repo_name}/contents',
                '--jq', '.[].name'
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                return result.stdout.strip().split('\n') if result.stdout.strip() else []
            else:
                return []
        except:
            return []
    
    def verify_multiple_files(self, filenames: List[str]) -> Dict[str, Tuple[bool, str]]:
        """Verify multiple files at once"""
        results = {}
        for filename in filenames:
            print(f"Verifying {filename}...")
            results[filename] = self.verify_file_in_github(filename)
        return results
    
    def safe_cleanup_with_verification(self, files_to_cleanup: List[str]) -> Dict:
        """Perform safe cleanup with GitHub verification"""
        print("=== SAFE CLEANUP WITH GITHUB VERIFICATION ===")
        print(f"Verifying {len(files_to_cleanup)} files...")
        
        # Verify all files
        verification_results = self.verify_multiple_files(files_to_cleanup)
        
        # Categorize results
        safe_to_delete = []
        unsafe_to_delete = []
        
        for filename, (exists, message) in verification_results.items():
            if exists:
                safe_to_delete.append((filename, message))
                print(f"✅ SAFE: {filename} - {message}")
            else:
                unsafe_to_delete.append((filename, message))
                print(f"❌ UNSAFE: {filename} - {message}")
        
        # Generate report
        report = {
            'total_files': len(files_to_cleanup),
            'safe_to_delete': len(safe_to_delete),
            'unsafe_to_delete': len(unsafe_to_delete),
            'safe_files': safe_to_delete,
            'unsafe_files': unsafe_to_delete,
            'verification_timestamp': subprocess.run(['date'], capture_output=True, text=True).stdout.strip()
        }
        
        # Save verification log
        with open('cleanup_verification_log.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n=== VERIFICATION COMPLETE ===")
        print(f"Total files: {report['total_files']}")
        print(f"Safe to delete: {report['safe_to_delete']}")
        print(f"Unsafe to delete: {report['unsafe_to_delete']}")
        
        return report
    
    def restore_file_from_backup(self, filename: str) -> bool:
        """Attempt to restore a file from backup locations"""
        backup_locations = [
            f"backups/{filename}",
            f"backup/{filename}",
            f".git/objects/",
            f"__pycache__/{filename}",
            f"temp/{filename}"
        ]
        
        for location in backup_locations:
            if os.path.exists(location):
                try:
                    subprocess.run(['cp', location, filename], check=True)
                    print(f"✅ Restored {filename} from {location}")
                    return True
                except:
                    continue
        
        print(f"❌ Could not restore {filename} from any backup location")
        return False
    
    def commit_file_to_github(self, filename: str, target_repo: str) -> bool:
        """Commit a file to a specific GitHub repository"""
        try:
            # Clone repository if not exists
            if not os.path.exists(f"temp_repos/{target_repo}"):
                subprocess.run(['mkdir', '-p', 'temp_repos'], check=True)
                subprocess.run([
                    'gh', 'repo', 'clone', f'{self.github_org}/{target_repo}', 
                    f'temp_repos/{target_repo}'
                ], check=True)
            
            # Copy file to repository
            subprocess.run(['cp', filename, f'temp_repos/{target_repo}/'], check=True)
            
            # Commit and push
            os.chdir(f'temp_repos/{target_repo}')
            subprocess.run(['git', 'add', filename], check=True)
            subprocess.run(['git', 'commit', '-m', f'Add {filename} - orchestration system'], check=True)
            subprocess.run(['git', 'push'], check=True)
            
            os.chdir('/Users/divinejohns/memU')
            print(f"✅ Committed {filename} to {target_repo}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to commit {filename} to {target_repo}: {str(e)}")
            os.chdir('/Users/divinejohns/memU')
            return False

def main():
    verifier = SafeCleanupVerifier()
    
    # Files that were accidentally deleted
    deleted_files = [
        "BILLIONAIRE_CONSCIOUSNESS_ORCHESTRATION_COMPLETE.py",
        "SESSION_AWARE_ORCHESTRATION_SYSTEM.py",
        "COMPLETE_ORCHESTRATION_INTEGRATION.py",
        "PROMPTING_ORCHESTRATION_SYSTEM.md",
        "TEST_ORCHESTRATION_SYSTEM.py",
        "FINAL_TEST_RESULTS.md"
    ]
    
    print("=== SAFE CLEANUP VERIFICATION SYSTEM ===")
    print("This system prevents accidental deletion of uncommitted files")
    
    # Test verification system
    test_files = ["README.md", "package.json"]  # Common files that should exist
    print("\n=== TESTING VERIFICATION SYSTEM ===")
    verifier.verify_multiple_files(test_files)
    
    print("\n=== CHECKING DELETED FILES ===")
    verifier.verify_multiple_files(deleted_files)

if __name__ == "__main__":
    main()
