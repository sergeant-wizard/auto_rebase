import argparse
import os
import tempfile

import git
import requests


class AutoRebase:
    def __init__(
        self, g: git.cmd.Git, host: str, repository: str, user_id: str
    ):
        self._git = git
        self._host = host
        self._repository = repository
        self._user_id = user_id
        self._git.fetch('origin')

    def patch_diff_from_master(self, branch: str) -> str:
        base = self._git.merge_base(branch, 'origin/master')
        return self.patch_diff(base, branch)

    def patch_diff(self, commit1: str, commit2: str) -> str:
        with tempfile.TemporaryFile('w') as f:
            f.write(self._git.diff(commit1, commit2))
            f.seek(0)
            return self._git.execute(['git', 'patch-id'], istream=f)

    def rebase(self, base: str) -> bool:
        try:
            self._git.rebase(base)
        except git.exc.GitCommandError as e:
            if e.status == 128:
                return False
            else:
                raise e
        finally:
            try:
                self._git.rebase('--abort')
            except git.exc.GitCommandError:
                pass
        return True

    def rebase_with_check(self, branch: str):
        remote_branch = f'origin/{branch}'
        self._git.checkout(branch)
        if not self.rebase(remote_branch):
            print(f'skipping branch {branch} due to rebase error to {remote_branch}')  # NOQA
            return False
        if not self.rebase('origin/master'):
            print(f'skipping branch {branch} due to rebase error to master')
            return False
        if self._git.rev_parse(branch) == self._git.rev_parse(remote_branch):
            print(f'branch {branch} is up to date')
            return False
        remote_patch_diff = self.patch_diff_from_master(remote_branch)
        local_patch_diff = self.patch_diff_from_master(remote_branch)
        if remote_patch_diff == local_patch_diff:
            print(f'branch {branch} ready')
            return True
        else:
            print(f'branch {branch} has patch diffs')
            return False

    def get_pull_requests(self):
        assert 'GITHUB_REPO_TOKEN' in os.environ.keys()
        access_params = {
            'access_token': os.environ['GITHUB_REPO_TOKEN'],
            'per_page': 100,
            'state': 'open',
        }
        base_url = f'{self._host}/api/v3'

        url = f'{base_url}/repos/{self._repo}/pulls'
        res = requests.get(url, params=access_params)
        return [
            pr['head']['ref'] for pr in res.json()
            if pr['user']['id'] == self._user_id
        ]

    def rebase_all(self):
        for branch in self.get_pull_requests():
            self.rebase_with_check(branch)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host', default='https://github.com')
    parser.add_argument('repository', default='sergeant-wizard/auto_rebase')
    parser.add_argument('user_id')
    parser.add_argument('path')
    args = parser.parse_args()

    AutoRebase(
        g=git.cmd.Git(args.path),
        host=args.host,
        repository=args.repository,
        user_id=args.user_id,
    ).rebase_all()
