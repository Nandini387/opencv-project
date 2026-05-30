# OpenCV Face Lock Demo

This project is a small face-authentication demo built with OpenCV and `face_recognition`. It has two scripts:

- `register_face.py` captures a face from your webcam and saves it as `known_face.jpg`
- `lock_screen.py` uses that saved face to detect whether the camera sees a matching person and shows a simple lock/unlock UI

It is a learning project and a prototype, not production-grade security software.

## Features

- Webcam-based face registration
- Real-time face matching from a saved reference image
- Simple lock/unlock overlay with status messages
- Automatic re-lock after a short unlock window

## Requirements

- Python 3.9 or newer
- A working webcam
- OpenCV
- face_recognition
- numpy

`face_recognition` may require extra system dependencies depending on your OS. On Windows, installation can sometimes fail if build tools or compatible wheels are missing.

## Install

Create and activate a virtual environment first if you want to keep dependencies isolated, then install the packages:

```bash
pip install opencv-python face_recognition numpy
```

If `face_recognition` installation fails, install the required system packages for `dlib` first, then retry.

## How To Use

### 1. Register your face

Run the registration script and look at the camera until your face is detected.

```bash
python register_face.py
```

When prompted, press the Space bar to save the current frame as `known_face.jpg`.

### 2. Start the lock screen demo

After registration completes, run the lock screen script:

```bash
python lock_screen.py
```

Look at the camera to unlock the screen. Press `Q` to quit.

## How It Works

1. `register_face.py` detects a face using OpenCV Haar cascades and saves the camera frame as `known_face.jpg`.
2. `lock_screen.py` loads that image, extracts a face encoding with `face_recognition`, and compares live webcam frames against it.
3. When the live face matches, the UI switches to an unlocked state for a few seconds, then locks again automatically.

## Files

- `register_face.py` - captures and saves the reference face image
- `lock_screen.py` - performs face matching and renders the lock screen UI
- `colors.csv` - included in the repository, but not used by the current scripts

## Notes

- Use a clear, front-facing photo during registration for best results.
- `known_face.jpg` is generated locally and should not be committed if you want to keep your reference image private.
- Lighting, camera quality, and angle affect recognition accuracy.
- This demo is not secure enough for real authentication or device protection.

## Troubleshooting

- If the camera does not open, check that no other app is using it.
- If face matching fails often, try re-registering your face in better lighting.
- If `face_recognition` cannot install, make sure the underlying `dlib` dependency is available for your platform.

## License

No license has been specified yet. Add one if you plan to share or reuse this project.
