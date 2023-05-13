from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.config import Limits
from src.core.enums import TableNames
from src.core.mixins import PhoneNumberModel
from src.db.postgres import Base


class NameGeo:
    """Template for geo data.

    #### Attrs:
    - name (str):
        Geo location name.
    """

    name: Mapped[str] = mapped_column(String(Limits.DEFAULT_LEN_GEO_NAME))


class CountryModel(Base, NameGeo):
    """Table for country data.

    #### Attrs:
    - id (int):
        Identifier.
    - name (str):
        Country name.
    """

    __tablename__ = TableNames.COUNTRY
    name: Mapped[str] = mapped_column(
        String(Limits.DEFAULT_LEN_GEO_NAME),
        unique=True,
        index=True,
    )


class RegionModel(Base, NameGeo):
    """Table for region data (states, kingdoms, lands etc).

    #### Attrs:
    - id (int):
        Identifier.
    - name (str):
        Region name.
    - country_id (int):
        Relation to `CountryModel`.
    """

    __tablename__ = TableNames.REGION
    __tableargs__ = UniqueConstraint(
        "country_id",
        "id",
        name="unique region for a country",
    )

    country_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(TableNames.COUNTRY + ".id"),
        default=None,
    )


class DistrictModel(Base, NameGeo):
    """Table for district data.

    #### Attrs:
    - id (int):
        Identifier.
    - name (str):
        District name.
    - region_id (int | None): Default None.
        Relation to `RegionModel`.
    """

    __tablename__ = TableNames.DISTRICT
    __tableargs__ = UniqueConstraint(
        "region_id",
        "id",
        name="unique district for a region_country",
    )

    region_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(TableNames.REGION + ".id"),
        default=None,
    )


class CityModel(Base, NameGeo):
    """Table for city data (and towns, villages etc).
    There are may be countries without regions.

    #### Attrs:
    - id (int):
        Identifier.
    - name (str):
        City name.
    - country_id (int):
        Relation to `CountryModel`.
    - region_id (int | None): Default None.
        Relation to `RegionModel`.
    - district_id (int | None): Default None.
        Relation to `DistrictModel`.
    """

    __tablename__ = TableNames.CITY
    __tableargs__ = UniqueConstraint(
        "country_id",
        "region_id",
        "id",
        name="unique city for a region_country",
    )

    country_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey(TableNames.COUNTRY + ".id"), default=None
    )
    region_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(TableNames.REGION + ".id"),
        default=None,
    )
    district_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(TableNames.REGION + ".id"),
        default=None,
    )


class StreetModel(Base, NameGeo):
    """Table for street data (avenues, roads, squares etc).

    #### Attrs:
    - id (int):
        Identifier.
    - name (str):
        Street name.
    - city_id (int):
        Relation to `CityModel`.
    """

    __tablename__ = TableNames.STREET
    __tableargs__ = UniqueConstraint(
        "city_id",
        "id",
        name="unique street for city",
    )
    city_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(TableNames.CITY + ".id"),
        default=None,
    )


class AddressModel(Base):
    """Table for full addres data.
    There may be addresess without street.

    #### Attrs:
    - id (int):
        Identifier.
    - city_id (int):
        Relation to `CityModel`.
    - street_id (int | None): Default None.
        Relation to `StreetModel`.
    - building (str | None): Default None.
        Building number.
    - adds (str | None): Default None.
        Additional info such as letter, building, entrance etc.
    - office (str| None): Default None.
        Office (room, appartment) number.
    """

    __tablename__ = TableNames.ADDRESS

    city_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey(TableNames.CITY + ".id"), default=None
    )
    street_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(TableNames.STREET + ".id"),
        default=None,
    )
    building: Mapped[str | None] = mapped_column(
        String(Limits.LEN_16_GEO_NAME),
        default=None,
    )
    adds: Mapped[str | None] = mapped_column(
        String(Limits.LEN_16_GEO_NAME),
        default=None,
    )
    office: Mapped[str | None] = mapped_column(
        String(Limits.LEN_16_GEO_NAME),
        default=None,
    )


class PhoneModel(Base, PhoneNumberModel):
    """Table for phone numbers of addresses.

    #### Attrs:
    - phone_number (int):
        Big integer (int64) field.
    - address_id (int):
        Relation to `AddressModel`.
    """

    __tablename__ = TableNames.PHONE

    address_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(TableNames.ADDRESS + ".id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
