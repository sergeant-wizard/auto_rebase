import os

import git

import auto_rebase

base_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.path.pardir,
))


def test_patch_diff():
    branch_1, branch_2 = [f'origin/test/edit_a_{idx}' for idx in range(1, 3)]
    g = git.cmd.Git(base_dir)
    ar = auto_rebase.AutoRebase(g)
    repo = git.Repo(base_dir)

    assert repo.commit(branch_1) != repo.commit(branch_2)

    diff1 = ar.patch_diff(branch_1)
    diff2 = ar.patch_diff(branch_2)
    assert diff1 == diff2
