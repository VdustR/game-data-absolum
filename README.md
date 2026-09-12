# Absolum save data

[Download the modified save from Releases](https://github.com/VdustR/game-data-absolum/releases).

> [!CAUTION]
> Use at your own risk. Back up your save before replacing it.

**Tested on:** Absolum **v05 r35192**, Windows Steam.

## What this save changes

- Sets Radiance level to **999** and Crystals, Primordial Roots, and Meta Fruits to **999,999** each.
- Enables the known character growth, upgrades, purchases, and unlock flags in this save.
- Marks **16 Mystic Ordeals** gold and gives each one records for all four characters. Some challenge rules remain locked.
- Expands battle history to **118 runs**. Edited records use conspicuous strings of 9s for scores and tracked stats, a **9:59** timer, **999** clashes, deflects, and dodges, and **0** damage taken. Synthetic ordeal runs rotate selected skills by character.

**Still unresolved:** The completion counter is missing 1%, and the **Courage trial (勇氣試煉)** is not unlocked.

## Install

1. Exit Absolum.
2. Back up `Save.bin` and `Save.temp.bin` in `%LOCALAPPDATA%\Absolum_SaveGame_Steam`.
3. Extract the Release ZIP and copy its two files into that folder.
4. Launch the game and check your save slot and battle records.

This save was checked in game on the tested version above. Compatibility with other builds is unknown.

## Scripts

`gen.py` recreates the battle-record pattern from the specific **118-record** save used for this release. It requires Python 3 and does not overwrite its input or an existing output save.

```text
python gen.py path/to/source/Save.bin path/to/output-folder
python test.py path/to/source/Save.bin path/to/output-folder/Save.bin
```

`test.py` checks the generated records and confirms that non-history data is preserved. Load any generated save in game before using it as your main save.

## License

Code and documentation are licensed under [MIT](LICENSE). The save file is distributed through Releases.
