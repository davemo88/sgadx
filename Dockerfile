FROM buildpack-deps:jessie

# remove several traces of debian python
RUN apt-get purge -y python.*

RUN apt-get update \
    && apt-get install -y python-scipy \
                          python-pandas \
                          ipython \
                          git \
                          vim \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN curl -SL 'https://bootstrap.pypa.io/get-pip.py' | python2 && \
    pip install --no-cache-dir --upgrade pip

ADD requirements.txt ./

RUN pip install --no-cache-dir -r ./requirements.txt \
  && rm ./requirements.txt

ADD config.sample.py ./config.py
ADD sgadx ./sgadx/
ADD tests ./tests/
