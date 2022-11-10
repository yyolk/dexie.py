import pytest

import dexie


@pytest.fixture
def dexie_test_client():
    return dexie.Dexie(base_url=DEXIE_MAINNET)


DEXIE_MAINNET = "https://api.dexie.space"
DEXIE_TESTNET = "https://api-testnet.dexie.space"


def test_bleak():
    dc = dexie.Dexie(base_url=DEXIE_MAINNET)
    assert dc


def test_search_offers(dexie_test_client):
    offers = dexie_test_client.search_offers(page_size=7)
    assert offers
    assert len(offers) == 7


def test_get_offer(dexie_test_client):
    # from api docs
    dexie_offer_id = "HR7aHbCXsJto7iS9uBkiiGJx6iGySxoNqUGQvrZfnj6B"
    offer = dexie_test_client.get_offer(dexie_offer_id)
    assert offer
    assert offer.status == 4


def test_get_pairs(dexie_test_client):
    pairs = dexie_test_client.get_pairs()
    assert pairs
    assert len(pairs) > 0


def test_get_tickers(dexie_test_client):
    ticker = dexie_test_client.get_tickers("XCH_DBX")[0]
    assert ticker
    assert ticker.last_price
    assert ticker.pool_id


def test_get_orderbook(dexie_test_client):
    req_depth = 6
    ob = dexie_test_client.get_orderbook("XCH_DBX", depth=req_depth)
    assert ob
    assert len(ob.bids) == req_depth / 2


def test_get_historical_trades(dexie_test_client):
    h_trades = dexie_test_client.get_historical_trades("XCH_DBX", limit=3)
    assert h_trades
    assert len(h_trades.trades) == 3
