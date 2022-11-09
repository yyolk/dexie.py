import hashlib
from enum import Enum

import base58
from uplink import Consumer, Query, get, returns


def offer_file_to_dexie_id(offerfile: bytes):
    return base58.b58encode(hashlib.sha256(offerfile).digest()).decode()


class DexieOfferStatus(Enum):
    ACTIVE = 0
    PENDING = 1
    CANCELLING = 2
    CANCELLED = 3
    COMPLETED = 4
    UNKNOWN = 5


class DexieSortQuery(Enum):
    PRICE = "price"
    PRICE_DESCENDING = "price_desc"
    DATE_COMPLETED = "date_completed"
    DATE_FOUND = "date_found"


class Dexie(Consumer):
    @returns.json()
    @get("v1/offers")
    def search_offers(
        self,
        status: Query = None,
        offered: Query = None,
        requested: Query = None,
        offered_or_requested: Query = None,
        sort: Query = None,
        compact: Query = None,
        include_multiple_requested: Query = None,
        page: Query = None,
        page_size: Query = None,
    ):
        pass

    @returns.json()
    @get("v1/offers/{_id}")
    def get_offer(self, _id):
        """Inspect an offer

        Args:
            _id: Base58 encoded SHA256 Hash of the offer file
        """
        pass

    def get_offer_status(self, _id):
        offer = self.get_offer(_id).get("offer")
        if offer:
            return DexieOfferStatus(offer["status"])

    @returns.json
    @get("v1/prices/pairs")
    def get_pairs(self):
        """Get all traded XCH-CAT Pairs"""
        pass

    @returns.json
    @get("v1/prices/tickers")
    def get_tickers(self, ticker_id: Query = None):
        """Tickers (Market and Price Data)

        Args:
            ticker_id: (not required) any ``ticker_id`` from /pairs
        """
        pass

    @returns.json
    @get("v1/prices/orderbook")
    def get_orderbook(self, ticker_id: Query, depth: Query = None):
        """Order Book Depth Details

        Args:
            ticker_id: any ``ticker_id`` from /pairs
            depth: (not required) Orders depth quantity, 0 or empty returns full depth Depth 100 means 50 for each bid/ask side
        """
        pass

    @returns.json
    @get("v1/prices/historical_trades")
    def get_historical_trades(
        self,
        ticker_id: Query,
        _type: Query(name="type") = None,
        limit: Query = None,
        start_time: Query = None,
        end_time: Query = None,
    ):
        """Historical Trades

        Args:
            ticker_id: any ticker_id from /pairs, eg ``XCH_DBX``
            _type: "buy" or "sell"
            limit: (int) Number of historical trades to retrieve from time of query. Default is 1000, set to 0 for all.
            start_time: (timestamp in milliseconds) Start time from which to query historical trades from
            end_time: (timestamp in milliseconds) End time for historical trades query
        """
        pass
