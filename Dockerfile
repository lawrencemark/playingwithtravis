
FROM python:3.9 as base


#EXPOSE NETWORK PORTS TO LOCAL HOST
EXPOSE 5000


#FLASK INSTALL AND ENVIRONMENT VARIABLES
ENV FLASK_APP=/srv/www/todo_app/app.py 
ENV FLASK_ENV=development
ENV PATH="/root/.poetry/bin/:/srv/www/.venv/bin:/srv/www/todo_app:${PATH}" 



#PULL THE LATEST POETRY SCRIPT AND INSTALL
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python




FROM base AS production
#PRODUCTION RELEASE WITH MINIMAL CONFIGURATION
RUN mkdir /srv/www
WORKDIR /srv/www
COPY ./poetry.toml .
COPY ./pyproject.toml .
COPY ./scripts ./scripts
COPY ./todo_app ./todo_app
#RUNNER SCRIPT
ENV APPLICATIONTYPE=PRODUCTION
WORKDIR /srv/www/
RUN poetry install
ENTRYPOINT [ "/srv/www/scripts/setupenv.sh" ]


FROM base as development
#LOCAL DEVELEOPMENT RELEASE WITH SIMPLE WERKZEUG(TOOL) WEBSERVER
RUN apt-get update && apt-get install -qqy nano
#RUNNER SCRIPT
ENV APPLICATIONTYPE=DEVELOPMENT
WORKDIR /srv/www/
ENTRYPOINT [ "/srv/www/scripts/setupenv.sh" ]



FROM base AS test
WORKDIR /tmp
COPY ./requirements.txt .
RUN pip install -r requirements.txt
#INSTALL CHROME AND DRIVER - SPECIFIC VERSION SET TO 93.0.4577.15
RUN apt-get update && apt-get install git 
RUN apt-get update -qqy && apt-get install -qqy wget gnupg unzip
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
&& echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -qqy \
  && apt-get -qqy install google-chrome-stable \
  && rm /etc/apt/sources.list.d/google-chrome.list \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
RUN  wget --no-verbose -O /tmp/chromedriver_linux64.zip "https://chromedriver.storage.googleapis.com/93.0.4577.15/chromedriver_linux64.zip" \
&& unzip /tmp/chromedriver_linux64.zip -d /usr/bin \
  && rm /tmp/chromedriver_linux64.zip \
  && chmod 755 /usr/bin/chromedriver
RUN poetry config virtualenvs.create false
#RUNNER SCRIPT
ENV APPLICATIONTYPE=TRAVISCI
WORKDIR /srv/www/
ENTRYPOINT [ "/srv/www/scripts/setupenv.sh" ]



