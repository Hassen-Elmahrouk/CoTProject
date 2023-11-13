FROM python:3.10

# Set the working directory in the container to /app
WORKDIR /app

# Install necessary OS packages
RUN apt-get update && \
    apt-get install -y \
    git \
    libgl1-mesa-glx  # Added this line for libGL

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install detectron2 from GitHub
RUN pip install 'git+https://github.com/facebookresearch/detectron2.git'

# Copy the current directory contents into the container at /app
COPY . /app

# Define environment variable for Azure Storage Connection String
# Warning: For production, use a more secure way of handling sensitive data like this
ENV AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=berryscan;AccountKey=QkISzI7rKPcUQoWhsTGlBgcqErzbTPKsZ3FOiww/6Gtm8mBVoOVyjlvMcHn9o1D+cpt7XAawXYi0+AStTXC5dg==;EndpointSuffix=core.windows.net"

# Run train_model.py when the container launches
CMD ["python", "./train_model.py"]