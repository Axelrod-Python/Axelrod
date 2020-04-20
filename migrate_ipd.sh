#!/bin/sh
# Migrates data for ipd.  Will delete later.

# Manually move most files into ipd.
# Change any axelrod.ipd to axelrod if the IDE tried to change any.

# Replace Player with IpdPlayer
# find . -type f -name "*.py" -exec sed -i 's/\([^A-Za-z]\)Player\([^A-Za-z]\)/\1IpdPlayer\2/g' {} ';'
# find . -type f -name "*.py" -exec sed -i 's/^Player\([^A-Za-z]\)/IpdPlayer\1/g' {} ';'
# find . -type f -name "*.py" -exec sed -i 's/\([^A-Za-z]\)Player$/\1IpdPlayer/g' {} ';'
# find . -type f -name "*.py" -exec sed -i 's/^Player$/IpdPlayer/g' {} ';'

# Replace Match with IpdMatch
# find . -type f -name "*.py" -exec sed -i 's/\([^A-Za-z]\)Match\([^A-Za-z]\)/\1IpdMatch\2/g' {} ';'
# find . -type f -name "*.py" -exec sed -i 's/^Match\([^A-Za-z]\)/IpdMatch\1/g' {} ';'
# find . -type f -name "*.py" -exec sed -i 's/\([^A-Za-z]\)Match$/\1IpdMatch/g' {} ';'
# find . -type f -name "*.py" -exec sed -i 's/^Match$/IpdMatch/g' {} ';'

# Replace Game with IpdGame
# find . -type f -name "*.py" -exec sed -i 's/\([^A-Za-z]\)Game\([^A-Za-z]\)/\1IpdGame\2/g' {} ';'
# find . -type f -name "*.py" -exec sed -i 's/^Game\([^A-Za-z]\)/IpdGame\1/g' {} ';'
# find . -type f -name "*.py" -exec sed -i 's/\([^A-Za-z]\)Game$/\1IpdGame/g' {} ';'
# find . -type f -name "*.py" -exec sed -i 's/^Game$/IpdGame/g' {} ';'

# Replace Tournament with IpdTournament
# find . -type f -name "*.py" -exec sed -i 's/\([^A-Za-z]\)Tournament\([^A-Za-z]\)/\1IpdTournament\2/g' {} ';'
# find . -type f -name "*.py" -exec sed -i 's/^Tournament\([^A-Za-z]\)/IpdTournament\1/g' {} ';'
# find . -type f -name "*.py" -exec sed -i 's/\([^A-Za-z]\)Tournament$/\1IpdTournament/g' {} ';'
# find . -type f -name "*.py" -exec sed -i 's/^Tournament$/IpdTournament/g' {} ';'

# Undo IpdPlayer for Player in quotes
# find . -type f -name "*.py" -exec sed -i 's/\"IpdPlayer\ /\"Player\ /g' {} ';'
# Manually change remaining "IpdPlayer index" to "Player index"

# Fix imports
# find . -type f -name "*.py" -exec sed -i 's/from\ axelrod\./from\ axelrod\.ipd\./g' {} ';'
# find . -type f -name "*.py" -exec sed -i 's/import\ axelrod\./import\ axelrod\.ipd\./g' {} ';'

# A bunch of stuff needs to be added to __init__, so copy the new file.
# Change "from axelrod.ipd.strategies import FSMPlayer" to "from axelrod.ipd.strategies.finite_state_machines import FSMPlayer" in axelrod_second.py

# find . -type f -name "*.py" -exec sed -i 's/test_outputs/\.\.\/test_outputs/g' {} ';'

# Manually change "axl.match" to "axl.ipd.match" and "axl.plot" to "axl.ipd.match" and "axl.strategy_transformers" to "axl.ipd.strategy_transformers" and "axl.result_set" to "axl.ipd.result_set"
# Manually change path in test_load_data.py
# Manually change "from axelrod.ipd.tests import TestTitForTat" to "from axelrod.ipd.tests.strategies.test_titfortat import TestTitForTat"
# Manually SimpleFSM and SimpleHMM to _strategies.
# Manually fix test_hmm imports
