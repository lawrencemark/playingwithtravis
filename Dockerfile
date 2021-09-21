
FROM python:3.9 as base

EXPOSE 5000
WORKDIR /tmp
COPY ./requirements.txt .
RUN pip install -r requirements.txt

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
WORKDIR /srv/www/todo_app
ENTRYPOINT ["/srv/www/todo_app/flaskrun.sh"]
