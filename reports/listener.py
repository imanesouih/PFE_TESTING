import os
import threading
import datetime
from jinja2 import Environment, FileSystemLoader
import sys
import yaml

class listener:
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, report_file='koko.html', template_file='./reports/template.html'):
        self.report_file = report_file
        self.template_file = template_file
        self.total_tests = 0
        self.total_passed = 0
        self.total_failed = 0
        self.total_skipped = 0
        self.suite_stats = {}
        self.test_details = []
        self.is_closed = False
        self.lock = threading.Lock()
        if '--variablefile' in sys.argv:
                    index = sys.argv.index('--variablefile')
                    env_file = sys.argv[index + 1]
                    try:
                        # Charger les informations d'environnement à partir du fichier YAML correspondant
                        with open(env_file, 'r') as yaml_file:
                            self.env_info = yaml.safe_load(yaml_file)
                    except FileNotFoundError:
                        print(f"Error: File '{env_file}' not found.")
                    except Exception as e:
                        print(f"Error loading YAML file: {e}")
        

    def start_suite(self, suite, result):
        suite_name = suite.name
        if suite.source and suite.source.lower().endswith('.robot'):
            start_time = datetime.datetime.now()
            self.suite_stats[suite_name] = {
                'total_tests': 0,
                'passed': 0,
                'failed': 0,
                'skipped': 0,
                'start_time': start_time.strftime("%Y-%m-%d %H:%M:%S"),
                'status': 'Running',
                'project_key': self.env_info.get('project_key', 'N/A'),
                'environment': self.env_info.get('environment', 'N/A'),
                'testeur': self.env_info.get('Testeur', 'N/A')
            }

    def end_suite(self, suite, result):
        suite_name = suite.name
        if suite.source and suite.source.lower().endswith('.robot') and suite.tests:
            end_time = datetime.datetime.now()
            start_time = datetime.datetime.strptime(self.suite_stats[suite_name]['start_time'], "%Y-%m-%d %H:%M:%S")
            elapsed_time = end_time - start_time
            self.suite_stats[suite_name]['end_time'] = end_time.strftime("%Y-%m-%d %H:%M:%S")
            self.suite_stats[suite_name]['elapsed_time'] = str(elapsed_time)
            self.suite_stats[suite_name]['status'] = 'Finished'

    def end_test(self, test, result):
        suite_name = test.parent.name
        if suite_name in self.suite_stats:
            test_name = test.name
            test_status = "PASS" if result.passed else "FAIL"
            message = result.message if not result.passed else ""
            
            # Extract tags from the test
            tags = [tag for tag in test.tags if tag.startswith('FT-')]

            # Generate Jira links based on tags
            jira_links = [f'<a href="https://imanesouih.atlassian.net/browse/{tag}">{tag}</a>' for tag in tags]

            self.test_details.append((suite_name, test_name, test_status, message, jira_links))
            
            self.suite_stats[suite_name]['total_tests'] += 1
            if result.passed:
                self.suite_stats[suite_name]['passed'] += 1
            else:
                self.suite_stats[suite_name]['failed'] += 1
            if result.skipped:
                self.suite_stats[suite_name]['skipped'] += 1
            self.total_tests += 1
            if result.passed:
                self.total_passed += 1
            else:
                self.total_failed += 1
            if result.skipped:
                self.total_skipped += 1

        self.update_report()

    def close(self):
        if not self.is_closed:
            with self.lock:
                if not self.is_closed:
                    self.is_closed = True
                    self.update_report()

    def update_report(self):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template(self.template_file)

        rendered_template = template.render(
            total_tests=self.total_tests,
            total_passed=self.total_passed,
            total_failed=self.total_failed,
            total_skipped=self.total_skipped,
            suite_stats=self.suite_stats,
            test_details=self.test_details,
            env_info=self.env_info
        )

        with open(self.report_file, 'w') as f:
            f.write(rendered_template)
