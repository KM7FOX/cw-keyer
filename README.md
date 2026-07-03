# cw-keyer

A Python library for sending, receiving, and eventually teaching Morse code (CW).

This project began as software to key a transmitter from a Raspberry Pi, but is evolving into a reusable library for Morse encoding, decoding, GPIO interfacing, and AI-assisted CW training.

## Current Features

- Morse code encoder
- Configurable timing model (WPM)
- GPIO straight key interface for Raspberry Pi
- Modular package architecture
- Installable as a Python package

## Planned Features

- Morse decoder
- Sidetone generation
- LED output
- Adaptive CW trainer
- AI conversational practice partner
- Character and timing statistics
- Farnsworth timing
- Koch training
- Headless and GUI front ends

## Installation

Clone the repository:

```bash
git clone https://github.com/KM7FOX/cw-keyer.git
cd cw-keyer
```

Create a virtual environment:

```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
```

Install the package in editable mode:

```bash
pip install -e .
```

On Raspberry Pi OS, install the GPIO dependencies:

```bash
sudo apt install python3-gpiozero python3-lgpio
```

## Example

```python
from km7fox_cw.encoder.straight_key import Keyer

keyer = Keyer(wpm=12)
keyer.send("CQ CQ CQ DE KM7FOX K")
```

## Project Goals

This project is intended to become a clean, reusable Morse code library rather than a single application.

The encoder, decoder, timing model, and hardware interfaces are designed as independent components that can be reused by applications including:

- command-line tools
- Raspberry Pi hardware projects
- graphical training applications
- AI-based CW tutors
- automated testing

## Status

Early development.

The architecture is still evolving and APIs may change between releases.

## Contributing

Ideas, bug reports, and pull requests are welcome.

## License

MIT License