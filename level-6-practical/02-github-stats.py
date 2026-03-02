"""
Level 6 - Exercise 02: GitHub Stats Fetcher
=============================================

Difficulty: 3/5 stars
Estimated time: 20 minutes

Fetch public GitHub repository or user statistics using the GitHub
REST API (no authentication needed for public data).

Includes a DEMO MODE with mock data so the script can run without
network access.

Features
--------
- Fetch user profile info (repos, followers, bio).
- Fetch repository stats (stars, forks, language, issues).
- List a user's most-starred repositories.
- Pretty-print results to the console.

Usage:
    python3 02-github-stats.py user octocat
    python3 02-github-stats.py repo python/cpython
    python3 02-github-stats.py user torvalds --demo

Expected output (demo mode):
-----------------------------
    GitHub User: octocat
    -------------------------
    Name      : The Octocat
    Bio       : I'm a cat that codes
    Public repos : 8
    Followers    : 12345
    Following    : 9
"""

import argparse
import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------
MOCK_USERS = {
    "octocat": {
        "login": "octocat",
        "name": "The Octocat",
        "bio": "I'm a cat that codes",
        "public_repos": 8,
        "followers": 12345,
        "following": 9,
        "html_url": "https://github.com/octocat",
        "created_at": "2011-01-25T18:44:36Z",
        "location": "San Francisco",
        "company": "@github",
    },
    "torvalds": {
        "login": "torvalds",
        "name": "Linus Torvalds",
        "bio": None,
        "public_repos": 7,
        "followers": 200000,
        "following": 0,
        "html_url": "https://github.com/torvalds",
        "created_at": "2011-09-03T15:26:22Z",
        "location": "Portland, OR",
        "company": "Linux Foundation",
    },
}

MOCK_REPOS = {
    "python/cpython": {
        "full_name": "python/cpython",
        "description": "The Python programming language",
        "html_url": "https://github.com/python/cpython",
        "stargazers_count": 58000,
        "forks_count": 28000,
        "open_issues_count": 7500,
        "language": "Python",
        "license": {"name": "Other"},
        "created_at": "2017-02-10T19:23:51Z",
        "updated_at": "2025-03-01T12:00:00Z",
        "default_branch": "main",
        "size": 950000,
    },
    "torvalds/linux": {
        "full_name": "torvalds/linux",
        "description": "Linux kernel source tree",
        "html_url": "https://github.com/torvalds/linux",
        "stargazers_count": 170000,
        "forks_count": 52000,
        "open_issues_count": 350,
        "language": "C",
        "license": {"name": "GPL-2.0"},
        "created_at": "2011-09-04T22:48:12Z",
        "updated_at": "2025-03-01T10:00:00Z",
        "default_branch": "master",
        "size": 4200000,
    },
}

MOCK_USER_REPOS = {
    "octocat": [
        {"name": "Hello-World", "stargazers_count": 2500, "language": "Python",
         "fork": False, "description": "My first repository on GitHub!"},
        {"name": "Spoon-Knife", "stargazers_count": 12000, "language": None,
         "fork": False, "description": "This repo is for demonstration purposes"},
        {"name": "octocat.github.io", "stargazers_count": 300, "language": "HTML",
         "fork": False, "description": "Personal page"},
        {"name": "git-consortium", "stargazers_count": 15, "language": "Ruby",
         "fork": True, "description": "A consortium of git users"},
    ],
}


# ---------------------------------------------------------------------------
# GitHub API Client
# ---------------------------------------------------------------------------
API_BASE = "https://api.github.com"


def github_get(endpoint: str, demo: bool = False, mock_data=None) -> dict | list:
    """Make a GET request to the GitHub API.

    Parameters
    ----------
    endpoint : str
        API path (e.g. "/users/octocat").
    demo : bool
        If True, return mock_data instead of making a real request.
    mock_data : dict or list or None
        Data to return in demo mode.
    """
    if demo:
        if mock_data is not None:
            return mock_data
        raise ValueError(f"No mock data for endpoint: {endpoint}")

    url = f"{API_BASE}{endpoint}"
    req = Request(url, headers={
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "PythonGitHubStats/1.0",
    })
    try:
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        if exc.code == 404:
            print(f"Not found: {endpoint}")
        elif exc.code == 403:
            print("Rate limited. Try again later or use --demo.")
        else:
            print(f"HTTP error {exc.code}: {exc.reason}")
        sys.exit(1)
    except URLError as exc:
        print(f"Network error: {exc}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------
def show_user(username: str, demo: bool = False) -> None:
    """Fetch and display a GitHub user's profile."""
    mock = MOCK_USERS.get(username.lower()) if demo else None
    if demo and mock is None:
        mock = {
            "login": username, "name": username.title(), "bio": "N/A",
            "public_repos": 0, "followers": 0, "following": 0,
            "html_url": f"https://github.com/{username}",
            "created_at": "N/A", "location": "N/A", "company": "N/A",
        }
    data = github_get(f"/users/{username}", demo=demo, mock_data=mock)

    header = f"GitHub User: {data['login']}"
    print(f"\n{header}")
    print("-" * len(header))
    print(f"  Name         : {data.get('name', 'N/A')}")
    print(f"  Bio          : {data.get('bio') or 'N/A'}")
    print(f"  Company      : {data.get('company') or 'N/A'}")
    print(f"  Location     : {data.get('location') or 'N/A'}")
    print(f"  Public repos : {data.get('public_repos', 0)}")
    print(f"  Followers    : {data.get('followers', 0)}")
    print(f"  Following    : {data.get('following', 0)}")
    print(f"  Profile      : {data.get('html_url', '')}")
    print(f"  Joined       : {data.get('created_at', 'N/A')}")
    print()

    # Also show top repos
    mock_repos = MOCK_USER_REPOS.get(username.lower(), []) if demo else None
    repos = github_get(
        f"/users/{username}/repos?sort=stars&per_page=5",
        demo=demo,
        mock_data=mock_repos,
    )
    if repos:
        print(f"  Top Repositories (by stars):")
        for repo in sorted(repos, key=lambda r: r.get("stargazers_count", 0),
                           reverse=True)[:5]:
            stars = repo.get("stargazers_count", 0)
            lang = repo.get("language") or "N/A"
            desc = repo.get("description") or ""
            fork_tag = " [fork]" if repo.get("fork") else ""
            print(f"    {repo['name']}{fork_tag} - {stars} stars ({lang})")
            if desc:
                print(f"      {desc[:70]}")
    print()


def show_repo(full_name: str, demo: bool = False) -> None:
    """Fetch and display a GitHub repository's stats."""
    mock = MOCK_REPOS.get(full_name.lower()) if demo else None
    if demo and mock is None:
        mock = {
            "full_name": full_name, "description": "N/A",
            "html_url": f"https://github.com/{full_name}",
            "stargazers_count": 0, "forks_count": 0,
            "open_issues_count": 0, "language": "N/A",
            "license": None, "created_at": "N/A", "updated_at": "N/A",
            "default_branch": "main", "size": 0,
        }
    owner, repo = full_name.split("/", 1)
    data = github_get(f"/repos/{owner}/{repo}", demo=demo, mock_data=mock)

    header = f"GitHub Repo: {data['full_name']}"
    print(f"\n{header}")
    print("-" * len(header))
    print(f"  Description  : {data.get('description') or 'N/A'}")
    print(f"  Language     : {data.get('language') or 'N/A'}")
    print(f"  Stars        : {data.get('stargazers_count', 0):,}")
    print(f"  Forks        : {data.get('forks_count', 0):,}")
    print(f"  Open issues  : {data.get('open_issues_count', 0):,}")
    lic = data.get("license")
    print(f"  License      : {lic['name'] if lic else 'N/A'}")
    print(f"  Branch       : {data.get('default_branch', 'N/A')}")
    size_mb = (data.get("size", 0) or 0) / 1024
    print(f"  Size         : {size_mb:.1f} MB")
    print(f"  URL          : {data.get('html_url', '')}")
    print(f"  Created      : {data.get('created_at', 'N/A')}")
    print(f"  Last updated : {data.get('updated_at', 'N/A')}")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch GitHub user or repository statistics."
    )
    parser.add_argument(
        "command",
        choices=["user", "repo"],
        help="What to look up: 'user' or 'repo'",
    )
    parser.add_argument(
        "target",
        help="Username (e.g. octocat) or owner/repo (e.g. python/cpython)",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Use mock data (no network required)",
    )
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.demo:
        print("[DEMO MODE] Using mock GitHub data.\n")

    if args.command == "user":
        show_user(args.target, demo=args.demo)
    elif args.command == "repo":
        if "/" not in args.target:
            print("Error: repo target must be in 'owner/repo' format.")
            sys.exit(1)
        show_repo(args.target, demo=args.demo)


# ===================================================================
# Demo / self-test
# ===================================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No arguments provided. Running full demo...\n")
        print("=" * 60)
        print("USER: octocat")
        print("=" * 60)
        show_user("octocat", demo=True)

        print("=" * 60)
        print("USER: torvalds")
        print("=" * 60)
        show_user("torvalds", demo=True)

        print("=" * 60)
        print("REPO: python/cpython")
        print("=" * 60)
        show_repo("python/cpython", demo=True)

        print("=" * 60)
        print("REPO: torvalds/linux")
        print("=" * 60)
        show_repo("torvalds/linux", demo=True)
    else:
        main()
