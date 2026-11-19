import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.github.com"
LOGIN = "OmerFarukOruc"
FLAKE_OWNER = "OmerFarukOruc"
FLAKE_NAME = "nixos-config"
SKILLS_PATH = "agents/skills"
WEEKS = 52
WEEKS_PER_QUERY = 4
OUTPUT = Path(__file__).resolve().parent.parent / "data" / "activity.json"


def call(token: str, path: str, payload: dict | None = None) -> dict:
    request = urllib.request.Request(
        API + path,
        data=json.dumps(payload).encode() if payload else None,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        sys.exit(
            f"GitHub answered {error.code} for {path.partition('?')[0]}; Retry-After is "
            f"{error.headers.get('Retry-After')} and the rate limit resets at {error.headers.get('X-RateLimit-Reset')}."
        )


def graphql(token: str, query: str) -> dict:
    body = call(token, "/graphql", {"query": query})
    if "errors" in body:
        sys.exit(f"GraphQL refused a query: {body['errors'][0]['message']}")
    return body["data"]


def merged_pull_requests(token: str, since: datetime.date) -> int:
    query = f"author:{LOGIN} is:pr is:merged is:public merged:>={since}"
    body = call(token, "/search/issues?per_page=1&q=" + urllib.parse.quote(query))
    if body["incomplete_results"]:
        sys.exit("GitHub search returned an incomplete result, so no count was written.")
    return body["total_count"]


def flake_counts(token: str) -> tuple[int, int]:
    repository = graphql(
        token,
        f'query {{ repository(owner: "{FLAKE_OWNER}", name: "{FLAKE_NAME}") {{ '
        "defaultBranchRef { target { ... on Commit { history { totalCount } } } } "
        f'object(expression: "HEAD:{SKILLS_PATH}") {{ ... on Tree {{ entries {{ type }} }} }} }} }}',
    )["repository"]
    flake = f"{FLAKE_OWNER}/{FLAKE_NAME}"
    if not repository or not repository["defaultBranchRef"]:
        sys.exit(f"{flake} was not found or has no default branch.")
    if not repository["object"] or "entries" not in repository["object"]:
        sys.exit(f"{flake} has no folder {SKILLS_PATH} on its default branch.")
    commits = repository["defaultBranchRef"]["target"]["history"]["totalCount"]
    skills = sum(entry["type"] == "tree" for entry in repository["object"]["entries"])
    return commits, skills


def weeks(token: str, mondays: list[datetime.date]) -> list[dict]:
    fields = (
        "totalCommitContributions totalPullRequestContributions "
        "totalIssueContributions restrictedContributionsCount"
    )
    result = []
    for first in range(0, len(mondays), WEEKS_PER_QUERY):
        days = mondays[first : first + WEEKS_PER_QUERY]
        parts = " ".join(
            f'w{index}: contributionsCollection(from: "{day}T00:00:00Z", '
            f'to: "{day + datetime.timedelta(days=6)}T23:59:59Z") {{ {fields} }}'
            for index, day in enumerate(days)
        )
        user = graphql(token, f'query {{ user(login: "{LOGIN}") {{ {parts} }} }}')["user"]
        if not user:
            sys.exit(f"GitHub has no user {LOGIN}.")
        for index, day in enumerate(days):
            week = user[f"w{index}"]
            result.append(
                {
                    "week": str(day),
                    "commits": week["totalCommitContributions"],
                    "pull_requests": week["totalPullRequestContributions"],
                    "issues": week["totalIssueContributions"],
                    "private": week["restrictedContributionsCount"],
                }
            )
    return result


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("Set GITHUB_TOKEN to a GitHub token before running this script.")
    today = datetime.datetime.now(datetime.timezone.utc).date()
    this_monday = today - datetime.timedelta(days=today.weekday())
    mondays = [this_monday - datetime.timedelta(weeks=WEEKS - 1 - index) for index in range(WEEKS)]
    commits, skills = flake_counts(token)
    activity = {
        "numbers": {
            "pull_requests": merged_pull_requests(token, mondays[0]),
            "flake_commits": commits,
            "skills": skills,
        },
        "weeks": weeks(token, mondays),
    }
    draft = OUTPUT.with_suffix(".json.part")
    draft.write_text(json.dumps(activity, indent=1) + "\n", encoding="utf-8", newline="\n")
    os.replace(draft, OUTPUT)


if __name__ == "__main__":
    main()
