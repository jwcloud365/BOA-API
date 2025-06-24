
# Testdata met voorbeelden v0.1 – BOA bevraging rijbewijzenregister

**Datum**: 10-06-2025  
**Versie**: 0.1  
**Status**: Concept  

---

## Revisies

| Versie | Datum      | Auteur(s)     | Omschrijving       |
|--------|------------|---------------|--------------------|
| 0.1    | 10-06-2025 | M. Popma      | Initiële versie     |

---

## Colofon

- **Locatie**: Veendam  
- **Projectnaam**: Toegang Rijbewijsregister voor BOA’s  
- **Projectleider**: Robert Soldaat  
- **Contactpersonen**: Alfred Velthuis, Marius Popma  

---

## Bijlage: Testdata

Voor de testgevallen worden BSN-nummers gekozen uit de BSN-lijst van RvIG. Door deze test-BSN’s te gebruiken weten we zeker dat er niet per ongeluk bestaande BSN’s getest worden.  

**Bron**: [RvIG Test BSN's](https://www.rvig.nl/test-bsn-a-nummers-omnummertabel)

---

### BSN’s waarbij een foto gevonden kan worden  
(*geboortedatum willekeurig in te vullen*)

- Test-BSN 1682: `999998523`  
- Test-BSN 1683: `999998535`  
- Test-BSN 1684: `999998547`  
- Test-BSN 1685: `999998559`  
- Test-BSN 1686: `999998560`  

*(Foto’s gegenereerd met ChatGPT)*  
Controle via: [Pimeyes](http://www.pimeyes.com)

---

### BSN’s waarbij **geen** foto gevonden kan worden  
(*BSN’s voldoen wel aan 11-proef*)

- Test-BSN 1687: `999998572`  
- Test-BSN 1688: `999998584`  
- Test-BSN 1689: `999998596`  
- Test-BSN 1690: `999998602`  
- Test-BSN 1691: `999998614`  

---

### BSN die **niet voldoet** aan de 11-proef  

- Test-BSN 1692: `999998620`  
(*Voldoet niet aan 11-proef – te gebruiken voor foutsituatie*)
