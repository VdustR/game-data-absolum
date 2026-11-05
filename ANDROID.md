# Android save installation

Tested November 5, 2026 with **Absolum 1.0.148 (148)**, package `com.playdigious.absolum`, on a Samsung **SM-S9110**. The adapted save loaded into camp, with Radiance **999** and **111%** overall progress visible. This procedure replaces the existing progress with the release's full progress, unlocks, and 119 battle records.

## Package contents

Download [the Android 1.0.148 package](https://github.com/VdustR/game-data-absolum/releases/download/android-1.0.148-save-1/Absolum-Fortitude-complete-Android-1.0.148.zip) from the dedicated Android release. The Windows Steam save has a separate release.

- `template/Save.bin` and `template/Save.temp.bin`: the complete Steam release progress, without a phone's identifier-like field.
- `android_save.py` and `proto_wire.py`: Python 3 tools for adapting the template locally.
- `test_android.py`: synthetic transfer and overwrite-protection checks (`python -m unittest -v test_android`).
- `README.md`: these installation instructions.
- `ANDROID.md`: a copy of these instructions for links from the format notes.
- `SAVE_FORMAT.md`: observed fields and the limits of testing.
- `LICENSE`: the code and documentation license.

The template files are not ready-to-copy Android saves. Run the tool with a save from your own phone. The package intentionally excludes the tested phone's field-21 value.

## Install with ADB

This requires Python 3 and Android Platform Tools (`adb`) on the computer, and an authorized USB-debugging connection. ADB could access the app's external save directory on the tested phone; access on other Android configurations is not established. If access is denied, stop rather than changing device security settings as part of this procedure.

Run the following commands from the extracted package directory. Replace `DEVICE_SERIAL` with your phone's serial from `adb devices -l`. Keep the game closed until both replacement files have been copied.

1. Verify the target phone, then stop Absolum:

   ```sh
   adb devices -l
   adb -s DEVICE_SERIAL shell am force-stop com.playdigious.absolum
   ```

2. Copy the current save directory to a new local backup folder. Keep it until the replacement works:

   ```sh
   adb -s DEVICE_SERIAL pull /sdcard/Android/data/com.playdigious.absolum/files/GuardCrushGames/Absolum phone-backup
   ```

   Check that `phone-backup/Save.bin` and `phone-backup/Save.temp.bin` exist before proceeding.

3. Generate the adapted files in a new directory:

   ```sh
   python android_save.py template/Save.bin phone-backup/Save.bin android-output
   ```

   The tool leaves both inputs untouched, retains the phone's field 21, and refuses an existing output directory. It rejects missing or duplicate field 21, a template containing field 21, mismatched field-19 markers, layouts without three slots, and additional unrecognized phone-only top-level fields. These checks bound the observed layout; they do not prove compatibility with another game version. Keep the generated files local because they contain the phone's identifier-like value.

4. Copy both generated files to the phone:

   ```sh
   adb -s DEVICE_SERIAL push android-output/Save.bin /sdcard/Android/data/com.playdigious.absolum/files/GuardCrushGames/Absolum/Save.bin
   adb -s DEVICE_SERIAL push android-output/Save.temp.bin /sdcard/Android/data/com.playdigious.absolum/files/GuardCrushGames/Absolum/Save.temp.bin
   ```

5. Open Absolum, select the first slot, and check Radiance 999, 111% progress, and successful camp loading. If loading fails, close the game and restore both files from `phone-backup` to the same paths.

## What was verified

The tested output preserved every Steam release field and appended only the local Android field 21. Both files were copied to the phone and their SHA256 hashes matched the prepared files. The game recognized the slot and loaded the camp scene with four characters visible. Structural checks confirmed 119 battle records, Radiance 999, and file balances of 9,999,999 Crystals and 999,999 each of Primordial Roots and Meta Fruits.

The camp HUD displayed **9,999,869** Crystals, 130 fewer than the file value, while the immediate file readback still showed 9,999,999. The cause and later persistence of that difference are unknown.

The 17-ordeal medal display was verified previously on Windows, but was not checked individually on Android. Extended gameplay, cloud synchronization, other Android versions/devices, iOS, reverse transfer to Steam, and direct installation of the unadapted Steam file were not tested. Field 21's meaning and whether it is required remain unknown; preserving it repeats the successful procedure without claiming a requirement.

See [save format notes](SAVE_FORMAT.md) for the underlying observations.
