# Absolum save data

[Download the modified save from Releases](https://github.com/VdustR/game-data-absolum/releases).

> [!CAUTION]
> Use at your own risk. Back up your save before replacing it.

**Tested on:** Absolum **v05 r35192**, Windows Steam.

## What this save changes

- Sets Radiance level to **999**. Current balances: **1,000,834** Crystals, **999,999** Primordial Roots, and **999,999** Meta Fruits.
- Enables the known character growth, upgrades, purchases, and unlock flags in this save.
- Shows **17 Mystic Ordeals** with gold icons and all visible medals, including the completed **Fortitude Ordeal**.
- Contains **119 battle records**. Edited records use strings of 9s for scores and tracked stats, a **9:59** timer, **999** clashes, deflects, and dodges, and **0** damage taken. The 68 generated ordeal runs cover four characters per ordeal and rotate five authentic skills per character.

**Still unresolved:** Global progress remains at **111%**, one point short of 112%.

## Install

1. Exit Absolum.
2. Back up `Save.bin` and `Save.temp.bin` in `%LOCALAPPDATA%\Absolum_SaveGame_Steam`.
3. Extract the Release ZIP and copy its two files into that folder.
4. Launch the game and check your save slot and battle records.

This save was checked in game on the tested version above. Compatibility with other builds is unknown.

## Scripts

`gen.py` recreates the battle-record and medal pattern from this save and later saves that retain its first **118 records**. It requires Python 3 and does not overwrite its input or an existing output save.

```text
python gen.py path/to/source/Save.bin path/to/output-folder
python test.py path/to/source/Save.bin path/to/output-folder/Save.bin
```

`test.py` checks the generated records and confirms that non-history data is preserved. Load any generated save in game before using it as your main save.

[Save format notes](SAVE_FORMAT.md) document the Fortitude completion record, medal fields, and field ordering observed in this game build.

## License

Code and documentation are licensed under [MIT](LICENSE). The save file is distributed through Releases.
