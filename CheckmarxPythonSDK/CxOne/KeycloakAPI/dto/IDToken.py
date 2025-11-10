from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .AddressClaimSet import AddressClaimSet


@dataclass
class IDToken:
    jti: Optional[str] = None
    exp: Optional[int] = None
    nbf: Optional[int] = None
    iat: Optional[int] = None
    iss: Optional[str] = None
    sub: Optional[str] = None
    typ: Optional[str] = None
    azp: Optional[str] = None
    other_claims: Optional[Dict[str, Any]] = None
    nonce: Optional[str] = None
    auth_time: Optional[int] = None
    session_state: Optional[str] = None
    at_hash: Optional[str] = None
    c_hash: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    middle_name: Optional[str] = None
    nickname: Optional[str] = None
    preferred_username: Optional[str] = None
    profile: Optional[str] = None
    picture: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    gender: Optional[str] = None
    birthdate: Optional[str] = None
    zoneinfo: Optional[str] = None
    locale: Optional[str] = None
    phone_number: Optional[str] = None
    phone_number_verified: Optional[bool] = None
    address: Optional[AddressClaimSet] = None
    updated_at: Optional[int] = None
    claims_locales: Optional[str] = None
    acr: Optional[str] = None
    s_hash: Optional[str] = None
    auth_time: Optional[int] = None
    sid: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.jti is not None:
            value = self.jti
            result['jti'] = value
        if self.exp is not None:
            value = self.exp
            result['exp'] = value
        if self.nbf is not None:
            value = self.nbf
            result['nbf'] = value
        if self.iat is not None:
            value = self.iat
            result['iat'] = value
        if self.iss is not None:
            value = self.iss
            result['iss'] = value
        if self.sub is not None:
            value = self.sub
            result['sub'] = value
        if self.typ is not None:
            value = self.typ
            result['typ'] = value
        if self.azp is not None:
            value = self.azp
            result['azp'] = value
        if self.other_claims is not None:
            value = self.other_claims
            result['otherClaims'] = value
        if self.nonce is not None:
            value = self.nonce
            result['nonce'] = value
        if self.auth_time is not None:
            value = self.auth_time
            result['authTime'] = value
        if self.session_state is not None:
            value = self.session_state
            result['sessionState'] = value
        if self.at_hash is not None:
            value = self.at_hash
            result['atHash'] = value
        if self.c_hash is not None:
            value = self.c_hash
            result['cHash'] = value
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.given_name is not None:
            value = self.given_name
            result['givenName'] = value
        if self.family_name is not None:
            value = self.family_name
            result['familyName'] = value
        if self.middle_name is not None:
            value = self.middle_name
            result['middleName'] = value
        if self.nickname is not None:
            value = self.nickname
            result['nickname'] = value
        if self.preferred_username is not None:
            value = self.preferred_username
            result['preferredUsername'] = value
        if self.profile is not None:
            value = self.profile
            result['profile'] = value
        if self.picture is not None:
            value = self.picture
            result['picture'] = value
        if self.website is not None:
            value = self.website
            result['website'] = value
        if self.email is not None:
            value = self.email
            result['email'] = value
        if self.email_verified is not None:
            value = self.email_verified
            result['emailVerified'] = value
        if self.gender is not None:
            value = self.gender
            result['gender'] = value
        if self.birthdate is not None:
            value = self.birthdate
            result['birthdate'] = value
        if self.zoneinfo is not None:
            value = self.zoneinfo
            result['zoneinfo'] = value
        if self.locale is not None:
            value = self.locale
            result['locale'] = value
        if self.phone_number is not None:
            value = self.phone_number
            result['phoneNumber'] = value
        if self.phone_number_verified is not None:
            value = self.phone_number_verified
            result['phoneNumberVerified'] = value
        if self.address is not None:
            value = self.address.to_dict()
            result['address'] = value
        if self.updated_at is not None:
            value = self.updated_at
            result['updatedAt'] = value
        if self.claims_locales is not None:
            value = self.claims_locales
            result['claimsLocales'] = value
        if self.acr is not None:
            value = self.acr
            result['acr'] = value
        if self.s_hash is not None:
            value = self.s_hash
            result['sHash'] = value
        if self.auth_time is not None:
            value = self.auth_time
            result['authTime'] = value
        if self.sid is not None:
            value = self.sid
            result['sid'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'address' in snake_data and snake_data['address'] is not None:
            snake_data['address'] = AddressClaimSet.from_dict(snake_data['address'])
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
