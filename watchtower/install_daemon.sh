#!/bin/bash
# Install Watchtower Daemon as System Service

set -e

echo "=========================================="
echo "  WATCHTOWER DAEMON INSTALLATION"
echo "=========================================="
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo "Detected: Linux (systemd)"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    echo "Detected: macOS (launchd)"
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

echo ""

# Install daemon service
if [ "$OS" == "linux" ]; then
    # Systemd installation
    echo "Installing systemd service..."

    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    SERVICE_FILE="$SCRIPT_DIR/daemon/watchtower.service"

    # User service directory
    USER_SERVICE_DIR="$HOME/.config/systemd/user"
    mkdir -p "$USER_SERVICE_DIR"

    # Copy service file
    cp "$SERVICE_FILE" "$USER_SERVICE_DIR/watchtower.service"

    echo "✓ Service file installed"

    # Reload systemd
    systemctl --user daemon-reload

    echo "✓ systemd reloaded"

    # Enable service
    echo ""
    echo "Enable Watchtower daemon to start at login? (y/n)"
    read -r response

    if [[ "$response" =~ ^[Yy]$ ]]; then
        systemctl --user enable watchtower.service
        echo "✓ Service enabled"

        echo ""
        echo "Start Watchtower daemon now? (y/n)"
        read -r response2

        if [[ "$response2" =~ ^[Yy]$ ]]; then
            systemctl --user start watchtower.service
            echo "✓ Service started"

            # Show status
            systemctl --user status watchtower.service --no-pager
        fi
    fi

    echo ""
    echo "Daemon management commands:"
    echo "  Start:   systemctl --user start watchtower"
    echo "  Stop:    systemctl --user stop watchtower"
    echo "  Status:  systemctl --user status watchtower"
    echo "  Logs:    journalctl --user -u watchtower -f"

elif [ "$OS" == "macos" ]; then
    # Launchd installation
    echo "Installing launchd service..."

    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    PLIST_FILE="$SCRIPT_DIR/daemon/com.watchtower.daemon.plist"

    # User LaunchAgents directory
    LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
    mkdir -p "$LAUNCH_AGENTS_DIR"

    # Replace %USER% with actual username
    sed "s/%USER%/$USER/g" "$PLIST_FILE" > "$LAUNCH_AGENTS_DIR/com.watchtower.daemon.plist"

    echo "✓ LaunchAgent installed"

    # Load service
    echo ""
    echo "Start Watchtower daemon now? (y/n)"
    read -r response

    if [[ "$response" =~ ^[Yy]$ ]]; then
        launchctl load "$LAUNCH_AGENTS_DIR/com.watchtower.daemon.plist"
        echo "✓ Service loaded and started"
    fi

    echo ""
    echo "Daemon management commands:"
    echo "  Load:    launchctl load ~/Library/LaunchAgents/com.watchtower.daemon.plist"
    echo "  Unload:  launchctl unload ~/Library/LaunchAgents/com.watchtower.daemon.plist"
    echo "  Logs:    tail -f /tmp/watchtower.*.log"
fi

echo ""
echo "=========================================="
echo "  ✓ DAEMON INSTALLATION COMPLETE"
echo "=========================================="
echo ""
