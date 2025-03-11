#Python base image
FROM python:3.11.8

#env variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

#SET DIR AS WORKING DIR
WORKDIR /app

COPY requirements.txt /app

#dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat-traditional
RUN apt-get install net-tools
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#entrypoint
COPY ./Karpackie_Kwatery_Locator/entrypoint.sh .
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

#copy project
COPY . .

#run entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]


#expose not necessary here (good practice)
EXPOSE 8000

# CMD ["gunicorn", "--config", "gunicorn_config.py", "GLSR_Gym.wsgi:application"]

