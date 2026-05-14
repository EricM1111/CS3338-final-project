CS 3338 Final Project - Group 4 - Scientific Forgery Image Detection System
Jira Project URL:
[https://calstatela-cs3338-spr25.atlassian.net/jira/your-work](https://cs3337-group-11.atlassian.net/jira/software/projects/IFD/boards/167)
Team
Janelle Rivera
Eric Marroquin
Alexis Flores
Alex Lam
Overview
The Scientific Forgery Image Detection System is a web-based application that detects copy-move forgery in biomedical and scientific images. The system allows users to upload images and receive analysis results identifying possible duplicated regions in scientific figures.
The system comprises:

A Web Application (Frontend)
A Backend API Server
A Detection System (Planned)

System Architecture
The application follows this general workflow:

Users upload biomedical images through the web interface
Frontend sends image to backend API
Backend receives and processes the image
Detection system analyzes image (future implementation)
Backend returns results to frontend
User views results in the web interface

Features
Web Application (Frontend):

Image upload interface
Image preview
Submit button for analysis
Results display section

Backend System:

REST API for image upload
Image handling and validation
JSON responses
Communication with detection module

Detection System (Planned):

Copy-move forgery detection
Identification of duplicated regions
Image region comparison
Pixel-level analysis

Technologies Used
Frontend: HTML
Backend: Python, FastAPI, Uvicorn
Planned Libraries: OpenCV, NumPy, Pillow, PyTorch
