<h1 align="center">
  <br>
	BerryScan
</h1>
<h3 align="center">
  Revolutionary Cloud of Things Application for Strawberry Farming</br>
  Monitor your crops efficiently and smartly 🍓
</h3>
<div align="center">
  <h4>
    <a href="#Overview">Overview</a> |
    <a href="#Live-Demo">Live Demo</a> |
    <a href="#Installation-Guide">Installation Guide</a> |
    <a href="#Technologies">Technologies</a> |
    <a href="#Features">Features</a> |
    <a href="#Resources">Resources</a> |
  </h4>
</div>
<br>

## Overview
BerryScan is a cutting-edge application that integrates cloud of things technology to revolutionize strawberry farming. By utilizing a robotic system equipped with GPS and camera, BerryScan explores your farm, captures images, and sends them to the cloud. Our advanced algorithms then process these images to detect diseases, providing you with detailed insights about the health of your crops and their precise location on your farm.

Key Goals of BerryScan:
- Efficient monitoring and disease detection in strawberry crops.
- Precise GPS-based mapping of disease locations for targeted treatment.
- User-friendly interface to access and interpret farm data.

Achievements:
- Developed a fully functional prototype for automated farm monitoring.
- Implemented robust image processing algorithms for accurate disease detection.
- Integrated GPS technology for precise mapping and location tracking.

## Live Demo
please visit https://berryscan.tech/index.html
## Installation Guide

To deploy BerryScan, follow these steps:

1. Set up on your preferred device (compatible with major operating systems).

2. Install **MongoDB** for database management.
4. Clone the Repository: 
   `git clone https://github.com/Houssem-Ben-Salem/CoTProject.git`

5. Navigate to CoTProject/code/api  directory and run `mvn clean install` 

6. move the war file under wildfly/standalone/deployments

7. nivagate to CoTProject/code/mlops , run pip install requirements.txt then  run python3 app.py
## Technologies
BerryScan is built using a variety of technologies for robust and scalable performance:
- Backend:
  - jakarta ee 
  - flask
  - MongoDB
  - azure blob storage

- IoT and Robotics:
  - Raspberry Pi (or compatible hardware)
  - GPS Module
  - High-Resolution Camera

- Frontend:
  - React.js (Progressive Web App)

## Features
- **Disease Detection**: Utilizes AI-based image processing to detect and classify diseases in strawberries.
- **GPS Mapping**: Accurately maps the location of diseased crops for easy identification and treatment.
- **User Dashboard**: A comprehensive interface to view, analyze, and manage farm data effectively.
##Certifications and grading
We have enabled HTTPS with letsencrypt TLS certificate with HSTS enabled as well, ensuring only secure connections are allowed to the middleware. Enabling TLS1.2 only on Wildfly helps generate A+ grading on SSlabs
![certificate](https://github.com/Houssem-Ben-Salem/CoTProject/assets/94080018/b8998347-a833-4061-90e7-4fe375eba690)


## Solution Screenshots:
![screenshot](https://github.com/Houssem-Ben-Salem/CoTProject/assets/94080018/34c775f7-4adc-4ed1-9519-b73c6cd8ceea)


