# Set the current working directory to the directory of the script
cd "$(dirname "$0")"

# Check for .env file
if [ -f .env ]; then
  echo ".env file found"
else
  echo "Creating .env file"
  cp ../.env.example .env
  echo ".env file created"
fi
echo ""


# Check for i/o paths
echo "Checking for i/o paths"
OUTPUT_PATH=$(grep "^OUTPUT_PATH" .env | cut -d '=' -f2- | tr -d ' "')
POKEMON_INPUT_PATH=$(grep "^POKEMON_INPUT_PATH" .env | cut -d '=' -f2- | tr -d ' "')
POKEMON_OUTPUT_PATH=$(grep "^POKEMON_OUTPUT_PATH" .env | cut -d '=' -f2- | tr -d ' "')
WILD_ENCOUNTER_PATH=$(grep "^WILD_ENCOUNTER_PATH" .env | cut -d '=' -f2- | tr -d ' "')
if [ -f $POKEMON_INPUT_PATH ]; then
  echo "Pokemon input data found"
else
  echo "Pokemon input data not found"
  echo "Please use the following link to download the data:"
  echo "https://github.com/zhenga8533/pokeapi-parser/tree/v1"
fi
echo ""


# Check if "python" is available and is version 3
if command -v python &> /dev/null && [[ $(python -c "import sys; print(sys.version_info.major)" 2>/dev/null) == "3" ]]; then
    PYTHON="python"
    PIP="pip"
# Check if "python3" is available and is version 3
elif command -v python3 &> /dev/null && [[ $(python3 -c "import sys; print(sys.version_info.major)" 2>/dev/null) == "3" ]]; then
    PYTHON="python3"
    PIP="pip3"
else
    echo "No compatible Python 3 interpreter found."
    exit 1
fi
echo "Using $PYTHON"
echo ""


# Install requirements
if [ -f ../requirements.txt ]; then
  $PIP install -r ../requirements.txt
  echo "Requirements installed"
else
  echo "No requirements file found"
fi
echo ""


# Run all parsers
echo "Running all parsers"
$PYTHON action_replay_codes.py
$PYTHON important_trainer_rosters.py
$PYTHON item_&_trade_changes.py
$PYTHON level_up_move_changes.py
$PYTHON pokemon_changes.py
$PYTHON trainer_rosters.py
$PYTHON wild_pokemon.py

$PYTHON pokemon.py
$PYTHON wild_encounters.py
echo "All parsers ran successfully"

# Replace existing files with new ones
rm $OUTPUT_PATH/pokemon_nav.md
rm $OUTPUT_PATH/wild_nav.md

mkdir -p ../docs/mechanics
mkdir -p ../docs/pokemon
mkdir -p ../docs/wild_encounters

cp -r -f -u $OUTPUT_PATH/* ../docs/mechanics
cp -r -f -u $POKEMON_OUTPUT_PATH/* ../docs/pokemon
cp -r -f -u $WILD_ENCOUNTER_PATH/* ../docs/wild_encounters
