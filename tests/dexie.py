import pytest

import dexie


def test_bleak():
    dc = dexie.Dexie(base_url="https://api.dexie.space")
    assert dc
