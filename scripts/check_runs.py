import urllib.request
import json
import sys


def get_workflow_runs():
    url = "https://api.github.com/repos/rajshekar321/ai-devops/actions/runs"
    req = urllib.request.Request(url, headers={"User-Agent": "AI-DevOps-Checker"})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            print(f"Total Workflow Runs: {data.get('total_count', 0)}\n")
            for run in data.get("workflow_runs", []):
                print(f"Run #{run.get('run_number')}: {run.get('name')}")
                print(f"  Event:       {run.get('event')}")
                print(f"  Status:      {run.get('status')}")
                print(f"  Conclusion:  {run.get('conclusion')}")
                print(f"  Commit:      {run.get('head_sha')[:7]} - {run.get('head_commit', {}).get('message', '').strip().splitlines()[0]}")
                print(f"  URL:         {run.get('html_url')}")
                
                # Fetch job details
                jobs_url = run.get('jobs_url')
                if jobs_url:
                    try:
                        jreq = urllib.request.Request(jobs_url, headers={"User-Agent": "AI-DevOps-Checker"})
                        with urllib.request.urlopen(jreq) as jresp:
                            jdata = json.loads(jresp.read().decode("utf-8"))
                            for job in jdata.get('jobs', []):
                                print(f"    Job: {job.get('name')} -> {job.get('conclusion')}")
                                for step in job.get('steps', []):
                                    print(f"      Step: {step.get('name')} [{step.get('conclusion')}]")
                    except Exception as je:
                        print(f"    Could not load jobs: {je}")
                print("-" * 50)
    except Exception as e:
        print(f"Error fetching workflow runs: {e}", file=sys.stderr)


if __name__ == "__main__":
    get_workflow_runs()
