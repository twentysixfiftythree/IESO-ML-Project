FROM python:3.9
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN mkdir -p /app/data

ENTRYPOINT ["python"]
# i change this to whichever im scraping
CMD ["scripts/PriceData.py"]