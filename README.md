# Eye State Detector

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0.1-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5.3-green)
![dlib](https://img.shields.io/badge/dlib-19.22-green)

## Project Overview

The **Eye State Detector** is a web-based application designed to analyze whether a person's eyes are open or closed in a given image. The application leverages computer vision and machine learning techniques, specifically using Python libraries such as OpenCV and dlib, to provide accurate and reliable results. This tool can be applied in various fields such as driver drowsiness detection, human-computer interaction, and biometric authentication.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [System Requirements](#system-requirements)
- [Screenshots](#screenshots)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Features

- **User-Friendly Interface**: Simple and intuitive web interface for image upload and analysis.
- **Real-Time Feedback**: Provides immediate feedback on whether the eyes are open or closed in the uploaded image.
- **Robust Image Processing**: Utilizes advanced computer vision techniques for accurate detection.
- **Lightweight**: Runs on a Flask-based backend, making it easy to deploy.

## Project Structure

```bash
Eye-State-Detector/
├── static/
│   ├── css/
│   │   └── styles.css
├── templates/
│   ├── index.html
│   └── result.html
├── uploads/
│   └── # Stores uploaded images
├── app.py
├── README.md
└── requirements.txt
