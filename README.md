# ProFlow 240 Control

Aplicativo Linux para controlar o Watercooler Jungle Leopard ProFlow 240 com interface gráfica profissional.

## ✨ Recursos

- 🎨 Interface gráfica moderna com PyQt6
- 🖼️ Suporte para imagens, GIFs e vídeos
- 📱 Escalamento automático sem distorção
- 🔄 Controle de orientação (0°, 90°, 180°, 270°)
- 🔐 Sem necessidade de sudo repetido
- 🎯 Preview em tempo real
- ⚙️ Configurações personalizáveis

## 📋 Requisitos

- Python 3.9+
- Linux (testado em CachyOS)
- Acesso USB ao watercooler

## 🚀 Instalação

### Via Clone

```bash
git clone https://github.com/fimimo/proflow-240-control.git
cd proflow-240-control
pip install -r requirements.txt
```

### Permissões USB

Para evitar usar `sudo` toda vez:

```bash
sudo python setup.py install_usb_rules
```

Ou manualmente:

```bash
sudo cp udev/99-proflow.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## ▶️ Uso

```bash
python src/main.py
```

## 📁 Estrutura do Projeto

```
proflow-240-control/
├── src/
│   ├── main.py                 # Ponto de entrada
│   ├── ui/
│   │   ├── main_window.py      # Interface principal
│   │   ├── widgets.py          # Componentes customizados
│   │   └── styles.py           # Temas e estilos
│   ├── device/
│   │   ├── usb_handler.py      # Comunicação USB
│   │   └── protocol.py         # Protocolo do device
│   ├── media/
│   │   ├── image_processor.py  # Processamento de imagens
│   │   └── video_handler.py    # Suporte a vídeos
│   └── utils/
│       ├── config.py           # Configurações
│       └── logger.py           # Sistema de logs
├── resources/
│   └── icons/                  # Ícones da interface
├── udev/
│   └── 99-proflow.rules        # Regras de permissão USB
├── requirements.txt
├── setup.py
└── README.md
```

## 🔧 Informações do Device

**USB Device ID:** 
- VID: 0x33C3
- PID: 0x7792
- Class: Communication Device (0x02)
- Caminho: `PCIROOT(0)#PCI(0102)#PCI(0000)#USBROOT(0)#USB(11)#USB(1)`

## 📸 Screenshots

[Em breve]

## 🐛 Troubleshooting

### Device não encontrado

```bash
lsusb | grep 33c3
```

Se não aparecer, verifique a conexão USB.

### Erro de permissão

Execute:

```bash
sudo python -m proflow-240-control
```

Ou instale as regras udev.

## 📝 Licença

MIT

## 👤 Autor

fimimo