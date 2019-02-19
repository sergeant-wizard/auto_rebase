import os

import git

import auto_rebase

base_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.path.pardir,
))


def test_patch_diff():
    branch_1, branch_2 = [f'origin/edit_a_{idx}' for idx in range(1, 3)]
    g = git.cmd.Git(base_dir)
    ar = auto_rebase.AutoRebase(g)
    repo = git.Repo(base_dir)
    assert repo.commit(branch_1) != repo.commit(branch_2)
    patch_diff_1 = ar.patch_diff(branch_1, branch_1 + '~')
    patch_diff_2 = ar.patch_diff(branch_2, branch_2 + '~')
    assert patch_diff_1 == patch_diff_2
