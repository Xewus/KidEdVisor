from pydantic import BaseModel, Field, validator
from src.config import Limits
from src.core.enums import Countries
from src.core.exceptions import BadRequestException


def GeoNameField(**kw) -> Field:
    """Field with name length limit set.

    #### Returns:
    - Field:
        Field with name length limit set.
    """
    return Field(max_lenth=Limits.DEFAULT_LEN_GEO_NAME, **kw)


class AddressScheme(BaseModel):
    """Scheme for addresses.

    Among other things, you must provide one of the `building` or `adds`.

    #### Attrs:
    - country (Countries): Default `RUSSIA`.
        Country name.
    - region (str | None): Default `None`.
        Region name.
    - district (str | None): Default `None`.
        District name.
    - city (str):
        City name.
    - street (str | None): Default `None`'
        Street name.
    - building (PositiveInt | None): Default `None`'
        Building number.
    - adds (str | None): Default `None`'
        Additional info such as letter, building, entrance etc.
    - office (PositiveInt | None): Default `None`'
        Office (room, appartment) number.
    - phones (list[int] | None): Default `None`'
        Phone numbers.
    """

    country: Countries = Field(
        default=Countries.RUSSIA,
        title="Country name",
        example=Countries.RUSSIA,
    )
    region: str | None = GeoNameField(
        default=None,
        title="Region name",
        example="Камчатский край",
    )
    district: str | None = Field(
        default=None,
        title="District name",
        example="РАЙОН",
    )
    city: str = GeoNameField(
        title="City name",
        example="Broadwood",
    )
    street: str | None = GeoNameField(
        default=None,
        title="Street name",
        example="Broadwood Road",
    )
    building: str | None = Field(
        default=None,
        title="Building number",
        example="1041 A",
    )
    adds: str | None = Field(
        default=None,
        title="Additional info such as letter, entrance etc.",
        max_length=Limits.LEN_16_GEO_NAME,
        example="Near the lake",
    )
    office: str | None = Field(
        default=None,
        title="Office (room, appartment) number",
        example=6,
    )
    phones: list[int] | None = Field(
        default=None,
        title="Phone numbers",
        description="No more than three numbers allowed",
        example=[6494095878],
        max_items=3,
    )

    class Config:
        orm_mode = True

    @validator("phones")
    def phone_validator(cls, phones: list[int] | None) -> list[int] | None:
        if not phones:
            return None

        for phone in phones:
            if not Limits.MIN_PHONE_NUMBER < phone < Limits.MAX_PHONE_NUMBER:
                raise BadRequestException("bad phone number")
        return phones

    @validator("adds")
    def biuldung_or_adds_validator(
        cls, adds: str | None, values: dict
    ) -> str | None:
        if not adds and not values.get("building"):
            raise BadRequestException(
                "if you do not have a building number, "
                "you must provide other clarifying information"
            )
        return adds
