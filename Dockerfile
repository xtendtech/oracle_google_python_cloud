FROM  python:3.13:slim
WORKDIR /app
COPY . ./app
RUN pip install  flask psutil
EXPOSE 5000
CMD [ "python" "main.py"]
# docker build -t flask-monitor .
# docker run -p 5000:5000 flask-monitor