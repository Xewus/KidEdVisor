from enum import IntEnum, StrEnum

from src.config import settings


class TableNames(StrEnum):
    """
    #### Attrs:
    - AUTH (str): "auth"
    - PARENT (str): "parent"
    - OWNER (str): "owner"
    - OWNER_ADDRESS (str): "owner_address"
    - INSTITUTION (str): "nstitution"
    - TEACHER (str): "teacher"
    - CATEGORY (str): "category"
    - COUNTRY (str): "country"
    - REGION (str): "region"
    - DISTRICT (str): "district"
    - CITY (str): "city"
    - STREET (str): "street"
    - ADDRESS (str): "address"
    - PHONE (int): "phone"
    """

    AUTH = "auth"

    PARENT = "parent"

    OWNER = "owner"
    INSTITUTION = "institution"
    TEACHER = "teacher"
    OWNER_ADDRESS = "owner_address"
    CATEGORY = "category"

    COUNTRY = "country"
    REGION = "region"
    DISTRICT = "district"
    CITY = "city"
    STREET = "street"
    ADDRESS = "address"
    PHONE = "phone"


class UserType(IntEnum):
    """
    #### Attrs:
    - PARENT (int): 1
    - OWNER (int): 2
    - ADMIN (int): 42
    """

    PARENT = 1
    OWNER = 2
    ADMIN = 42


class InstitutionType(IntEnum):
    """
    #### Attrs:
    - KINDERGARTEN (int): 100
    - SCHOOL (int): 200
    - HIGH_SCHOOL (int): 201
    - PRIVATE_SCHOOL (int): 202
    - COLLEGE (int): 300
    - INSTITUTE (int): 400
    - UNIVERSITY (int): 401
    - ADDITIONAL (int): 500
    - SPORT (int): 600
    - CREATION (int): 700
    - SCIENCE (INT): 800
    """

    KINDERGARTEN = 100
    SCHOOL = 200
    HIGH_SCHOOL = 201
    PRIVATE_SCHOOL = 202
    COLLEGE = 300
    INSTITUTE = 400
    UNIVERSITY = 401
    ADDITIONAL = 500
    SPORT = 600
    CREATION = 700
    SCIENCE = 800


class AppPaths(StrEnum):
    """
    #### Attrs:
    - API (str): "/api"
    - V1 (str): "/v1"
    - TOKEN (str): "/token"
    - ADMINS (str): "/admins"
    - AUTH (str): "/auth"
    - PROVIDERS (str): "/providers"
    - PARENTS (str): "/parents"
    """

    API = "/api"
    V1 = "/v1"
    TOKEN = "/token"
    ADMINS = "/admins"
    AUTH = "/auth"
    PROVIDERS = "/providers"
    PARENTS = "/parents"


class RouteTags(StrEnum):
    """Tags for routes.

    #### Attrs:
    - ADMINS (str): "ADMINS"
    - AUTH (str): "AUTH"
    - PROVIDERS (str): "PROVIDERS"
    - PARENTS (str): "PARENTS"
    """

    ADMINS = "ADMINS"
    AUTH = "AUTH"
    PROVIDERS = "PROVIDERS"
    PARENTS = "PARENTS"


class SendEmailFrom(StrEnum):
    """
    #### Attrs:
    - GOOGLE (str): from settings
    """

    GOOGLE = settings.google_email


class Countries(StrEnum):
    AFGHANISTAN = "Afghanistan"
    ALBANIA = "Albania"
    ALGERIA = "Algeria"
    ANDORRA = "Andorra"
    ANGOLA = "Angola"
    ANTIGUA_AND_BARBUDA = "Antigua and Barbuda"
    ARGENTINA = "Argentina"
    ARMENIA = "Armenia"
    AUSTRALIA = "Australia"
    AUSTRIA = "Austria"
    AZERBAIJAN = "Azerbaijan"
    BAHAMAS = "Bahamas"
    BAHRAIN = "Bahrain"
    BANGLADESH = "Bangladesh"
    BARBADOS = "Barbados"
    BELARUS = "Belarus"
    BELGIUM = "Belgium"
    BELIZE = "Belize"
    BENIN = "Benin"
    BHUTAN = "Bhutan"
    BOLIVIA = "Bolivia"
    BOSNIA_AND_HERZEGOVINA = "Bosnia and Herzegovina"
    BOTSWANA = "Botswana"
    BRAZIL = "Brazil"
    BRUNEI = "Brunei"
    BULGARIA = "Bulgaria"
    BURKINA_FASO = "Burkina Faso"
    BURUNDI = "Burundi"
    CABO_VERDE = "Cabo Verde"
    CAMBODIA = "Cambodia"
    CAMEROON = "Cameroon"
    CANADA = "Canada"
    CENTRAL_AFRICAN_REPUBLIC = "Central African Republic"
    CHAD = "Chad"
    CHILE = "Chile"
    CHINA = "China"
    COLOMBIA = "Colombia"
    COMOROS = "Comoros"
    DEMOCRATIC_REPUBLIC_OF_THE_CONGO = "Democratic Republic of the Congo"
    REPUBLIC_OF_THE_CONGO = "Republic of the Congo"
    COSTA_RICA = "Costa Rica"
    COTE_DIVOIRE = "Cote d'Ivoire"
    CROATIA = "Croatia"
    CUBA = "Cuba"
    CYPRUS = "Cyprus"
    CZECH_REPUBLIC = "Czech Republic"
    DENMARK = "Denmark"
    DJIBOUTI = "Djibouti"
    DOMINICA = "Dominica"
    DOMINICAN_REPUBLIC = "Dominican Republic"
    ECUADOR = "Ecuador"
    EGYPT = "Egypt"
    EL_SALVADOR = "El Salvador"
    EQUATORIAL_GUINEA = "Equatorial Guinea"
    ERITREA = "Eritrea"
    ESTONIA = "Estonia"
    ESWATINI = "Eswatini"
    ETHIOPIA = "Ethiopia"
    FIJI = "Fiji"
    FINLAND = "Finland"
    FRANCE = "France"
    GABON = "Gabon"
    GAMBIA = "Gambia"
    GEORGIA = "Georgia"
    GERMANY = "Germany"
    GHANA = "Ghana"
    GREECE = "Greece"
    GRENADA = "Grenada"
    GUATEMALA = "Guatemala"
    GUINEA = "Guinea"
    GUINEA_BISSAU = "Guinea-Bissau"
    GUYANA = "Guyana"
    HAITI = "Haiti"
    HONDURAS = "Honduras"
    HUNGARY = "Hungary"
    ICELAND = "Iceland"
    INDIA = "India"
    INDONESIA = "Indonesia"
    IRAN = "Iran"
    IRAQ = "Iraq"
    IRELAND = "Ireland"
    ISRAEL = "Israel"
    ITALY = "Italy"
    JAMAICA = "Jamaica"
    JAPAN = "Japan"
    JORDAN = "Jordan"
    KAZAKHSTAN = "Kazakhstan"
    KENYA = "Kenya"
    KIRIBATI = "Kiribati"
    KOSOVO = "Kosovo"
    KUWAIT = "Kuwait"
    KYRGYZSTAN = "Kyrgyzstan"
    LAOS = "Laos"
    LATVIA = "Latvia"
    LEBANON = "Lebanon"
    LESOTHO = "Lesotho"
    LIBERIA = "Liberia"
    LIBYA = "Libya"
    LIECHTENSTEIN = "Liechtenstein"
    LITHUANIA = "Lithuania"
    LUXEMBOURG = "Luxembourg"
    MADAGASCAR = "Madagascar"
    MALAWI = "Malawi"
    MALAYSIA = "Malaysia"
    MALDIVES = "Maldives"
    MALI = "Mali"
    MALTA = "Malta"
    MARSHALL_ISLANDS = "Marshall Islands"
    MAURITANIA = "Mauritania"
    MAURITIUS = "Mauritius"
    MEXICO = "Mexico"
    MICRONESIA = "Micronesia"
    MOLDOVA = "Moldova"
    MONACO = "Monaco"
    MONGOLIA = "Mongolia"
    MONTENEGRO = "Montenegro"
    MOROCCO = "Morocco"
    MOZAMBIQUE = "Mozambique"
    MYANMAR = "Myanmar (Burma)"
    NAMIBIA = "Namibia"
    NAURU = "Nauru"
    NEPAL = "Nepal"
    NETHERLANDS = "Netherlands"
    NEW_ZEALAND = "New Zealand"
    NICARAGUA = "Nicaragua"
    NIGER = "Niger"
    NIGERIA = "Nigeria"
    NORTH_KOREA = "North Korea"
    NORTH_MACEDONIA = "North Macedonia"
    NORWAY = "Norway"
    OMAN = "Oman"
    PAKISTAN = "Pakistan"
    PALAU = "Palau"
    PALESTINE = "Palestine"
    PANAMA = "Panama"
    PAPUA_NEW_GUINEA = "Papua New Guinea"
    PARAGUAY = "Paraguay"
    PERU = "Peru"
    PHILIPPINES = "Philippines"
    POLAND = "Poland"
    PORTUGAL = "Portugal"
    QATAR = "Qatar"
    ROMANIA = "Romania"
    RUSSIA = "Russia"
    RWANDA = "Rwanda"
    SAINT_KITTS_AND_NEVIS = "Saint Kitts and Nevis"
    SAINT_LUCIA = "Saint Lucia"
    SAINT_VINCENT_AND_THE_GRENADINES = "Saint Vincent and the Grenadines"
    SAMOA = "Samoa"
    SAN_MARINO = "San Marino"
    SAO_TOME_AND_PRINCIPE = "Sao Tome and Principe"
    SAUDI_ARABIA = "Saudi Arabia"
    SENEGAL = "Senegal"
    SERBIA = "Serbia"
    SEYCHELLES = "Seychelles"
    SIERRA_LEONE = "Sierra Leone"
    SINGAPORE = "Singapore"
    SLOVAKIA = "Slovakia"
    SLOVENIA = "Slovenia"
    SOLOMON_ISLANDS = "Solomon Islands"
    SOMALIA = "Somalia"
    SOUTH_AFRICA = "South Africa"
    SOUTH_KOREA = "South Korea"
    SOUTH_SUDAN = "South Sudan"
    SPAIN = "Spain"
    SRI_LANKA = "Sri Lanka"
    SUDAN = "Sudan"
    SURINAME = "Suriname"
    SWAZILAND = "Swaziland"
    SWEDEN = "Sweden"
    SWITZERLAND = "Switzerland"
    SYRIA = "Syria"
    TAIWAN = "Taiwan"
    TAJIKISTAN = "Tajikistan"
    TANZANIA = "Tanzania"
    THAILAND = "Thailand"
    TIMOR_LESTE = "Timor-Leste"
    TOGO = "Togo"
    TONGA = "Tonga"
    TRINIDAD_AND_TOBAGO = "Trinidad and Tobago"
    TUNISIA = "Tunisia"
    TURKEY = "Turkey"
    TURKMENISTAN = "Turkmenistan"
    TUVALU = "Tuvalu"
    UGANDA = "Uganda"
    UKRAINE = "Ukraine"
    UNITED_ARAB_EMIRATES = "United Arab Emirates"
    UNITED_KINGDOM = "United Kingdom"
    UNITED_STATES_OF_AMERICA = "United States of America"
    URUGUAY = "Uruguay"
    UZBEKISTAN = "Uzbekistan"
    VANUATU = "Vanuatu"
    VATICAN_CITY = "Vatican City"
    VENEZUELA = "Venezuela"
    VIETNAM = "Vietnam"
    YEMEN = "Yemen"
    ZAMBIA = "Zambia"
    ZIMBABWE = "Zimbabwe"
