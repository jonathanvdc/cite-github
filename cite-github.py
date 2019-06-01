#!/usr/bin/env python3

import base64
import sys
from github import Github, Branch, Repository
from collections import defaultdict, OrderedDict
from datetime import date


class BibTexEntry(object):
    """A data structure that describes a BibTex entry."""

    def __init__(self, kind: str, name: str, fields: OrderedDict):
        self.kind = kind
        self.name = name
        self.fields = fields

    def __str__(self):
        return '@%s{%s,\n%s}' % (
            self.kind,
            self.name,
            ''.join([
                '\t%s={%s}\n' % pair
                for pair in self.fields.items()]))


def name_user(user):
    """Names a GitHub user, preferring IRL names but falling back to usernames
       if necessary."""
    irl_name = user.name
    return user.login if irl_name is None else irl_name


def get_contributors(repo: Repository, path: str, branch_name: str):
    """Gets a sorted list of contributors to a file in a repository."""
    commit_list = repo.get_commits(sha=branch_name, path=path)

    # Remove duplicate users and map users to their commit counts.
    unique_users = defaultdict(int)
    for commit in commit_list:
        unique_users[commit.author] += 1

    # Sort users by commit count, name them.
    return sorted(list(unique_users.keys()),
                  key=lambda user: unique_users[user], reverse=True)


def guess_title(repo: Repository, path: str, branch_name: str):
    """Guesses the title of a file in a repo or branch."""
    if path.endswith('.md'):
        # If we are dealing with a markdown file, then we will interpret
        # the first header in the file as the file's title.
        contents = repo.get_contents(path, ref=branch_name)
        text = base64.b64decode(contents.content).decode('UTF-8')
        lines = text.split('\n')
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#'):
                return stripped.strip('#').strip()

    # Turn the file name into a title.
    return path.split('/')[-1].split('.')[0].replace('-', ' ').replace('_', ' ').capitalize()


def name_entry(title: str, last_edit: date, contributors):
    """Names a BibTex entry based on its title, the date on which it was last edited,
       and a file's list of contributors."""
    first_named_contributor = None
    for contrib in contributors:
        if first_named_contributor is None and contrib.name is not None:
            first_named_contributor = contrib.name.split(' ')[-1].lower()

    if first_named_contributor is None:
        first_named_contributor = name_user(contributors[0]).lower()

    return '%s%d%s' % (title.split(' ')[0].lower(), last_edit.year, first_named_contributor)


def get_last_edit_date(repo: Repository, path: str, branch_name: str):
    """Gets a file's last edit date."""
    return max([commit.commit.author.date.date() for commit in repo.get_commits(sha=branch_name, path=path)])


def cite(repo: Repository, path: str, branch_name: str = None):
    """Cites a file at a particular path in a repository."""
    if branch_name is None:
        branch_name = repo.default_branch
    contrib_names = get_contributors(repo, path, branch_name)
    last_edit_date = get_last_edit_date(repo, path, branch_name)
    title = guess_title(repo, path, branch_name)
    fields = OrderedDict()
    fields['title'] = title
    fields['author'] = ' and '.join(map(name_user, contrib_names))
    fields['month'] = last_edit_date.strftime('%B')
    fields['year'] = str(last_edit_date.year)
    fields['howpublished'] = '\\url{%s/blob/%s/%s}' % (
        repo.html_url, branch_name, path)
    today = date.today()
    fields['note'] = 'Accessed on %s %d, %d.' % (
        today.strftime('%B'), today.day, today.year)
    return BibTexEntry('misc', name_entry(title, last_edit_date, contrib_names), fields)


def cite_url(gh: Github, url):
    """Cites a file based on its GitHub URL."""
    # GitHub file URLs are formatted as 'https://www.github.com/OWNER/REPO/blob/BRANCH/PATH...'
    url = url.strip('http://').strip('https://')
    pieces = url.split('/')
    repo_slug = '/'.join(pieces[1:3])
    branch_name = pieces[4]
    path = '/'.join(pieces[5:])

    repo = gh.get_repo(repo_slug)
    return cite(repo, path, branch_name)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: cite-github.py URL [token]')

    url = sys.argv[1]

    # Create a GitHub API object.
    if len(sys.argv) >= 3:
        gh = Github(sys.argv[2])
    else:
        gh = Github()

    # Cite the document.
    print(cite_url(gh, url))
