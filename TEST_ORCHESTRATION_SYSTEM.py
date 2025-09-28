#!/usr/bin/env python3
"""
TEST ORCHESTRATION SYSTEM
Comprehensive testing suite for the Billionaire Consciousness Orchestration System
"""

import os
import json
import subprocess
import sys
import time
import unittest
from datetime import datetime
from typing import Dict, List, Any

class OrchestrationSystemTester:
    def __init__(self):
        self.test_results = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def run_test(self, test_name: str, test_function) -> bool:
        """Run a single test and record results"""
        self.total_tests += 1
        print(f"🧪 Running test: {test_name}")
        
        try:
            result = test_function()
            if result:
                self.passed_tests += 1
                print(f"✅ PASSED: {test_name}")
                return True
            else:
                self.failed_tests += 1
                print(f"❌ FAILED: {test_name}")
                return False
        except Exception as e:
            self.failed_tests += 1
            print(f"❌ ERROR in {test_name}: {str(e)}")
            return False
    
    def test_orchestrator_import(self) -> bool:
        """Test if orchestrator can be imported"""
        try:
            from BILLIONAIRE_CONSCIOUSNESS_ORCHESTRATION_COMPLETE import BillionaireConsciousnessOrchestrator
            orchestrator = BillionaireConsciousnessOrchestrator()
            return True
        except ImportError as e:
            print(f"Import error: {e}")
            return False
        except Exception as e:
            print(f"Initialization error: {e}")
            return False
    
    def test_session_system_import(self) -> bool:
        """Test if session system can be imported"""
        try:
            from SESSION_AWARE_ORCHESTRATION_SYSTEM import SessionOrchestrator, SessionManager
            return True
        except ImportError as e:
            print(f"Session system import error: {e}")
            return False
        except Exception as e:
            print(f"Session system error: {e}")
            return False
    
    def test_integration_system_import(self) -> bool:
        """Test if integration system can be imported"""
        try:
            from COMPLETE_ORCHESTRATION_INTEGRATION import CompleteOrchestrationIntegration
            integrator = CompleteOrchestrationIntegration()
            return True
        except ImportError as e:
            print(f"Integration system import error: {e}")
            return False
        except Exception as e:
            print(f"Integration system error: {e}")
            return False
    
    def test_github_connectivity(self) -> bool:
        """Test GitHub API connectivity"""
        try:
            result = subprocess.run([
                'gh', 'auth', 'status'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                return True
            else:
                print(f"GitHub auth error: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("GitHub connectivity timeout")
            return False
        except Exception as e:
            print(f"GitHub connectivity error: {e}")
            return False
    
    def test_repository_verification(self) -> bool:
        """Test repository verification"""
        try:
            result = subprocess.run([
                'gh', 'repo', 'list', 'Worldwidebro', '--limit', '10',
                '--json', 'name'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                repos = json.loads(result.stdout)
                return len(repos) > 0
            else:
                print(f"Repository verification error: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("Repository verification timeout")
            return False
        except Exception as e:
            print(f"Repository verification error: {e}")
            return False
    
    def test_orchestrator_functionality(self) -> bool:
        """Test orchestrator functionality"""
        try:
            from BILLIONAIRE_CONSCIOUSNESS_ORCHESTRATION_COMPLETE import BillionaireConsciousnessOrchestrator
            
            orchestrator = BillionaireConsciousnessOrchestrator()
            
            # Test initialization
            init_status = orchestrator.initialize_orchestration_system()
            
            # Check if initialization was successful
            if 'github_repos_verified' in init_status:
                return True
            else:
                print("Orchestrator initialization failed")
                return False
        except Exception as e:
            print(f"Orchestrator functionality error: {e}")
            return False
    
    def test_session_management(self) -> bool:
        """Test session management functionality"""
        try:
            from SESSION_AWARE_ORCHESTRATION_SYSTEM import SessionManager
            
            session_manager = SessionManager()
            
            # Test session registration
            test_session_id = f"test_{int(time.time())}"
            success = session_manager.register_session(test_session_id, "test_user")
            
            if success:
                # Test session update
                update_success = session_manager.update_session(
                    test_session_id, 
                    status='testing',
                    current_task='test_task',
                    progress=50.0
                )
                
                # Test session retrieval
                session = session_manager.get_session_status(test_session_id)
                
                return update_success and session is not None
            else:
                print("Session registration failed")
                return False
        except Exception as e:
            print(f"Session management error: {e}")
            return False
    
    def test_integration_system(self) -> bool:
        """Test integration system functionality"""
        try:
            from COMPLETE_ORCHESTRATION_INTEGRATION import CompleteOrchestrationIntegration
            
            integrator = CompleteOrchestrationIntegration()
            
            # Test initialization
            init_status = integrator.initialize_integration_system()
            
            # Check if initialization was successful
            if 'system_components' in init_status:
                return True
            else:
                print("Integration system initialization failed")
                return False
        except Exception as e:
            print(f"Integration system error: {e}")
            return False
    
    def test_cursor_rules(self) -> bool:
        """Test Cursor rules availability"""
        try:
            cursor_rules_dir = ".cursor/rules"
            if os.path.exists(cursor_rules_dir):
                rules_files = os.listdir(cursor_rules_dir)
                return len(rules_files) > 0
            else:
                print("Cursor rules directory not found")
                return False
        except Exception as e:
            print(f"Cursor rules error: {e}")
            return False
    
    def test_file_structure(self) -> bool:
        """Test essential file structure"""
        try:
            essential_files = [
                "BILLIONAIRE_CONSCIOUSNESS_ORCHESTRATION_COMPLETE.py",
                "SESSION_AWARE_ORCHESTRATION_SYSTEM.py",
                "COMPLETE_ORCHESTRATION_INTEGRATION.py",
                "PROMPTING_ORCHESTRATION_SYSTEM.md",
                "SAFE_CLEANUP_VERIFICATION_SYSTEM.py"
            ]
            
            missing_files = []
            for file in essential_files:
                if not os.path.exists(file):
                    missing_files.append(file)
            
            if missing_files:
                print(f"Missing files: {missing_files}")
                return False
            else:
                return True
        except Exception as e:
            print(f"File structure error: {e}")
            return False
    
    def test_system_health(self) -> bool:
        """Test overall system health"""
        try:
            # Check disk space
            result = subprocess.run(['df', '-h', '.'], capture_output=True, text=True)
            if result.returncode != 0:
                print("Disk space check failed")
                return False
            
            # Check network connectivity
            result = subprocess.run(['ping', '-c', '1', 'github.com'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                print("Network connectivity check failed")
                return False
            
            return True
        except Exception as e:
            print(f"System health error: {e}")
            return False
    
    def run_comprehensive_tests(self) -> Dict:
        """Run all tests and generate comprehensive report"""
        print("🧪 COMPREHENSIVE ORCHESTRATION SYSTEM TESTING")
        print("=" * 60)
        
        # Define test suite
        tests = [
            ("File Structure", self.test_file_structure),
            ("Cursor Rules", self.test_cursor_rules),
            ("System Health", self.test_system_health),
            ("GitHub Connectivity", self.test_github_connectivity),
            ("Repository Verification", self.test_repository_verification),
            ("Orchestrator Import", self.test_orchestrator_import),
            ("Session System Import", self.test_session_system_import),
            ("Integration System Import", self.test_integration_system_import),
            ("Orchestrator Functionality", self.test_orchestrator_functionality),
            ("Session Management", self.test_session_management),
            ("Integration System", self.test_integration_system)
        ]
        
        # Run all tests
        test_results = {}
        for test_name, test_function in tests:
            test_results[test_name] = self.run_test(test_name, test_function)
        
        # Generate comprehensive report
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': self.total_tests,
            'passed_tests': self.passed_tests,
            'failed_tests': self.failed_tests,
            'success_rate': (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0,
            'test_results': test_results,
            'system_status': 'healthy' if self.failed_tests == 0 else 'issues_detected'
        }
        
        # Save test report
        with open('orchestration_test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print(f"Success Rate: {report['success_rate']:.1f}%")
        print(f"System Status: {report['system_status']}")
        
        if self.failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for test_name, result in test_results.items():
                if not result:
                    print(f"  - {test_name}")
        
        print("\n📋 Detailed report saved to: orchestration_test_report.json")
        
        return report

def main():
    tester = OrchestrationSystemTester()
    report = tester.run_comprehensive_tests()
    
    # Return exit code based on test results
    if tester.failed_tests == 0:
        print("\n🎯 ALL TESTS PASSED! System is fully operational.")
        sys.exit(0)
    else:
        print(f"\n⚠️ {tester.failed_tests} tests failed. Please review and fix issues.")
        sys.exit(1)

if __name__ == "__main__":
    main()
