# Kangkong Edge AI Monitoring System

A Raspberry Pi-oriented monitoring application for observing kangkong (water
spinach) using a camera, soil-moisture sensor, and pH sensor. It captures an
image and sensor readings, validates and preprocesses them, classifies the
visible plant canopy, makes an alert decision, and stores the complete result
locally. The system is designed to keep working at the edge without a cloud
connection.

## Current capabilities

- Raspberry Pi CSI camera capture through Picamera2
- ADS1115 soil-moisture and pH voltage acquisition
- pH calibration
- Mock camera and sensors for development on macOS, Windows, and x86 Linux
- Image validation and OpenCV preprocessing
- Explainable green/yellow canopy classification
- Nitrogen-deficiency alert decisions with confidence thresholds
- Timestamped JSON results and a searchable SQLite history
- `latest.json` output for a dashboard or other local consumer
- Append-only JSON Lines alert outbox with cooldown protection
- One-shot and continuous scheduled operation
- Typed domain models, service contracts, and automated tests

## How a monitoring cycle works

```text
Camera + sensors
       |
       v
    Validate ---- invalid input --> log and stop cycle
       |
       v
Resize image -> classify canopy -> decide -> store JSON + SQLite
                                      |              |
                                      v              v
                                 alert outbox    latest.json
```

The included classifier is an edge-friendly HSV colour baseline. It measures
green and yellow vegetation pixels, reports images with too little vegetation
as `Unknown`, and flags a high yellow share as a possible nitrogen deficiency.
It is functional and explainable, but it is not a substitute for a validated
trained agricultural model. The configured `models/tflite/model.tflite` path is
reserved for a future model integration.

## Requirements

- Python 3.10 or newer
- A virtual environment is recommended
- For Raspberry Pi operation: Raspberry Pi OS, a supported CSI camera,
  Picamera2, and an ADS1115 connected over I2C

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\\Scripts\\activate`.

Run one monitoring cycle with mock hardware:

```bash
KANGKONG_HARDWARE=mock python main.py
```

Run continuously at the interval configured in `app/config/settings.py`:

```bash
KANGKONG_HARDWARE=mock python main.py --continuous
```

Stop continuous operation with `Ctrl+C`.

## Raspberry Pi setup

Install Picamera2 using Raspberry Pi OS packages, then install the Python
dependencies:

```bash
sudo apt update
sudo apt install -y python3-picamera2 python3-venv
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
python -m pip install -r requirements-raspberry-pi.txt
```

Enable the camera and I2C interfaces in Raspberry Pi configuration. Connect
the soil-moisture signal to ADS1115 channel P0 and the pH signal to P1. Then
run:

```bash
KANGKONG_HARDWARE=raspberry_pi python main.py
```

`KANGKONG_HARDWARE` accepts:

- `mock` — always use development hardware
- `raspberry_pi` — always use Picamera2 and ADS1115
- `auto` — default; use Raspberry Pi hardware on ARM Linux and mocks elsewhere

## Generated data

Runtime files are created automatically:

| Path | Purpose |
| --- | --- |
| `datasets/raw/` | Original camera captures |
| `datasets/processed/` | Resized images used for classification |
| `datasets/results/YYYYMMDD_HHMMSS.json` | Complete cycle records |
| `datasets/results/latest.json` | Latest dashboard-ready record |
| `datasets/results/alerts.jsonl` | Alert delivery outbox |
| `database/monitoring.db` | SQLite monitoring history |
| `logs/application.log` | Application log |

The SQLite table is named `monitoring_results` and contains timestamps, sensor
values, prediction, confidence, decision, and paths to the image and JSON
record.

## Configuration

Central configuration lives in `app/config/settings.py`. Important defaults
include:

| Setting | Default |
| --- | ---: |
| Monitoring interval | 60 minutes |
| Image size | 640 × 480 |
| Inference confidence threshold | 0.80 |
| Nitrogen-deficiency alert threshold | 0.80 |
| Alert cooldown | 30 minutes |

The current pH calibration is:

```text
calibrated pH = 1.958 × sensor voltage + 2.843
```

Calibrate this equation and the moisture interpretation against the actual
sensors and growing medium before relying on the measurements.

## Testing

```bash
python -m pytest -q
```

The tests cover application composition, domain models, settings, hardware
selection, mock capture, monitoring-cycle execution, and alert decisions.

## Project structure

```text
app/core/          lifecycle, scheduling, and workflow orchestration
app/services/      capture, validation, inference, decisions, and outputs
app/hardware/      mock and Raspberry Pi hardware adapters
app/contracts/     interfaces between application layers
app/domain/        immutable monitoring data models
app/config/        application settings
tests/             automated tests
datasets/          captured, processed, and generated monitoring data
models/            reserved model artifacts
```

## Operational notes

- The software can indicate a possible deficiency; it does not provide an
  agronomic diagnosis. Confirm alerts with sensor history and physical review.
- Alert entries are written to a local outbox. An SMS, email, or messaging
  provider can consume `alerts.jsonl` without changing the monitoring pipeline.
- `latest.json` is a presentation-neutral dashboard feed rather than a hosted
  web interface.
- Use a service manager such as systemd to restart continuous operation after
  crashes or reboots in a deployment.

## License

See [LICENSE](LICENSE).
