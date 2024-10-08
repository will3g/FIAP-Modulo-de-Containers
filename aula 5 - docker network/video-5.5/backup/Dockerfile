# busybox: Combina os utilitários mais utilizados do UNIX em um executável
FROM busybox

WORKDIR /backup

COPY handler.sh /backup/handler.sh

RUN chmod +x /backup/handler.sh

# Cron para executar após 1 hora
CMD ["/bin/sh", "-c", "/backup/handler.sh; while true; do sleep 3600; done"]
