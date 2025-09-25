
FROM python:3.9


WORKDIR /app


COPY requirements.txt /app/


RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Create data directory
RUN mkdir -p /app/data


CMD ["python", "DemandData.py"]