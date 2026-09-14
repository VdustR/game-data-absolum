# Save format notes (Steam v05 r35192)

These notes come from comparing an untouched save before and after a player completed the Fortitude Ordeal, then loading edited copies in game. They describe this build only.

## Fortitude Ordeal

- The completed run adds a **119th battle-history record** (index 118). The pre-run save had 118 records. The real record identifies the Rogue; the generator leaves its character and selected skill unchanged.
- The real Fortitude record has `Perma.CO_Preset = 18 * 65536`. Four older generated Fortitude records used `17 * 65536` while their character medals stayed dark, despite having four character IDs and the expected ordeal success keys. The generator now corrects this preset ID in those four records; the visual effect still needs a game check.
- The run includes `Run.CO_Preset_SUCCESS_ORDEAL_GROUNDHOG` in its tracking data. Completion also changed `Perma.FixRaw.CO_Ordeals_Succeeded` from 16 to 18 and added `Perma.CO_Preset_SUCCESS_GROUNDHOG`. Preserve these values from the real post-run save.
- The five tracking values associated with Fortitude's rule medals are `Run.Tracking.FixRaw.ShopItemsBought`, `Run.Badge_UltimateUses`, `Run.Badge_MercenariesBought`, `Run.Badge_ThrowableUses`, and `Run.Tracking.FixRaw.LifeHealed`. Setting all five to zero in the highest-score Fortitude record lit the rule medals, but did not light its four character medals. `Run.Badge_UltimateUses` was absent from the real record and must be added.
- Tracking entries are protobuf field 50 inside each history record. Insert missing field-50 entries alongside existing field-50 entries, before later fields. Appending the missing entry at the end made the game discard most tracking entries when it saved again.
- The game still displayed **111%** after the real completion. Four speculative Legacy flags did not increase it and are excluded from the generated save.

## Generated records

Records 50–117 cover 17 ordeals with four characters per ordeal. `gen.py` retains that layout and cycles through five selected skills found in the original first 50 records for each character. It edits scores and tracked statistics into obvious 9 patterns and sets the medal tracking values above to zero. `test.py` checks the 17-by-4 layout, five-skill cycle, unchanged non-history data, and the required tracking values.

Use an untouched post-Fortitude save as input when reproducing the 119-record version. The scripts do not create genuine completion data for a trial that has not been cleared.
