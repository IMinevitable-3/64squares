FROM ubuntu:latest
RUN echo 'APT::Install-Suggests "0";' >> /etc/apt/apt.conf.d/00-docker
RUN echo 'APT::Install-Recommends "0";' >> /etc/apt/apt.conf.d/00-docker
RUN apt-get update \
  && apt-get install -y python3 python3-pip python3.10-dev --no-install-recommends \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
  && apt-get install -y libpq-dev --no-install-recommends \
  && rm -rf /var/lib/apt/lists/*
RUN apt-get update \
  && apt-get install -y build-essential \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN pip install --upgrade pip 
RUN pip install --upgrade setuptools
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000

CMD ["sh", "-c", "chmod +x wait_dude.sh && ./wait_dude.sh"]
