FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /app

COPY . .

RUN pip install playwright pytest pytest-html python-dotenv faker

CMD ["pytest", "-m", "smoke", "-v", "--html=reports/report.html", "--self-contained-html"]