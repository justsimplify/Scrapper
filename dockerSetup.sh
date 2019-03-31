#!/usr/bin/env bash
docker stop scrap_backend_vm && \
docker rm scrap_backend_vm && \
docker rmi scrap_backend && \
docker build -t scrap_backend . && \
docker run -d -p 8200:8000 --name=scrap_backend_vm scrap_backend