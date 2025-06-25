
# Interface beschrijving v0.91 – BOA bevraging register

**Datum**: 10-06-2025  
**Versie**: 0.91  
**Status**: Concept  

---

## Revisies



---

## Colofon

- 

---

## Inhoudsopgave

1. [Inleiding](#1-inleiding)  
2. [Globaal Ontwerp](#2-globaal-ontwerp)  
3. [Berichten](#3-berichten)  

---

## 1. Inleiding

### 1.1 Doel

Een heldere beschrijving van de interface 

### 1.2 Scope

Opvragen van pasfoto’s uit het register door BOA’s (domeinen I, II, IV) via REST API.

**Uitgangspunten:**

- Gebaseerd op Digikoppeling REST-API 2.0.2  
- Gebruik van Diginetwerk  
- OWASP richtlijnen  
- BOA werkgever is verantwoordelijk voor authenticatie en mobiele apparaten  
- KISS: Keep It Simple and Secure

### 1.3 Referenties

- [RFC7515 - JSON Web Signature](https://www.rfc-editor.org/rfc/rfc7515)
- [RFC7516 - JSON Web Encryption](https://www.rfc-editor.org/rfc/rfc7516.html)
- [JWT.io](https://jwt.io/)
- [RFC7517 - JSON Web Key](https://www.rfc-editor.org/rfc/rfc7517)
- [mkjwk.org - JWK Generator](https://mkjwk.org/)
- [OWASP MAS](https://mas.owasp.org/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [Digikoppeling REST-API](https://gitdocumentatie.logius.nl/publicatie/dk/restapi/)

### 1.4 Definities

| Afkorting | Betekenis                     |
|-----------|-------------------------------|
| JWK       | JSON Web Key                  |
| JWT       | JSON Web Token                |
| JWE       | JSON Web Encryption           |

---

## 2. Globaal Ontwerp

### 2.1 Context

**Entiteiten:**

- BOA App  
- BOA Backend  
- RDW API (Digikoppeling REST API)

**Stappen:**

1. BOA start bevraging, BSN en geboortedatum worden opgehaald.
2. Data + ephemeral public key worden via backend verzonden naar RDW.
3. RDW retourneert versleutelde pasfoto (JWE).
4. BOA Backend ontvangt, verwerkt en stuurt door.
5. BOA App ontsleutelt JWE met private key.
6. Alle gegevens worden na gebruik gewist.

### 2.2 Technische richtlijnen

**Versleuteling:**

- ECDH-ES + AES256GCM met “Concat KDF” (RFC 7518 §4.6)

**Request voorbeeld:**

```json
{
  "BSN": "123456789",
  "geboortedatum": "2000-08-16",
  "pseudo-id-boa": "Boa-123",
  "ontvanger-publieke-sleutel": {
    "kty": "EC",
    "crv": "P-256",
    "x": "c6rIBg1HEE4qN7y-ppyfISXBf9z2N208QD5XOKX3Oc8",
    "y": "oqeScDnAeZZT5sG3BRwwiQD_c01faYWU8AOqI4bdbag"
  }
}
```

**Reply voorbeeld:**

```json
{
  "transactie-id": "7bdba0d1-bc9b-4e2a-b69e-4308a8373d32",
  "pasfoto-id": 1,
  "pasfoto-jwe": "eyJhbGciOiJFQ0RILUVTIiwiZW5jIjoiQTI1NkdDTSIs..."
}
```

### 2.3 Security

| Aspect         | Maatregel                                                               |
|----------------|-------------------------------------------------------------------------|
| Vertrouwelijkheid | TLS + JWE pasfoto encryptie                                         |
| Integriteit     | JWE garandeert data-integriteit                                       |
| Authenticiteit  | PKIO certificaat BOA werkgever                                        |

**Dreigingen:**

- Spoofing: verantwoordelijkheid BOA werkgever  
- Tampering: backend moet voldoende beveiligen  
- Repudiation: traceerbaar via PKIO  
- Information Disclosure: TLS + JWE  
- DoS: RDW bescherming  
- Elevation of privilege: niet van toepassing

---

## 3. Berichten

### 3.1 Request gegevens

- **BSN**: 9 cijfers (met 11-proef)  
- **Geboortedatum**: `YYYY-MM-DD` of `YYYY-00-00`  
- **Publieke sleutel**: EC key met `P-256`

**Voorbeeld:**

```json
{
  "BSN": "123456789",
  "geboortedatum": "2000-08-16",
  "ontvanger-publieke-sleutel": {
    "kty": "EC",
    "crv": "P-256",
    "x": "NjB_LBvIlsEMbqkJYY1cC0ZFKZ3ISC6CtvADYhX53zQ",
    "y": "WPUY5Dq7qT_kJP3U4EYm70BzRRnyMTTXhQsXpHSdkKQ"
  }
}
```

### 3.2 Reply gegevens

- **transactie-id**: UUID  
- **pasfoto-id**: index  
- **pasfoto-jwe**: versleutelde JWE string  

**JWE payload (na decryptie):**

```json
{
  "pasfoto": "/9j/4AAQSkZJRgABAQAAAQABAAD/...",
  "format": "jpg",
  "encoding": "base64"
}
```

---

## 3.1 Berichtvalidatie

### Publieke sleutel

| Validatie                        | Foutcode                             |
|----------------------------------|--------------------------------------|
| Type EC                          | 422 Unprocessable Content            |
| Curve P-256                      | 422 Unprocessable Content            |
| Onjuiste sleutelstructuur        | 500 Internal Server Error            |

### BSN

- Moet voldoen aan 11-proef  
- **Foutcode**: 422

### Geboortedatum

- ISO 8601 (`YYYY-MM-DD`, `YYYY-00-00`)  
- **Foutcode**: 422

### Geen match

- Indien geen pasfoto gevonden: **404 Not Found**

### Algemene fouten

- Verplichte attributen missen: **422**  
- Foutieve JSON: **422**  
- Overig/onvoorzien: **422** of **500**

---

**Bronnen:**

- [Elfproef - Wikipedia](https://nl.wikipedia.org/wiki/Elfproef#Burgerservicenummer)  
- [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html)
