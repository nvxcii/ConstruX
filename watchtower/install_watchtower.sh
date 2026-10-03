#!/bin/bash
# Watchtower Installation Script (Linux/macOS)

set -e

echo "=========================================="
echo "  WATCHTOWER INSTALLATION"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is required but not installed.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ pip3 found${NC}"

# Install Python dependencies
echo ""
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip3 install -r requirements.txt

echo -e "${GREEN}✓ Dependencies installed${NC}"

# Create symlink for CLI
echo ""
echo -e "${BLUE}Setting up Watchtower CLI...${NC}"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CLI_PATH="$SCRIPT_DIR/watchtower_cli.py"

# Make CLI executable
chmod +x "$CLI_PATH"

# Determine install location
if [ -w "/usr/local/bin" ]; then
    INSTALL_DIR="/usr/local/bin"
else
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
fi

# Create symlink
ln -sf "$CLI_PATH" "$INSTALL_DIR/watchtower"

echo -e "${GREEN}✓ CLI installed to ${INSTALL_DIR}/watchtower${NC}"

# Add to PATH if needed
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo -e "${YELLOW}⚠️  Add ${INSTALL_DIR} to your PATH:${NC}"
    echo -e "   ${BLUE}export PATH=\"\$PATH:$INSTALL_DIR\"${NC}"
    echo ""
    echo "Add this line to your ~/.bashrc or ~/.zshrc"
fi

# Initialize field
echo ""
echo -e "${BLUE}Do you want to initialize your field now? (y/n)${NC}"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    python3 "$CLI_PATH" init
fi

echo ""
echo "=========================================="
echo -e "${GREEN}  ✓ WATCHTOWER INSTALLED${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Run: watchtower status"
echo "  2. Start daemon: watchtower daemon start"
echo "  3. View glyphs: watchtower glyphs list"
echo ""
echo "For help: watchtower --help"
echo ""
