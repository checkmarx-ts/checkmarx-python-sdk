class AccessToken:
    def __init__(self, acr, address, allowed_origins, at_hash, auth_time, authorization, azp, birthdate, c_hash,
                 category, claims_locales, cnf, email, email_verified, exp, family_name, gender, given_name, iat, iss,
                 jti, locale, middle_name, name, nbf, nickname, nonce, other_claims, phone_number,
                 phone_number_verified, picture, preferred_username, profile, realm_access, s_hash, scope,
                 session_state, sid, sub, trusted_certs, typ, updated_at, website, zoneinfo):
        self.acr = acr
        self.address = address
        self.allowed_origins = allowed_origins
        self.at_hash = at_hash
        self.auth_time = auth_time
        self.authorization = authorization
        self.azp = azp
        self.birthdate = birthdate
        self.c_hash = c_hash
        self.category = category
        self.claims_locales = claims_locales
        self.cnf = cnf
        self.email = email
        self.email_verified = email_verified
        self.exp = exp
        self.family_name = family_name
        self.gender = gender
        self.given_name = given_name
        self.iat = iat
        self.iss = iss
        self.jti = jti
        self.locale = locale
        self.middle_name = middle_name
        self.name = name
        self.nbf = nbf
        self.nickname = nickname
        self.nonce = nonce
        self.otherClaims = other_claims
        self.phone_number = phone_number
        self.phone_number_verified = phone_number_verified
        self.picture = picture
        self.preferred_username = preferred_username
        self.profile = profile
        self.realm_access = realm_access
        self.s_hash = s_hash
        self.scope = scope
        self.session_state = session_state
        self.sid = sid
        self.sub = sub
        self.trusted_certs = trusted_certs
        self.typ = typ
        self.updated_at = updated_at
        self.website = website
        self.zoneinfo = zoneinfo

    def __str__(self):
        return f"AccessToken(" \
               f"acr={self.acr} " \
               f"address={self.address} " \
               f"allowed_origins={self.allowed_origins} " \
               f"at_hash={self.at_hash} " \
               f"auth_time={self.auth_time} " \
               f"authorization={self.authorization} " \
               f"azp={self.azp} " \
               f"birthdate={self.birthdate} " \
               f"c_hash={self.c_hash} " \
               f"category={self.category} " \
               f"claims_locales={self.claims_locales} " \
               f"cnf={self.cnf} " \
               f"email={self.email} " \
               f"email_verified={self.email_verified} " \
               f"exp={self.exp} " \
               f"family_name={self.family_name} " \
               f"gender={self.gender} " \
               f"given_name={self.given_name} " \
               f"iat={self.iat} " \
               f"iss={self.iss} " \
               f"jti={self.jti} " \
               f"locale={self.locale} " \
               f"middle_name={self.middle_name} " \
               f"name={self.name} " \
               f"nbf={self.nbf} " \
               f"nickname={self.nickname} " \
               f"nonce={self.nonce} " \
               f"otherClaims={self.otherClaims} " \
               f"phone_number={self.phone_number} " \
               f"phone_number_verified={self.phone_number_verified} " \
               f"picture={self.picture} " \
               f"preferred_username={self.preferred_username} " \
               f"profile={self.profile} " \
               f"realm_access={self.realm_access} " \
               f"s_hash={self.s_hash} " \
               f"scope={self.scope} " \
               f"session_state={self.session_state} " \
               f"sid={self.sid} " \
               f"sub={self.sub} " \
               f"trusted_certs={self.trusted_certs} " \
               f"typ={self.typ} " \
               f"updated_at={self.updated_at} " \
               f"website={self.website} " \
               f"zoneinfo={self.zoneinfo} " \
               f")"

    def to_dict(self):
        return {
            "acr": self.acr,
            "address": self.address,
            "allowed_origins": self.allowed_origins,
            "at_hash": self.at_hash,
            "auth_time": self.auth_time,
            "authorization": self.authorization,
            "azp": self.azp,
            "birthdate": self.birthdate,
            "c_hash": self.c_hash,
            "category": self.category,
            "claims_locales": self.claims_locales,
            "cnf": self.cnf,
            "email": self.email,
            "email_verified": self.email_verified,
            "exp": self.exp,
            "family_name": self.family_name,
            "gender": self.gender,
            "given_name": self.given_name,
            "iat": self.iat,
            "iss": self.iss,
            "jti": self.jti,
            "locale": self.locale,
            "middle_name": self.middle_name,
            "name": self.name,
            "nbf": self.nbf,
            "nickname": self.nickname,
            "nonce": self.nonce,
            "otherClaims": self.otherClaims,
            "phone_number": self.phone_number,
            "phone_number_verified": self.phone_number_verified,
            "picture": self.picture,
            "preferred_username": self.preferred_username,
            "profile": self.profile,
            "realm_access": self.realm_access,
            "s_hash": self.s_hash,
            "scope": self.scope,
            "session_state": self.session_state,
            "sid": self.sid,
            "sub": self.sub,
            "trusted_certs": self.trusted_certs,
            "typ": self.typ,
            "updated_at": self.updated_at,
            "website": self.website,
            "zoneinfo": self.zoneinfo,
        }


def construct_access_token(item):
    return AccessToken(
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
