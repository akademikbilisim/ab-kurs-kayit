FROM python:2.7

# Install requirements
COPY requirements.txt /tmp
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		python-dev \
		gcc \
		libpng-dev \
		libjpeg-dev \
		libpq-dev \
	&& rm -rf /var/lib/apt/lists/* \
	&& pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /usr/src/app

CMD [ "python", "manage.py", "runserver" ]

