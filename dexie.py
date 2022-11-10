"""
dexie.py
"""
import decimal
import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Callable

import base58
from uplink import (
    Consumer,
    Field,
    Query,
    converters,
    get,
    install,
    loads,
    json as sends_json,
    post,
    returns,
)

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

@dataclass
class DexieOffer():
    id: str
    status: DexieOfferStatus
    offer: str
    offered_coins: list[str]
    date_found: str
    date_completed: str
    date_pending: str
    spent_block_index: int
    price: decimal.Decimal
    offered: list[dict]
    requested: list[dict]
    fees: decimal.Decimal
    mempool: Optional[Any]
    related_offers: list[dict]
    coins: Optional[list[dict]] = None
    previous_price: Optional[decimal.Decimal] = None



@returns.json
class Dexie(Consumer):
    @sends_json
    @post("v1/offers")
    def post_offer(self, offer: Field):
        """Post an offer to dexie

        Args:
            offer: (uplink.Field) UTF-8 encoded offerfile
        """

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
    ) -> list[DexieOffer]:
        """Search Offers

        All arguments are optional. Call without args to get latest offers.

        Args:
            status: (uplink.Query | [DexieOfferStatus]) Only include offers with this status. TODO: Multiples allowed.
            offered: (uplink.Query) Only include offers which offer this asset
            requested: (uplink.Query) Only include offers which request this asset
            offered_or_requested: (uplink.Query) Only include offers which request OR offer this asset
            sort: (uplink.Query) Sort offers by this field
            compact: (uplink.Query) Outputs a lighter version without full offer files. Use this if you only need trade or price data to save bandwidth and load (e.g recent trades).
            include_multiple_requested: (uplink.Query) Include offers which request multiple assets (only applies if requested parameter is set)
            page: (uplink.Query) Request a specific page.
            page_size: (uplink.Query) How many offers to request. For more than 100 offers use ``page``.
        """




    @get("v1/offers/{id_}")
    def get_offer(self, id_) -> DexieOffer:
        """Inspect an offer

        Args:
            id_: Base58 encoded SHA256 Hash of the offer file (Dexie's OfferFile Id)
        """

    @get("v1/prices/pairs")
    def get_pairs(self):
        """Get all traded XCH-CAT Pairs"""

    @get("v1/prices/tickers")
    def get_tickers(self, ticker_id: Query = None):
        """Tickers (Market and Price Data)

        Args:
            ticker_id: (not required) any ``ticker_id`` from /pairs
        """

    @get("v1/prices/orderbook")
    def get_orderbook(self, ticker_id: Query, depth: Query = None):
        """Order Book Depth Details

        Args:
            ticker_id: any ``ticker_id`` from /pairs
            depth: (not required) Orders depth quantity, 0 or empty returns full depth Depth 100 means 50 for each bid/ask side
        """

    @get("v1/prices/historical_trades")
    def get_historical_trades(
        self,
        ticker_id: Query,
        type_: Query(name="type") = None,
        limit: Query = None,
        start_time: Query = None,
        end_time: Query = None,
    ):
        """Historical Trades

        Args:
            ticker_id: any ticker_id from /pairs, eg ``XCH_DBX``
            type_: "buy" or "sell"
            limit: (int) Number of historical trades to retrieve from time of query. Default is 1000, set to 0 for all.
            start_time: (timestamp in milliseconds) Start time from which to query historical trades from
            end_time: (timestamp in milliseconds) End time for historical trades query
        """


# Utility Functions


def offer_file_to_dexie_id(offerfile: bytes):
    """Take offerfile encoded as bytes and return a dexie offerfile id

    Args:
        offerfile: (bytes) The serialized offer file as bytes
    """
    return base58.b58encode(hashlib.sha256(offerfile).digest()).decode()


def get_offer_status(offer_status):
    """Just grab the status.

    Useful for batch processing status of many offers.

    Args:
        offer_status: (Dict) the response from a ``Dexie.get_offer`` request
    """
    offer = offer_status.get("offer")
    if offer:
        return DexieOfferStatus(offer["status"])
    return None


@install
@loads.from_json(DexieOffer)
def offer_json_reader(offer_cls, json_):
    """Default serialize method for loading an DexieOffer"""
    if json_.get("success"):
        if offers := json_.get("offers"):
            return [offer_cls(**offer) for offer in offers]
        if offer := json_.get("offer"):
            return offer_cls(**offer)
    return None


# @install
# class DexieResponseFactory(converters.Factory):
#     def create_response_body_converter(self, cls, request_definition)
#         def handler(response):
#             if response.get("success"):
#                 return 
#     return lambda response: 
