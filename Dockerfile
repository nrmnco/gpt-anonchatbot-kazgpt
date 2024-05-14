FROM python:latest
ENV TZ=UTC
COPY . .
WORKDIR .
RUN pip3 install -r requirements.txt
EXPOSE 80
CMD ["python", "./__main__.py"]
