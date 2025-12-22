# Taskly 🖥️

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flet](https://img.shields.io/badge/Flet-0.28+-5C2D91?style=for-the-badge&logo=flutter&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey?style=for-the-badge)

**A modern, elegant system monitor with Apple-style UI built with Python and Flet**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Contributing](#-contributing)

<img src="https://img.shields.io/github/stars/axel-g-dev/Taskly?style=social" alt="GitHub stars">
<img src="https://img.shields.io/github/forks/axel-g-dev/Taskly?style=social" alt="GitHub forks">

</div>

---

## ✨ Features

### 📊 Real-Time Monitoring
- **CPU** - Usage percentage (0-100%), core count, frequency
- **RAM** - Memory usage with used/total display
- **Temperature** - CPU temperature with color-coded indicators (green/orange/red)
- **Network** - Real-time upload/download speeds
- **Battery** - Level, charging status, time remaining
- **Disk** - Storage usage and capacity

### 📈 Data Visualization
- **3 Historical Charts** - CPU, RAM, and Network (30-second history)
- **Dual Network Chart** - Separate upload (cyan) and download (green) lines
- **Metric Cards** - Color-coded cards with progress bars
- **Process List** - Top 7 processes by CPU or RAM usage

### 🔔 Smart Alerts
- **Configurable Thresholds** - CPU (90%), RAM (85%), Temperature (80°C)
- **Alert Levels** - Warning and Critical states
- **Cooldown System** - 30-second cooldown between similar alerts
- **Visual Panel** - Color-coded alerts with timestamps

### 💾 Data Export
- **JSON Format** - Complete structured data with history arrays
- **CSV Format** - Human-readable tables for Excel/Google Sheets
- **Auto-Save** - Files saved to `./exports/` with timestamps
- **Comprehensive** - All metrics, history, and system info included

### ⚡ Performance Optimizations
- **Smart Caching** - Disk and battery updated every 5s instead of 1s
- **Optimized History** - 30 data points instead of 60 (-50% memory)
- **Conditional Updates** - UI updates only when values change >0.5%
- **Modular Architecture** - Clean, reusable component structure

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/axel-g-dev/Taskly.git
cd Taskly

# Create virtual environment
python3 -m venv env

# Activate virtual environment
source env/bin/activate  # macOS/Linux
# or
env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### macOS Temperature Monitoring (Optional)

To enable CPU temperature monitoring on macOS, install `osx-cpu-temp`:

```bash
# Install via Homebrew
brew install osx-cpu-temp

# Verify installation
osx-cpu-temp
```

> **Note**: Temperature monitoring works out-of-the-box on Linux. On macOS, it requires `osx-cpu-temp`. On Windows, support varies by hardware.

---

## 🎮 Usage

### Running the Application

```bash
# Activate virtual environment
source env/bin/activate

# Launch Taskly
python main.py
```

> **⚠️ Important:** Only run the application **once**. Each execution opens a new Flet window.

### Interface Overview

**Header Buttons:**
- 🕐 **Clock** - Real-time clock
- 📥 **Export** - Export data to JSON + CSV
- 🔔 **Alerts** - Toggle alert panel
- ℹ️ **Info** - Toggle detailed system information

**Metric Cards (Top Row):**
- **CPU** (Blue) - Processor usage 0-100%
- **RAM** (Purple) - Memory usage
- **Temperature** (Orange) - CPU temperature (if available)
- **Network** (Green) - Download speed

**Charts (Middle Row):**
- **CPU History** - 30-second CPU usage history
- **Memory History** - 30-second RAM usage history
- **Network History** - Upload + Download speeds

**Process List (Bottom):**
- Sort by CPU or RAM
- Shows top 7 most resource-intensive processes
- Real-time updates

---

## 📸 Screenshots

<div align="center">

### Main Dashboard
![Main Dashboard](https://via.placeholder.com/800x500?text=Main+Dashboard+Screenshot)

### Alert System
![Alert System](https://via.placeholder.com/800x500?text=Alert+System+Screenshot)

### System Info Panel
![System Info](https://via.placeholder.com/800x500?text=System+Info+Screenshot)

</div>

---

## 🏗️ Project Structure

```
Taskly/
├── main.py                      # Entry point
├── dashboard.py                 # Main UI interface
├── data_manager.py              # System metrics collection
├── data_exporter.py             # JSON/CSV export
├── config.py                    # Configuration & theme
├── utils.py                     # Utility functions
├── components/                  # UI Components
│   ├── __init__.py
│   ├── metric_card.py          # Metric display cards
│   ├── temperature_card.py     # Temperature card
│   ├── charts.py               # CPU/RAM/Network charts
│   ├── process_list.py         # Process table
│   ├── system_info.py          # System info panel
│   └── alert_manager.py        # Alert system
├── exports/                     # Exported data (gitignored)
├── env/                         # Virtual environment (gitignored)
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

---

## ⚙️ Configuration

### Alert Thresholds

Edit `config.py` to customize alert thresholds:

```python
ALERT_THRESHOLDS = {
    'cpu': 90,      # Alert if CPU > 90%
    'ram': 85,      # Alert if RAM > 85%
    'temp': 80,     # Alert if Temp > 80°C
}
```

### Performance Settings

```python
UPDATE_INTERVAL = 1.0       # Update interval (seconds)
HISTORY_SIZE = 30           # Number of history data points
CACHE_INTERVAL = 5          # Disk/battery cache interval (seconds)
```

### Debug Logging

```python
DEBUG = True     # Enable debug logs
VERBOSE = False  # Enable verbose logs (recommended: False in production)
```

---

## 🔧 Technical Details

### CPU Normalization

CPU usage is displayed as 0-100% for intuitive reading:

```python
# psutil returns average across all cores
cpu_pct = psutil.cpu_percent()  # Already normalized 0-100%
```

### Memory Optimizations

- **Reduced history**: 30 points instead of 60 (-50% memory)
- **Disk/battery caching**: Updated every 5s instead of 1s
- **Conditional UI updates**: Only update if change > 0.5%

### Temperature Compatibility

Temperature monitoring availability varies by platform:
- ✅ **Linux**: Fully supported (coretemp, k10temp, cpu_thermal)
- ✅ **macOS**: Supported via `osx-cpu-temp` (requires installation)
- ⚠️ **Windows**: Variable support depending on hardware

**macOS Setup**:
```bash
brew install osx-cpu-temp
```

The application automatically detects available temperature sensors and adapts the UI accordingly. If no sensors are available, the temperature card is hidden.

---

## 📊 Data Export

### JSON Format

```json
{
  "timestamp": "2025-12-22T15:03:44",
  "metrics": {
    "cpu": {
      "percent": 75.8,
      "count": 2,
      "freq_mhz": 2400,
      "temp_celsius": null,
      "history": [...]
    },
    "memory": {...},
    "network": {...}
  }
}
```

### CSV Format

```csv
Timestamp,2025-12-22T15:03:44

CPU Metrics
Usage %,Cores,Frequency MHz,Temperature °C
75.8,2,2400,N/A

Memory Metrics
Usage %,Used GB,Total GB,Available GB
74.0,4.4,8.0,3.6
...
```

---

## 🐛 Troubleshooting

### Application Won't Start

```bash
# Ensure virtual environment is activated
source env/bin/activate

# Reinstall dependencies
pip install --upgrade flet psutil
```

### Temperature Shows "--"

This is normal on macOS. Temperature sensors are not available via psutil on macOS.

### Multiple Flet Windows Open

1. Close all windows
2. Press `Ctrl+C` in all terminals
3. Relaunch **once**: `python main.py`

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/axel-g-dev/Taskly.git
cd Taskly
python3 -m venv env
source env/bin/activate
pip install flet psutil
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[Flet](https://flet.dev/)** - Modern UI framework for Python
- **[psutil](https://github.com/giampaolo/psutil)** - Cross-platform system monitoring library
- **Apple** - Design inspiration

---

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/axel-g-dev/Taskly/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/axel-g-dev/Taskly/discussions)
- 📧 **Email**: [Contact](mailto:your-email@example.com)

---

## 🗺️ Roadmap

- [ ] Multi-language support (French, Spanish, German)
- [ ] Custom themes and color schemes
- [ ] Process termination capability
- [ ] Historical data persistence
- [ ] System tray integration
- [ ] Web dashboard version
- [ ] Docker container support

---

<div align="center">

**Made with ❤️ and Python**

[⬆ Back to top](#taskly-)

</div>
