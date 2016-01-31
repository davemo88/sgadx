FROM buildpack-deps:jessie

# remove several traces of debian python
RUN apt-get purge -y python.*

# RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62
# RUN echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list

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
ADD run.py ./
ADD db ./db/