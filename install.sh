#!/bin/bash

# ProFlow 240 Control - Installation Script for CachyOS/Arch Linux

set -e

echo \"================================================\"
echo \"  ProFlow 240 Control - Installer\"
echo \"================================================\"
echo \"\"

# Colors
GREEN=\"\\033[0;32m\"
YELLOW=\"\\033[1;33m\"
RED=\"\\033[0;31m\"
NC=\"\\033[0m\"

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e \"${RED}❌ Python3 não encontrado!${NC}\"
    echo \"Instale com: sudo pacman -S python\"
    exit 1
fi

echo -e \"${GREEN}✅ Python3 encontrado$(python3 --version)${NC}\"
echo \"\"

# Create virtual environment
echo -e \"${YELLOW}📦 Criando ambiente virtual...${NC}\"
python3 -m venv venv
echo -e \"${GREEN}✅ Ambiente virtual criado${NC}\"
echo \"\"

# Activate virtual environment
echo -e \"${YELLOW}🔄 Ativando ambiente virtual...${NC}\"
source venv/bin/activate
echo -e \"${GREEN}✅ Ambiente virtual ativado${NC}\"
echo \"\"

# Upgrade pip
echo -e \"${YELLOW}📦 Atualizando pip...${NC}\"
pip install --upgrade pip setuptools wheel
echo -e \"${GREEN}✅ Pip atualizado${NC}\"
echo \"\"

# Install requirements
echo -e \"${YELLOW}📦 Instalando dependências...${NC}\"
pip install -r requirements.txt
echo -e \"${GREEN}✅ Dependências instaladas${NC}\"
echo \"\"

# Install udev rules
echo -e \"${YELLOW}🔐 Configurando permissões USB...${NC}\"
if [ -f \"udev/99-proflow.rules\" ]; then
    echo \"Copie as regras udev com:\"
    echo \"  sudo cp udev/99-proflow.rules /etc/udev/rules.d/\"
    echo \"  sudo udevadm control --reload-rules\"
    echo \"  sudo udevadm trigger\"
else
    echo -e \"${RED}❌ Arquivo udev/99-proflow.rules não encontrado${NC}\"
fi
echo \"\"

# Create launcher script
echo -e \"${YELLOW}🚀 Criando script de execução...${NC}\"
cat > run.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
python3 src/main.py
EOF
chmod +x run.sh
echo -e \"${GREEN}✅ Script de execução criado${NC}\"
echo \"\"

# Final instructions
echo \"================================================\"
echo -e \"${GREEN}✅ Instalação concluída!${NC}\"
echo \"================================================\"
echo \"\"
echo \"Próximos passos:\"
echo \"\"
echo \"1️⃣  Configure as permissões USB (necessário fazer apenas uma vez):\"
echo \"    sudo cp udev/99-proflow.rules /etc/udev/rules.d/\"
echo \"    sudo udevadm control --reload-rules\"
echo \"    sudo udevadm trigger\"
echo \"\"
echo \"2️⃣  Execute a aplicação com:\"
echo \"    ./run.sh\"
echo \"\"
echo \"   ou manualmente:\"
echo \"    source venv/bin/activate\"
echo \"    python3 src/main.py\"
echo \"\"
echo \"================================================\"
