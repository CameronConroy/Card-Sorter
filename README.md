# Card-Sorter

## Purpose

Card-Sorter is a hardware and software project for automatically identifying, organizing, randomizing, and sorting standard playing cards.

The system is designed around a face-up deck that is scanned by a camera. Card identity will be determined using OpenCV, then each card will be physically redirected into a rotating carousel of sorting buckets.

The sorter will use a bucket-sort-based process with a dedicated arbitration bucket for temporary card storage and reprocessing.

## Current Design

### Carousel

The current carousel design contains 8 buckets:

- 7 active sorting buckets
- 1 arbitration bucket

Each active bucket may hold multiple cards during the sorting process.

The arbitration bucket is used when a card cannot immediately be placed into its final sorting path and needs to be temporarily stored before another sorting pass.

## Software

The control software is written in Python.

The current web interface is built with NiceGUI and includes:

- Full deck display
- Drag-and-drop card ordering
- Manual deck organization
- Randomize function
- Randomize hidden function
- Card face visibility toggle
- Reset deck order
- Submit deck order
- API endpoint for retrieving the submitted deck

## Planned Card Detection

Cards will be presented face-up and scanned using a camera.

OpenCV will be used to identify the card before it enters the sorting mechanism.

The planned processing flow is:

```text
Deck

Card feed

Camera

OpenCV identification

Card routing mechanism

Carousel

Sorting bucket
```

## Planned Sorting Flow

The software will maintain the target deck order and determine which carousel bucket each scanned card should enter.

Cards will be distributed across the available buckets, then processed through additional passes as necessary until the requested deck order is reached.

The arbitration bucket will provide temporary storage when the normal bucket allocation cannot immediately resolve the next sorting step.

## Web Interface

The web interface acts as the primary method for defining the requested deck state.

Users can manually arrange cards through drag-and-drop or generate an order using built-in functions.

The submitted order will eventually be used by the physical sorter as the target output order.

## Project Components

Current and planned components include:

- Python
- NiceGUI
- OpenCV
- Camera
- Raspberry Pi
- Carousel
- DC motor
- Servos
- Solenoid
- Gear system
- Card feed mechanism
- Sorting buckets

## Status

Currently implemented:

- Deck representation
- Web interface
- Drag-and-drop organization
- Randomization
- Hidden-card randomization
- Deck reset
- Submitted deck API
- OpenCV card recognition
- Camera integration

In development:

- Sort algorithm
- Carousel control
- Card feed mechanism
- Motor and servo control
- Arbitration logic
- Physical sorter integration
