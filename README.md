# Kangkong Edge AI Monitoring System

A Raspberry Pi-based monitoring application for kangkong (*Ipomoea aquatica*, or water spinach). The system captures plant images, acquires soil-moisture and soil-pH sensor readings, validates and preprocesses inputs, classifies visible vegetation using an edge-friendly HSV baseline, evaluates the result, and stores monitoring records locally.

The system is designed for edge operation without requiring a cloud connection. A local Flask dashboard displays the latest monitoring results, plant image, sensor readings, and inference information.

> **Current model limitation:** The HSV classifier is an experimental baseline for screening visible canopy color patterns. It has not been validated as an accurate nitrogen-deficiency detector and should not be treated as an agronomic diagnosis.

## Current capabilities

- Raspberry Pi CSI camera capture through Picamera2 and the OV5647 camera.
- ADS1115 analog-to-digital conversion for soil-moisture and soil-pH sensor signals.
- pH calibration using the configured calibration equation.
- Mock hardware for development and automated testing.
- Image validation and OpenCV preprocessing.
- Green/yellow canopy classification using an HSV color baseline.
- `Unknown` classification when visible vegetation is insufficient.
- Confidence-based decision and alert evaluation.
- Timestamped JSON monitoring results.
- SQLite monitoring history.
- Latest-result JSON output for local consumers.
- Append-only JSON Lines alert outbox with cooldown protection.
- One-shot and continuous monitoring operation.
- Flask web dashboard with automatic refresh.
- Local dashboard access from the Raspberry Pi or another device on the same network.
- Typed domain models, service contracts, hardware abstraction, and automated tests.

## Dashboard

The Flask dashboard provides a local interface for inspecting monitoring results.

It displays:

- **Plant Health Status:** The result of the decision engine and its explanation.
- **Model Inference:** Prediction, confidence, model version, and inference timestamp.
- **Plant Image:** The latest processed plant image and its dimensions.
- **Sensor Readings:** Raw soil-moisture voltage and calibrated soil pH.
- **Connection Status:** Whether the dashboard can retrieve the latest monitoring result.
- **Last Updated:** The timestamp of the latest completed monitoring cycle.

The dashboard does not display temperature or humidity because the current prototype does not have sensors for those measurements.

### Starting the dashboard

Activate the Raspberry Pi project's virtual environment and start Flask:

```bash
cd ~/kangkong-edge-ai
source .venv/bin/activate
python -m flask --app "app.web:create_app" run --host 0.0.0.0 --port 5000
```

Keep the terminal running while using the dashboard.

Open the dashboard in a browser on the Raspberry Pi:

```text
http://127.0.0.1:5000/
```

To access it from another device connected to the same local network, use the Raspberry Pi's current IP address:

```text
http://<RASPBERRY_PI_IP>:5000/
```

For example, if the Pi's current IP address is `192.168.1.76`:

```text
http://192.168.1.76:5000/
```

The IP address may change depending on the network configuration. The dashboard is intended for local development and monitoring, not direct exposure to the public internet.

## Monitoring workflow

A monitoring cycle follows this sequence:

```text
Camera Capture + Sensor Acquisition
                 |
                 v
          Input Validation
                 |
        +--------+--------+
        |                 |
      Invalid            Valid
        |                 |
        v                 v
   Log and Stop     Image Preprocessing
                          |
                          v
                     HSV Inference
                          |
                          v
                    Decision Engine
                          |
                          v
                  Monitoring Result
                          |
             +------------+------------+
             |            |            |
             v            v            v
          JSON/SQLite  Dashboard   Alert Outbox
```

The `MonitoringManager` coordinates the workflow. Individual services handle camera acquisition, sensor readings, validation, preprocessing, inference, decision evaluation, storage, dashboard updates, and alert checks.

## Model and inference limitations

The current classifier is an HSV color-based baseline. It analyzes green and yellow vegetation pixels to produce a screening result.

- Images with insufficient visible vegetation can return `Unknown`.
- A high yellow-pixel proportion can trigger a possible nitrogen-deficiency classification, depending on the configured thresholds.
- The reported confidence is a baseline model output, not a validated measure of nitrogen-deficiency detection accuracy.
- Yellowing can have causes other than nitrogen deficiency.
- The configured `models/tflite/model.tflite` path is reserved for future model integration.

A trained and evaluated agricultural image-classification model is a future development objective. Results should be interpreted alongside sensor history and physical plant inspection.

## Requirements

### Development environment

- Python 3.10 or newer.
- Git.
- A virtual environment.
- Dependencies listed in `requirements.txt`.

### Raspberry Pi deployment

- Raspberry Pi running a compatible Raspberry Pi OS.
- Raspberry Pi CSI camera, currently the OV5647.
- Picamera2 installed through Raspberry Pi OS packages.
- ADS1115 ADC connected over I2C.
- Soil-moisture and soil-pH sensor circuits compatible with the ADC input limits.
- Python dependencies listed in `requirements-raspberry-pi.txt`.

## Development setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

### Run one monitoring cycle with mock hardware

```bash
KANGKONG_HARDWARE=mock python main.py
```

### Run continuous monitoring

```bash
KANGKONG_HARDWARE=mock python main.py --continuous
```

The monitoring interval is configured in `app/config/settings.py`.

Stop continuous operation with `Ctrl+C`.

### Start the dashboard during development

```bash
python -m flask --app "app.web:create_app" run --host 127.0.0.1 --port 5000
```

Then open:

```text
http://127.0.0.1:5000/
```

The loopback address is suitable for accessing the dashboard from the same computer. Use `0.0.0.0` only when you need access from other devices on your local network.

## Raspberry Pi setup

Install the system packages required for camera access and virtual environments:

```bash
sudo apt update
sudo apt install -y python3-picamera2 python3-venv
```

Create a virtual environment that can access the system-installed Picamera2 package:

```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-raspberry-pi.txt
```

Enable the camera and I2C interfaces in Raspberry Pi configuration as required by your hardware setup.

The current ADS1115 channel mapping is:

| ADC channel | Sensor |
|---|---|
| A0 / P0 | Soil moisture |
| A1 / P1 | Soil pH |

Confirm the sensor signal conditioning, common ground, and ADC input voltage limits before connecting or changing hardware wiring.

Run one monitoring cycle:

```bash
KANGKONG_HARDWARE=raspberry_pi python main.py
```

Run continuous monitoring:

```bash
KANGKONG_HARDWARE=raspberry_pi python main.py --continuous
```

Start the local dashboard in a separate terminal:

```bash
cd ~/kangkong-edge-ai
source .venv/bin/activate
python -m flask --app "app.web:create_app" run --host 0.0.0.0 --port 5000
```

The `KANGKONG_HARDWARE` setting accepts:

| Value | Behavior |
|---|---|
| `mock` | Always use development hardware |
| `raspberry_pi` | Use Picamera2 and ADS1115 hardware implementations |
| `auto` | Select Raspberry Pi hardware on supported ARM Linux systems and mocks elsewhere |

The default setting is `auto`.

## Sensor readings and calibration

### Soil moisture

The current implementation reports the soil-moisture sensor's raw voltage. It does not currently report a calibrated absolute soil-moisture percentage.

The existing characterization supports relative interpretation of the sensor signal: higher moisture corresponds to lower output voltage in the tested setup. Thresholds should be interpreted according to the actual sensor, soil, and installation conditions.

### Soil pH

The configured calibration equation is:

```text
calibrated pH = 1.958 × sensor voltage + 2.843
```

The equation was derived from the project's buffer-solution calibration procedure. Its suitability should be assessed against the sensor's calibration records and subsequent measurements.

The displayed pH value is a calibrated estimate derived from the measured voltage; it is not a direct digital measurement of pH by the ADC.

## Generated data

Runtime files are created automatically as the monitoring pipeline runs.

| Path | Purpose |
|---|---|
| `datasets/raw/` | Original camera captures |
| `datasets/processed/` | Preprocessed images used for inference |
| `datasets/results/YYYYMMDD_HHMMSS.json` | Individual monitoring-cycle records |
| `datasets/results/latest.json` | Latest dashboard-ready monitoring result |
| `datasets/results/alerts.jsonl` | Local alert delivery outbox |
| `database/monitoring.db` | SQLite monitoring history |
| `logs/application.log` | Application log |

The SQLite table is named `monitoring_results`. It stores monitoring history, including timestamps, sensor readings, prediction, confidence, decision, and image/result paths.

Generated images, monitoring records, databases, and logs are runtime data rather than source-code artifacts. Their inclusion in version control is controlled by the repository's `.gitignore` rules.

## Configuration

Central configuration is maintained in `app/config/settings.py`.

| Setting | Current configured default |
|---|---:|
| Monitoring interval | 60 minutes |
| Image dimensions | 640 × 480 |
| Inference confidence threshold | 0.80 |
| Nitrogen-deficiency alert threshold | 0.80 |
| Alert cooldown | 30 minutes |

These values are configuration defaults, not guarantees of model accuracy or agronomic validity.

## Testing

Run the automated test suite:

```bash
python -m pytest -q
```

The suite covers application composition, domain models, settings, hardware selection, mock capture, monitoring-cycle execution, and alert decisions.

Before committing changes, also run:

```bash
git diff --check
git status
```

## Project structure

```text
app/
├── config/       Application settings
├── contracts/    Service interfaces
├── core/         Application lifecycle and workflow orchestration
├── domain/       Monitoring data models
├── hardware/     Mock and Raspberry Pi hardware adapters
├── services/     Capture, validation, inference, decisions, and outputs
├── utils/        Shared utilities
└── web/          Flask application, routes, templates, and static assets

tests/            Automated tests
datasets/         Captured, processed, and generated monitoring data
database/         SQLite monitoring history
models/           Model artifacts and future model integration
main.py           Application entry point
```

## Operational notes

- The application runs locally and does not require a cloud backend for its core monitoring workflow.
- The dashboard reads the latest monitoring result and refreshes automatically.
- A new monitoring cycle must run to generate fresh sensor readings and a new captured image.
- The dashboard's reported connection status indicates whether its latest-result API request succeeds; it does not independently verify every hardware component.
- The current classifier is a screening baseline, not a confirmed nitrogen-deficiency diagnosis.
- Alert records are written to a local outbox. An SMS, email, or messaging provider could consume `alerts.jsonl` in a future integration.
- Use a service manager such as `systemd` for reliable continuous operation after reboots or process failures.
- Do not expose the Flask development server directly to the public internet.

## License

See [LICENSE](LICENSE).
