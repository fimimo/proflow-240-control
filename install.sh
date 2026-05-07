#!/bin/bash

# ProFlow 240 Control - Installation Script for CachyOS/Arch Linux

set -e

echo "================================================"
echo "  ProFlow 240 Control - Installer"
echo "================================================"
echo ""

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found!"
    echo "Install with: sudo pacman -S python"
    exit 1
fi

echo "Python3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "Virtual environment activated"
echo ""

# Upgrade pip
echo "Updating pip..."
pip install --upgrade pip setuptools wheel
echo "Pip updated"
echo ""

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Dependencies installed"
echo ""

# Install udev rules
echo "Configuring USB permissions..."
if [ -f "udev/99-proflow.rules" ]; then
    echo "Copy udev rules with:"
    echo "  sudo cp udev/99-proflow.rules /etc/udev/rules.d/"
    echo "  sudo udevadm control --reload-rules"
    echo "  sudo udevadm trigger"
else
    echo "File udev/99-proflow.rules not found"
fi
echo ""

# Create launcher script
echo "Creating launcher script..."
cat > run.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
python3 src/main.py
EOF
chmod +x run.sh
echo "Launcher script created"
echo ""

# Final instructions
echo "================================================"
echo "Installation completed!"
echo "================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Configure USB permissions (do this only once):"
echo "   sudo cp udev/99-proflow.rules /etc/udev/rules.d/"
echo "   sudo udevadm control --reload-rules"
echo "   sudo udevadm trigger"
echo ""
echo "2. Run the application with:"
echo "   ./run.sh"
echo ""
echo "   or manually:"
echo "   source venv/bin/activate"
echo "   python3 src/main.py"
echo ""
echo "================================================"
