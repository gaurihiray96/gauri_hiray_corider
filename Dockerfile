
FROM alpine



RUN apk add --no-cache python3-dev && pip3 install --upgrade pip


WORKDIR /app


COPY /requirements.txt /app

RUN pip3 install -r requirements.txt

COPY ["api.py", "/app"]

EXPOSE 5001



ENTRYPOINT [ "python3" ]

CMD ["api.py"]


