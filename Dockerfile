FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /hacknu

# Install required system dependencies
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev
RUN apk add --no-cache build-base libffi-dev
RUN apk add --no-cache ffmpeg

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8080

# Start Gunicorn
CMD ["uvicorn", "hacknu.asgi:application", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]