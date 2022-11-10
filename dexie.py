"""
dexie.py
"""

import hashlib
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Any, Optional, Callable, List

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
    types,
    utils,
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


@dataclass(frozen=True, unsafe_hash=True)
class DexieOffer:
    id: str
    status: DexieOfferStatus
    offer: str
    offered_coins: list[str]
    date_found: str
    date_completed: str
    date_pending: str
    spent_block_index: int
    price: Decimal
    offered: list[dict]
    requested: list[dict]
    fees: Decimal
    mempool: Optional[Any]
    related_offers: list[dict]
    coins: Optional[list[dict]] = None
    previous_price: Optional[Decimal] = None


# class DexieOffers(DexieOffer):
#     pass


@dataclass(frozen=True, unsafe_hash=True)
class DexiePair:
    ticker_id: str
    base: str
    target: str
    pool_id: str


@dataclass(frozen=True, unsafe_hash=True)
class DexieTicker:
    ticker_id: str
    base_currency: str
    target_currency: str
    last_price: Decimal
    current_avg_price: Decimal
    base_volume: Decimal
    target_volume: Decimal
    pool_id: str
    bid: Decimal
    ask: Decimal
    high: Decimal
    low: Decimal


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
    def get_pairs(self) -> list[DexiePair]:
        """Get all traded XCH-CAT Pairs"""

    @get("v1/prices/tickers")
    def get_tickers(self, ticker_id: Query = None) -> list[DexieTicker]:
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


def get_offer_status(offer: DexieOffer):
    """Just grab the status.

    Useful for batch processing status of many offers.

    Args:
        offer_status: (DexieOffer) the response from a ``Dexie.get_offer`` request
    """
    return offer.status


# @install
# @loads.from_json(DexieOffer)
# def offer_json_reader(offer_cls, json_):
#     """Default serialize method for loading an DexieOffer"""
#     if json_.get("success"):
#         # I don't know if uplink has a better way to handle this
#         # leveraging how it uses type annotations
#         if offers := json_.get("offers"):
#             return [offer_cls(**offer) for offer in offers]
#         if offer := json_.get("offer"):
#             return offer_cls(**offer)
#     return None


class _DexieResponseBody(converters.Converter):
    def __init__(self, model):
        self._model = model

    def convert(self, response):
        try:
            data = response.json()

        except AttributeError:
            data = response

        print("data is", data)
        print("model is", self._model)
        if data.get("success"):
            return data[self._model]

        return None


@install
class DexieResponseFactory(converters.Factory):
    def _get_model(self, type_):
        if type_ == DexieOffer:
            return "offer"
        if type_ == list[DexieOffer]:
            return "offers"
        if type_ == list[DexiePair]:
            return "pairs"
        if type_ == list[DexieTicker]:
            return "tickers"
        raise ValueError("Model not defined short circuit")

    def _make_converter(self, converter, type_):
        try:
            model = self._get_model(type_)
        except ValueError:
            # print("hit here")
            return None
        return converter(model)

    # def create_response_body_converter(self, cls, *args, **kwargs):
    def create_response_body_converter(self, cls, request_definition):
        print("cls", cls, "request_definition", request_definition)
        print(type(cls), type(request_definition))

        return self._make_converter(_DexieResponseBody, cls)

    #     def handler(response):
    #         if response.get("success"):
    #             return
    # return lambda response:
