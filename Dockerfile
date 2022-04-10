FROM debian:stretch-slim

# ============================================
# Install required packages
# ============================================
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
apt-get upgrade -y && \
apt-get install -y \
 wget curl \
    nano \
zlib1g-dev \
zlib1g \
netcat \
build-essential \
libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev \
liblzma-dev libxcb-xinerama0 libffi-dev \
--no-install-recommends && \
rm -rf /var/lib/apt/lists/*

# ============================================
# Download and compile python 3.9.1
# ============================================
RUN wget --no-check-certificate https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tgz && \
tar xvf Python-3.9.1.tgz && \
cd Python-3.9.1 && \
./configure --enable-optimizations && \
make install && \
cd / && rm -Rf Python-3.9.1*



# ============================================
# Install correct version of pip, dont use apt!
# ============================================
RUN curl -k https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
$(which python3) get-pip.py && $(which pip3) install --upgrade pip