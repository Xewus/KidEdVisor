import re

from aiohttp import ClientSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import settings
from src.core.enums import Countries
from src.core.exceptions import BadRequestException
from src.db.postgres.database import ASessionMaker

from .models import (
    AddressModel,
    CityModel,
    CountryModel,
    DistrictModel,
    RegionModel,
    StreetModel,
)
from .shemes import AddressScheme

STREET_REGEX = (
    r"\b(?:улица|переулок|проспект|бульвар|тракт|шоссе|набережная|линия|аллея"
    r"|тупик|микрорайон|квартал|дорога|переулок|микрорайон)\b"
)
DISTRICT_REGEX = r"\b(?:район)"


class FullAddress:
    """Class for passing the full address.

    #### Attrs:
    - country (CountryModel | None)
    - region (RegionModel | None)
    - district (DistrictModel | None)
    - city (CityModel | None)
    - street (StreetModel | None)
    - address (AddressModel | None)
    """

    def __init__(
        self,
        country: CountryModel | None,
        region: RegionModel | None,
        district: DistrictModel | None,
        city: CityModel | None,
        street: StreetModel | None,
        address: AddressModel | None,
    ):
        self.country = country
        self.region = region
        self.district = district
        self.city = city
        self.street = street
        self.address = address


class YaMapAPI:
    """Connection to the `Yandex.Maps` API."""

    pre_url = (
        f"https://search-maps.yandex.ru/v1/?apikey={settings.ya_map_api_key}"
        "&type=geo&lang=ru_RU&results=1&text="
    )

    @classmethod
    async def __get_data(cls, address: AddressScheme) -> tuple[str, dict]:
        """Get data from the Yandex.Maps API.

        #### Args:
        - address (AddressScheme):
            Data to search.

        #### Returns:
        - tuple[str, dict]:
            Get data from the Yandex.Maps API.

        #### Args:
        - address (AddressScheme):
            [Data to search as string, result from API].
        """
        text = " ".join(
            str(i)
            for i in address.dict(
                exclude_none=True, exclude={"additional", "office", "phones"}
            ).values()
        )

        async with ClientSession() as session:
            async with session.get(url=cls.pre_url + text) as response:
                return text, await response.json()

    @classmethod
    async def get_valid_address(cls, address: AddressScheme) -> AddressScheme:
        """Get data from the Yandex.Maps API and parse it.

        #### Args:
        - address (AddressScheme):
            Data to search.

        #### Raises:
        - BadRequestException:
            Can't find address.

        #### Returns:
        - AddressScheme:
            Valid data from Yandex.Maps API.
        """
        str_address, data = await cls.__get_data(address)
        try:
            raw_address = data["features"][0]["properties"][
                "GeocoderMetaData"
            ]["text"].split(", ")[1:]

            valid_address = AddressScheme.from_orm(address)

            valid_address.region = raw_address[0]

            step = 1
            if re.search(DISTRICT_REGEX, raw_address[step], re.IGNORECASE):
                valid_address.district = raw_address[step]
                step += 1
            else:
                valid_address.district = None

            if re.search(STREET_REGEX, raw_address[step], re.IGNORECASE):
                valid_address.city = valid_address.region
            else:
                valid_address.city = raw_address[step]
                step += 1

            if re.search(STREET_REGEX, raw_address[step]):
                valid_address.street = raw_address[step]
                step += 1

            if raw_address[step].isdigit():
                valid_address.building = raw_address[step]

        except (IndexError, KeyError):
            raise BadRequestException(f"can't find address: {str_address}")

        return valid_address


async def get_valid_address(address: AddressScheme) -> AddressScheme:
    """Get valid address from another API.

    #### Args:
    - address (AddressScheme):
        Data to search.

    #### Raises:
    - BadRequestException:
        Mot supported country.

    #### Returns:
    - AddressScheme:
            Valid data from another API.
    """

    match address.country:
        case Countries.RUSSIA:
            return await YaMapAPI.get_valid_address(address)
        case _:
            raise BadRequestException(f"no support for {address.country}")


async def countries_always_exists() -> None:
    """Set countries to the database if they don't exist."""
    async with ASessionMaker() as db:
        db: AsyncSession
        if await db.scalar(select(CountryModel.id).limit(1)):
            return None

        countries = (
            CountryModel(name=name)
            for name in Countries._value2member_map_.keys()
        )
        db.add_all(countries)
        await db.commit()
    return None
