#!/bin/bash
"""
Environment Setup Script for StickBot
Activates the solo_venv virtual environment and sets up the Python environment
"""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up StickBot environment...${NC}"

# Check if solo_venv exists
if [ ! -d "$HOME/solo_venv" ]; then
    echo -e "${RED}Error: Virtual environment not found at ~/solo_venv${NC}"
    echo -e "${YELLOW}Please create the virtual environment first:${NC}"
    echo "  python -m venv ~/solo_venv"
    exit 1
fi

# Activate the virtual environment
echo -e "${GREEN}Activating solo_venv...${NC}"
source ~/solo_venv/bin/activate

# Check if activation was successful
if [ -n "$VIRTUAL_ENV" ]; then
    echo -e "${GREEN}Virtual environment activated: $VIRTUAL_ENV${NC}"
else
    echo -e "${RED}Failed to activate virtual environment${NC}"
    exit 1
fi

# Install required packages if not already installed
echo -e "${GREEN}Installing required packages...${NC}"
pip install --quiet inputs RPi.GPIO gpiozero

echo -e "${GREEN}Environment setup complete!${NC}"
echo -e "${YELLOW}You can now run any Python scripts in the examples/ directory${NC}"
echo ""
echo "Available examples:"
echo "  python examples/xbox_controller.py"
echo "  python examples/digital_input.py"
echo "  python examples/digital_output.py"
echo "  python examples/pwm_control.py"
echo "  python examples/realtime_control.py"
echo ""