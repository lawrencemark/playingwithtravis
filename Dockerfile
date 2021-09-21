
FROM python:3.9 as base

EXPOSE 5000

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN mkdir /srv/www
WORKDIR /srv/www/
ENV PATH="/root/.poetry/bin/:/srv/www/.venv/bin:/srv/www/todo_app:${PATH}"
COPY ./poetry.toml .
COPY ./pyproject.toml .
RUN ~/.poetry/bin/poetry install
#CI pipeline and Travis build - using clone with inside the build
RUN apt-get update && apt-get install git && apt-get install nano
RUN apt-get update -qqy && apt-get install -qqy wget gnupg unzip
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
&& echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -qqy \
  && apt-get -qqy install google-chrome-stable \
  && rm /etc/apt/sources.list.d/google-chrome.list \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
# Install Chrome WebDriver
RUN  wget --no-verbose -O /tmp/chromedriver_linux64.zip "https://chromedriver.storage.googleapis.com/93.0.4577.15/chromedriver_linux64.zip" \
&& unzip /tmp/chromedriver_linux64.zip -d /usr/bin \
  && rm /tmp/chromedriver_linux64.zip \
  && chmod 755 /usr/bin/chromedriver
WORKDIR /tmp
RUN git clone --branch module7 https://github.com/lawrencemark/DevOps-Course-Starter
RUN cp -R /tmp/DevOps-Course-Starter/* /srv/www
COPY ./requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /srv/www/todo_app
ENTRYPOINT ["./flaskrun.sh"]
