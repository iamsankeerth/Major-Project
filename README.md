# Tamil Finger Spelling Recognition

This project provides a desktop application for recognizing Tamil finger spelling gestures in real time.  
It combines Mediapipe hand landmark detection with a TensorFlow LSTM classifier and wraps everything in a beginner-friendly GUI so you can translate signs straight from your webcam or play back reference clips.

## Highlights
- Real-time hand landmark detection powered by Mediapipe.
- Pre-trained LSTM model (`best_lstm_model.keras`) ready for inference out of the box.
- GUI with webcam preview, prediction overlay, history log, and utilities for browsing example signs.
- Reference image library to help users learn and verify each Tamil character.

## Prerequisites
- Windows 10/11 (other OSes work with small path changes).
- Python 3.10 (matches the supplied `venv_py310` environment).
- Webcam (USB or built-in) for live inference.
- Git (optional but recommended for cloning and version control).

## Quick Start
1. **Clone the repository**
   ```powershell
   git clone https://github.com/iamsankeerth/Major-Project.git
   cd "Major Project"
   ```
2. **Create and activate a virtual environment (Windows PowerShell)**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   > On macOS/Linux use `python3 -m venv venv` followed by `source venv/bin/activate`.
3. **Install required packages**
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. **Run the GUI**
   ```powershell
   python app.py
   ```
   The application window should appear. Load the bundled model if prompted and start the webcam feed to see live predictions.

## Dataset
The full Tamil Sign Language dataset used for training is available on Mendeley Data:  
https://data.mendeley.com/datasets/39kzs5pxmk/2

1. Download the dataset archive from the link above.
2. Extract it to a folder such as `data/raw/`.
3. Update your training scripts (or extend the GUI) to point to the extracted folder if you plan to retrain the model.

The `ReferenceImages/` directory shipped with this project contains representative frames for each gesture so the GUI can display lookup visuals even without the full dataset.

## Understanding the Application
- `app.py` - Main Tkinter GUI that manages webcam capture, Mediapipe hand tracking, preprocessing, and LSTM predictions.
- `best_lstm_model.keras` - Pre-trained model weights (skip training if you only need inference).
- `tamil_labels.json` - Maps class indices to Tamil characters and pronunciations.
- `ReferenceImages/` - Static reference images surfaced by the GUI when you browse characters.
- `tamil-sign-to-text.ipynb` - Notebook with experiments and training pipeline details.

## Deploying / Packaging Tips
- Use `python -m pip freeze > requirements-lock.txt` after testing to capture exact versions for deployment.
- To ship a ready-to-run build without Python, consider packaging with PyInstaller:
  ```powershell
  pip install pyinstaller
  pyinstaller --onefile --noconsole app.py
  ```
  (You may need to include `ReferenceImages/`, the model file, and label JSON via `--add-data`.)
- Test the packaged build on a clean machine to verify Mediapipe and TensorFlow dependencies.

## Troubleshooting
- **Webcam not detected** - Ensure another app is not using the camera; try changing the camera index in settings.
- **Mediapipe import errors** - Confirm you activated the correct virtual environment before installing requirements.
- **TensorFlow warnings about CPU instructions** - These are informational; performance may improve with a compatible GPU.
- **Predictions are blank** - Make sure your hand is inside the ROI box and well lit; adjust the detection confidence thresholds in the GUI settings if needed.

Feel free to fork the repository and extend it - ideas include adding new gestures, improving the UI, or integrating text-to-speech for recognized sequences. Pull requests and issues are welcome!
