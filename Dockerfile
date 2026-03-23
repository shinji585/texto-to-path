FROM python:3.11-slim

WORKDIR /app

# copy the code and create the necesary paths 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# create the path 
RUN mkdir -p schemas output cache

# command base 
ENTRYPOINT [ "python", "main.py" ]

