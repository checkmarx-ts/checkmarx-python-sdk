from dataclasses import dataclass


@dataclass
class AccessToken:
    acr: ... = None
    address: ... = None
    allowed_origins: ... = None
    at_hash: ... = None
    auth_time: ... = None
    authorization: ... = None
    azp: ... = None
    birthdate: ... = None
    c_hash: ... = None
    category: ... = None
    claims_locales: ... = None
    cnf: ... = None
    email: ... = None
    email_verified: ... = None
    exp: ... = None
    family_name: ... = None
    gender: ... = None
    given_name: ... = None
    iat: ... = None
    iss: ... = None
    jti: ... = None
    locale: ... = None
    middle_name: ... = None
    name: ... = None
    nbf: ... = None
    nickname: ... = None
    nonce: ... = None
    other_claims: ... = None
    phone_number: ... = None
    phone_number_verified: ... = None
    picture: ... = None
    preferred_username: ... = None
    profile: ... = None
    realm_access: ... = None
    s_hash: ... = None
    scope: ... = None
    session_state: ... = None
    sid: ... = None
    sub: ... = None
    trusted_certs: ... = None
    typ: ... = None
    updated_at: ... = None
    website: ... = None
    zoneinfo: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "AccessToken":
        return cls(
            acr=item.get("acr"),
            address=item.get("address"),
            allowed_origins=item.get("allowed_origins"),
            at_hash=item.get("at_hash"),
            auth_time=item.get("auth_time"),
            authorization=item.get("authorization"),
            azp=item.get("azp"),
            birthdate=item.get("birthdate"),
            c_hash=item.get("c_hash"),
            category=item.get("category"),
            claims_locales=item.get("claims_locales"),
            cnf=item.get("cnf"),
            email=item.get("email"),
            email_verified=item.get("email_verified"),
            exp=item.get("exp"),
            family_name=item.get("family_name"),
            gender=item.get("gender"),
            given_name=item.get("given_name"),
            iat=item.get("iat"),
            iss=item.get("iss"),
            jti=item.get("jti"),
            locale=item.get("locale"),
            middle_name=item.get("middle_name"),
            name=item.get("name"),
            nbf=item.get("nbf"),
            nickname=item.get("nickname"),
            nonce=item.get("nonce"),
            other_claims=item.get("otherClaims"),
            phone_number=item.get("phone_number"),
            phone_number_verified=item.get("phone_number_verified"),
            picture=item.get("picture"),
            preferred_username=item.get("preferred_username"),
            profile=item.get("profile"),
            realm_access=item.get("realm_access"),
            s_hash=item.get("s_hash"),
            scope=item.get("scope"),
            session_state=item.get("session_state"),
            sid=item.get("sid"),
            sub=item.get("sub"),
            trusted_certs=item.get("trusted_certs"),
            typ=item.get("typ"),
            updated_at=item.get("updated_at"),
            website=item.get("website"),
            zoneinfo=item.get("zoneinfo"),
        )
