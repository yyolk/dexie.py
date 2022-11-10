"""
dexie.py
"""

import hashlib
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Any, Literal, Optional, Union

import base58
from uplink import (
    Consumer,
    Field,
    Query,
    converters,
    get,
    install,
    json as sends_json,
    post,
    returns,
)


class DexieOfferStatus(Enum):
    """Enum for holding Dexie's vocab for offers"""

    ACTIVE = 0
    PENDING = 1
    CANCELLING = 2
    CANCELLED = 3
    COMPLETED = 4
    UNKNOWN = 5


class DexieSortQuery(Enum):
    """Enum for holding Dexie's vocab for sorting from prices"""

    PRICE = "price"
    PRICE_DESCENDING = "price_desc"
    DATE_COMPLETED = "date_completed"
    DATE_FOUND = "date_found"


@dataclass(frozen=True)
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


@dataclass(frozen=True)
class DexiePair:
    ticker_id: str
    base: str
    target: str
    pool_id: str


@dataclass(frozen=True)
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


@dataclass(frozen=True)
class DexieOrderBook:
    ticker_id: str
    pool_id: str
    timestamp: str
    bids: list[Any]
    asks: list[Any]


@dataclass(frozen=True)
class DexieTrade:
    trade_id: str
    price: Decimal
    base_volume: Decimal
    target_volume: Decimal
    trade_timestamp: str
    type: Union[Literal["buy"], Literal["sell"]]


@dataclass(frozen=True)
class DexieHistoricalTrade:
    ticker_id: str
    pool_id: str
    timestamp: str
    trades: list[DexieTrade]


@returns.json
class Dexie(Consumer):
    """Uplink DSL Dexie.Space API Client"""

    @sends_json
    @post("v1/offers")
    def post_offer(self, offer: Field):
        """Post an offer to dexie

        Args:
            offer: (str) an offer string
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

        TODO:
            - allow multiples on args:status
        Args:
            status: (Optional[DexieOfferStatus]) Only include offers with this status.
            offered: (Optional[str]) Only include offers which offer this asset
            requested: (Optional[str]) Only include offers which request this asset
            offered_or_requested: (Optional[str]) Only include offers which request OR offer this asset
            sort: (Optional[DexieSortQuery]) Sort offers by this field
            compact: (Optional[bool]) Outputs a lighter version without full offer files. Use this if you only need trade or price data to save bandwidth and load (e.g recent trades).
            include_multiple_requested: (Optional[bool]) Include offers which request multiple assets (only applies if requested parameter is set)
            page: (Optional[int]) Request a specific page.
            page_size: (Optional[int]) How many offers to request. For more than 100 offers use ``page``.
        """

    @get("v1/offers/{id_}")
    def get_offer(self, id_) -> DexieOffer:
        """Inspect an offer

        Args:
            id_: (str) Base58 encoded SHA256 Hash of the offer file (Dexie's OfferFile Id)
        """

    @get("v1/prices/pairs")
    def get_pairs(self) -> list[DexiePair]:
        """Get all traded XCH-CAT Pairs"""

    @get("v1/prices/tickers")
    def get_tickers(self, ticker_id: Query = None) -> list[DexieTicker]:
        """Tickers (Market and Price Data)

        Args:
            ticker_id: (Optional[str]) any ``ticker_id`` from /pairs
        """

    @get("v1/prices/orderbook")
    def get_orderbook(self, ticker_id: Query, depth: Query = None) -> DexieOrderBook:
        """Order Book Depth Details

        Args:
            ticker_id: (str) any ``ticker_id`` from /pairs
            depth: (Optional[int]) Orders depth quantity, 0 or empty returns full depth Depth 100 means 50 for each bid/ask side
        """

    @get("v1/prices/historical_trades")
    def get_historical_trades(
        self,
        ticker_id: Query,
        type: Query = None,
        limit: Query = None,
        start_time: Query = None,
        end_time: Query = None,
    ) -> DexieHistoricalTrade:
        """Historical Trades

        Args:
            ticker_id: (str) any ticker_id from /pairs, eg ``XCH_DBX``
            type: (Optional[str]) "buy" or "sell"
            limit: (Optional[int]) Number of historical trades to retrieve from time of query. Default is 1000, set to 0 for all.
            start_time: (Optional[str]) timestamp in milliseconds. Start time from which to query historical trades from
            end_time: (Optional[str]) timestamp in milliseconds. End time for historical trades query
        """


class _DexieResponseBody(converters.Converter):
    def __init__(self, model, model_cls):
        self._model = model
        self._model_cls = model_cls

    def convert(self, value):
        if hasattr(value, "json") and callable(value.get("json")):
            data = value.json()
        else:
            # this is a safe fallback that should be forwards compatible to
            # pass-through any other dexie data IF theres a method to call it
            data = value

        if data.get("success"):
            if self._model is not None:
                # collections are plural
                if self._model.endswith("s"):
                    datas = data[self._model]
                    return [self._model_cls(**datum) for datum in datas]
                return self._model_cls(**data[self._model])

            # sometimes we do need to inject more data like HistoricalTrades
            # which doesn't just have a single key with all the data
            # remove the response success key, which we no longer need
            model_data = {k: data[k] for k in data if k != "success"}
            # we wrap our data with our model_cls
            return self._model_cls(**model_data)

        return data


@install
class DexieResponseFactory(converters.Factory):
    """Unpack a response to make the data immediately usable with our models"""

    def _get_model_new_type(self, type_):
        if type_ == DexieOffer:
            return "offer", DexieOffer
        if type_ == list[DexieOffer]:
            return "offers", DexieOffer
        if type_ == list[DexiePair]:
            return "pairs", DexiePair
        if type_ == list[DexieTicker]:
            return "tickers", DexieTicker
        if type_ == DexieOrderBook:
            return "orderbook", DexieOrderBook
        if type_ == DexieHistoricalTrade:
            return None, DexieHistoricalTrade
        # TODO this is kinda a lame way to leave some way to hook in if the
        #      model isn't known for logging but fall back safely without a
        #      performance hit
        raise ValueError(
            (
                "Model not defined. This is a silent error caught in"
                " our private method. You shouldn't see this!"
            )
        )

    def _make_converter(self, converter, type_):
        try:
            model, new_type = self._get_model_new_type(type_)
            return converter(model, new_type)
        except ValueError:
            # this happens if we don't know the model
            # for faster dev i think making the client fall back to vanilla
            # response is appropriate
            pass
        return None

    def create_response_body_converter(self, cls, request_definition):
        return self._make_converter(_DexieResponseBody, cls)


# Chia offer data utils
def offer_bytes_to_dexie_id(offer: bytes) -> str:
    """Take offer encoded as bytes and return a dexie offer id

    Args:
        offer: (bytes) The serialized offer file as bytes
    """
    return base58.b58encode(hashlib.sha256(offer).digest()).decode()


def offer_str_to_dexie_id(offer: str) -> str:
    """Take offer str and return a dexie offer id"""
    return offer_bytes_to_dexie_id(bytes(offer, encoding="utf-8"))


@dataclass(frozen=True)
class DexieChiaOfferData:
    dexie_id: str
    offer_bytes: bytes
    offer_str: str

    @classmethod
    def from_bytes(cls, offer: bytes) -> "DexieChiaOfferData":
        """From bytes constructor"""
        return cls(offer_bytes_to_dexie_id(offer), offer, str(offer))

    @classmethod
    def from_str(cls, offer: str) -> "DexieChiaOfferData":
        """From str constructor"""
        return cls(offer_str_to_dexie_id(offer), bytes(offer, encoding="utf-8"), offer)
