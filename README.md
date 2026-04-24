# AI Fitness Trainer

## Overview

AI Fitness Trainer is a real-time exercise monitoring system that uses computer vision to track body movements and count repetitions of exercises such as squats and push-ups. The system uses a webcam feed, processes human pose landmarks, and provides live feedback through a web interface.


## Features

* Real-time webcam-based pose detection
* Automatic repetition counting
* Support for squats and push-ups
* Live display of exercise status, stage, and elapsed time
* Angle calculation for movement accuracy
* Web-based interface using Flask


## Technologies Used

* Python
* OpenCV
* MediaPipe
* NumPy
* Flask
* HTML, CSS, JavaScript


## Project Structure

AI-Fitness-Trainer/
│
├── app.py              # Flask backend application
├── fitness.py          # Pose detection and exercise logic
├── templates/
│   └── index.html      # Frontend interface
├── README.md



## Installation

### 1. Clone the Repository

git clone https://github.com/jiyathakker23-hub/AI-Fitness-Trainer.git
cd AI-Fitness-Trainer

### 2. Install Dependencies

pip install opencv-python mediapipe numpy flask

### 3. Run the Application

python app.py

### 4. Access the Application

Open a browser and go to:
http://127.0.0.1:5000/



## How It Works

The system uses MediaPipe Pose to detect key body landmarks from the webcam feed. Based on these landmarks:

* Joint angles are calculated using trigonometric functions
* Exercise stages (UP and DOWN) are identified
* A repetition is counted when a complete movement cycle is detected
* Processed video frames are streamed to the browser using Flask

For push-ups, elbow angles are used to detect motion.
For squats, knee and hip angles are analyzed to ensure proper form.



## Supported Exercises

* Squats
* Push-ups



## Usage Instructions

* Stand sideways to the camera for better detection
* Ensure your full body is visible
* Perform exercises in a slow and controlled manner
* Click the appropriate exercise button to start
* Click stop to end the session



## Limitations

* Works best with a clear background and good lighting
* Accuracy may decrease if body parts are not fully visible
* Currently supports only two exercises



## Future Improvements

* Add more exercises such as lunges and planks
* Improve accuracy using advanced models
* Add calorie estimation
* Store workout history
* Add user authentication



## License

This project is developed for educational purposes and does not include a specific license.



## Acknowledgements

* MediaPipe for pose detection
* OpenCV for video processing
