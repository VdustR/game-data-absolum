# Absolum save data

[Download the modified save from Releases](https://github.com/VdustR/game-data-absolum/releases).

> [!CAUTION]
> Use at your own risk. Back up your save before replacing it.

**Tested on:** Absolum **v05 r35192**, Windows Steam.

## Save contents

- Sets Radiance level to **999**. Current balances: **9,999,999** Crystals, **999,999** Primordial Roots, and **999,999** Meta Fruits.
- Enables the known character growth, upgrades, purchases, and unlock flags in this save.
- Shows **17 Mystic Ordeals** with gold icons and visible medals, including all four character medals for the completed **Fortitude Ordeal**.
- Contains **119 battle records**. Scores and tracked stats use obvious strings of 9s; clashes, deflects, and dodges are **999**, and damage taken is **0**. The 68 generated ordeal runs cover four characters per ordeal and rotate five authentic skills per character.

Overall progress currently shows **111%**. How to reach **112%** is unknown.

## Install

1. Exit Absolum.
2. Back up `Save.bin` and `Save.temp.bin` in `%LOCALAPPDATA%\Absolum_SaveGame_Steam`.
3. Extract the Release ZIP and copy its two files into that folder.
4. Launch the game and check your save slot and battle records.

This save was checked in game on the tested version above.

## Scripts

`gen.py` recreates the battle records and medals, sets Radiance to 999, and fills all three resource balances with 9s matching their current digit counts. Its input must contain the **genuine completed Fortitude run as record 119** and the existing growth and unlock flags. It does not overwrite its input or an existing output save.

```text
python gen.py path/to/source/Save.bin path/to/output-folder
python test.py path/to/source/Save.bin path/to/output-folder/Save.bin
```

`test.py` checks the generated records, Radiance, resources, and preservation of other data. Load any generated save in game before using it as your main save.

[Save format notes](SAVE_FORMAT.md) document the Fortitude completion record, medal fields, and field ordering observed in this game build.

## License

Code and documentation are licensed under [MIT](LICENSE). The save file is distributed through Releases.
