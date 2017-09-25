# OpenVAS with automated scanscript
# Based on OpenVAS image for Docker by Mike Splain
FROM ubuntu:16.04
MAINTAINER Alwin Peppels alwin.peppels@ictu.nl
ADD bin/* /openvas/
ADD config/redis.config /etc/redis/redis.config

RUN apt-get update && \
    apt-get install software-properties-common --no-install-recommends -yq && \
    add-apt-repository ppa:mikesplain/openvas -y && \
    add-apt-repository ppa:mrazavi/openvas -y && \
    apt-get clean && \
    apt-get update && \
    apt-get install alien \
                    bzip2 \
                    curl \
                    dirb \
                    dnsutils \
                    libopenvas9-dev \
                    net-tools \
                    nikto \
                    nmap \
                    nsis \
                    openssh-client \
                    openvas9 \
                    rpm \
                    rsync \
                    sendmail \
                    smbclient \
                    sqlite3 \
                    texlive-latex-base \
                    texlive-latex-extra \
                    texlive-latex-recommended \
                    w3af \
                    wapiti \
                    wget \
                    -yq && \
    mkdir /osp && \
    cd /osp && \
        wget http://wald.intevation.org/frs/download.php/1975/openvas-smb-1.0.1.tar.gz ;\
        wget http://wald.intevation.org/frs/download.php/1999/ospd-1.0.0.tar.gz && \
        wget http://wald.intevation.org/frs/download.php/2145/ospd-1.0.1.tar.gz && \
        wget http://wald.intevation.org/frs/download.php/2177/ospd-1.0.2.tar.gz && \
        wget http://wald.intevation.org/frs/download.php/2005/ospd-ancor-1.0.0.tar.gz && \
        wget http://wald.intevation.org/frs/download.php/2097/ospd-debsecan-1.0.0.tar.gz && \
        wget http://wald.intevation.org/frs/download.php/2003/ospd-ovaldi-1.0.0.tar.gz && \
        wget http://wald.intevation.org/frs/download.php/2149/ospd-paloalto-1.0b1.tar.gz && \
        wget http://wald.intevation.org/frs/download.php/2004/ospd-w3af-1.0.0.tar.gz && \
        wget http://wald.intevation.org/frs/download.php/2181/ospd-acunetix-1.0b1.tar.gz && \
        tar zxvf openvas-smb-1.0.1.tar.gz && \
        tar zxvf ospd-1.0.0.tar.gz && \
        tar zxvf ospd-1.0.1.tar.gz && \
        tar zxvf ospd-1.0.2.tar.gz && \
        tar zxvf ospd-ancor-1.0.0.tar.gz && \
        tar zxvf ospd-debsecan-1.0.0.tar.gz && \
        tar zxvf ospd-ovaldi-1.0.0.tar.gz && \
        tar zxvf ospd-paloalto-1.0b1.tar.gz && \
        tar zxvf ospd-w3af-1.0.0.tar.gz && \
        tar zxvf ospd-acunetix-1.0b1.tar.gz && \
    cd /osp/ospd-1.0.0 && \
        python setup.py install && \
    cd /osp/openvas-smb-1.0.1 && \
        python setup.py install && \
    cd /osp/ospd-ancor-1.0.0 && \
        pip install requests && \
        python setup.py install && \
    cd /osp/ospd-debsecan-1.0.0 && \
        python setup.py install && \
    cd /osp/ospd-ovaldi-1.0.0 && \
        python setup.py install && \
    cd /osp/ospd-1.0.1 && \
        python setup.py install && \
    cd /osp/ospd-paloalto-1.0b1 && \
        python setup.py install && \
    cd /osp/ospd-w3af-1.0.0 && \
        pip install Pexpect && \
        python setup.py install && \
    cd /osp/ospd-acunetix-1.0b1 && \
        python setup.py install && \
    cd /osp/ospd-1.0.2 && \
        python setup.py install && \
    cd /tmp && \
    wget https://github.com/Arachni/arachni/releases/download/v1.2.1/arachni-1.2.1-0.5.7.1-linux-x86_64.tar.gz && \
        tar -zxvf arachni-1.2.1-0.5.7.1-linux-x86_64.tar.gz && \
        mv arachni-1.2.1-0.5.7.1 /opt/arachni && \
        ln -s /opt/arachni/bin/* /usr/local/bin/ && \
    rm -rf /tmp/arachni* && \
    mkdir -p /openvas && \
    wget https://svn.wald.intevation.org/svn/openvas/trunk/tools/openvas-check-setup --no-check-certificate -O /openvas/openvas-check-setup && \
    chmod a+x /openvas/openvas-check-setup && \
    apt-get clean -yq && \
    apt-get autoremove -yq && \
    rm -rf /var/lib/apt/lists/* && \
    /openvas/setup.sh && \
    pip install openvas_lib  

CMD /openvas/run_scan.py

# Expose UI
EXPOSE 80 443 9390 9391 9392
