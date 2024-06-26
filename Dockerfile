FROM python:3.8-slim
RUN mkdir /app
WORKDIR app
ADD .. /app/
RUN ls -lrt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 4000
CMD ["streamlit", "run", "/app/src/main.py"]