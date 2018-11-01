FROM mikesplain/openvas

COPY start /start
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-cache policy openvas9-scanner && \
    chmod +x /start

ADD run_scan.py /openvas/run_scan.py
RUN chmod +x /openvas/run_scan.py

EXPOSE 443 9390
