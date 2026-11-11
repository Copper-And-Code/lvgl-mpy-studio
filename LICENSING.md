# Licensing

LVGL MPY Studio uses two licenses, so the IDE stays free and users can do what they want with their own products.

| Part | License |
|---|---|
| The IDE: `lvgl_mpy_studio/` except as noted below, tests and packaging scripts | GPL-3.0-or-later, text in `LICENSE` |
| Code the IDE generates for your projects | MIT, text in `LICENSE-MIT.txt` |
| What the IDE embeds in projects and executables: `lvgl_mpy_studio/gen/output/`, `native/lvsim/`, `runtime/display_driver.py` | MIT |

## Generated code

Code the IDE generates from your projects, including the IDE fragments that end up in it, is under the MIT license, not the GPL. This also applies to executables built with the IDE: the IDE's GPL does not extend to your products.

Your projects and the code you write remain yours: the IDE acquires no rights over them.

Library licenses remain those of their authors: LVGL and MicroPython, for example, are MIT. Notices are in `THIRD_PARTY.md`, and the IDE copies the license texts next to the executables it creates. If you distribute them, keep the `licenses` folder with the executable.

This document summarizes the licenses and is not legal advice.

---

# Licenze

LVGL MPY Studio usa due licenze, così l'IDE resta libero e chi lo usa può fare ciò che vuole con i propri prodotti.

| Parte | Licenza |
|---|---|
| L'IDE: `lvgl_mpy_studio/`, salvo quanto indicato sotto, test e script di pacchetto | GPL-3.0-or-later, testo in `LICENSE` |
| Il codice generato dall'IDE per i tuoi progetti | MIT, testo in `LICENSE-MIT.txt` |
| Ciò che l'IDE incorpora nei progetti e negli eseguibili: `lvgl_mpy_studio/gen/output/`, `native/lvsim/`, `runtime/display_driver.py` | MIT |

## Il codice generato

Il codice che l'IDE genera dai tuoi progetti, compresi i frammenti dell'IDE che vi finiscono dentro, è sotto licenza MIT, non GPL. Questo vale anche per gli eseguibili creati con l'IDE: la GPL dell'IDE non si estende ai tuoi prodotti.

I tuoi progetti e il codice che scrivi restano tuoi: l'IDE non ne acquisisce alcun diritto.

Le licenze delle librerie restano quelle dei rispettivi autori: LVGL e MicroPython, per esempio, sono MIT. Gli avvisi sono in `THIRD_PARTY.md` e l'IDE copia i testi delle licenze accanto agli eseguibili che crea. Se li distribuisci, tieni la cartella `licenses` insieme all'eseguibile.

Questo documento riassume le licenze e non è un parere legale.
