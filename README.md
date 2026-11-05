# Absolum save data

Modified Absolum saves and tools for Windows Steam and Android, with separate releases for each platform.

> [!CAUTION]
> Use at your own risk. Back up your save before replacing it.

## Downloads and tested versions

- [Windows Steam release](https://github.com/VdustR/game-data-absolum/releases/tag/v05-r35192-save-2): ready-to-copy save files, tested with Absolum **v05 r35192**. Follow the [Windows installation steps](#install-on-windows-steam).
- [Android release](https://github.com/VdustR/game-data-absolum/releases/tag/android-1.0.148-save-1): a save template and local adaptation tools, tested with Absolum **1.0.148 (148)** on a Samsung **SM-S9110** on November 5, 2026. Follow the [Android instructions](ANDROID.md) to generate files using your own phone save before installing them.

The adapted Android save was recognized and loaded into camp, displaying Radiance 999 and 111% progress. Individual ordeal medals were not rechecked on Android.

## Save contents

- Sets Radiance level to **999**. File balances: **9,999,999** Crystals, **999,999** Primordial Roots, and **999,999** Meta Fruits.
- Enables the known character growth, upgrades, purchases, and unlock flags in this save.
- On Windows Steam, shows **17 Mystic Ordeals** with gold icons and visible medals, including all four character medals for the completed **Fortitude Ordeal**.
- Contains **119 battle records**. Scores and tracked stats use obvious strings of 9s; clashes, deflects, and dodges are **999**, and damage taken is **0**. The 68 generated ordeal runs cover four characters per ordeal and rotate five authentic skills per character.

Overall progress currently shows **111%**. How to reach **112%** is unknown.

On Android, the camp HUD showed **9,999,869** Crystals while the immediate file readback still contained **9,999,999**. The cause of this difference is unknown. See the [Android observations and unverified behavior](SAVE_FORMAT.md#android-compatibility-observation).

## Install on Windows Steam

1. Exit Absolum.
2. Back up `Save.bin` and `Save.temp.bin` in `%LOCALAPPDATA%\Absolum_SaveGame_Steam`.
3. Extract the ZIP from the [Windows Steam release](https://github.com/VdustR/game-data-absolum/releases/tag/v05-r35192-save-2) and copy its two files into that folder.
4. Launch the game and check your save slot and battle records.

This save was checked in game on Windows Steam **v05 r35192**.

## Install on Android

Follow [Android installation and compatibility notes](ANDROID.md). The Android package preserves a field from your own phone save during adaptation. Its bundled template is not a ready-to-copy Android save.

## Scripts

`gen.py` recreates the battle records and medals, sets Radiance to 999, and fills all three resource balances with 9s matching their current digit counts. Its input must contain the **genuine completed Fortitude run as record 119** and the existing growth and unlock flags. It does not overwrite its input or an existing output save.

```text
python gen.py path/to/source/Save.bin path/to/output-folder
python test.py path/to/source/Save.bin path/to/output-folder/Save.bin
```

`test.py` checks the generated records, Radiance, resources, and preservation of other data. Load any generated save in game before using it as your main save.

[Save format notes](SAVE_FORMAT.md) document the Fortitude completion record, medal fields, and field ordering observed in this game build.

`android_save.py` combines the release template with the local phone save's top-level field 21 without changing either input. It creates a new output directory containing both save files. It does not edit a connected device.

```text
python android_save.py path/to/template/Save.bin path/to/phone/Save.bin path/to/new-output-folder
python -m unittest -v test_android
```

## License

Code and documentation are licensed under [MIT](LICENSE). The save file is distributed through Releases.
