#!/usr/bin/env bash
set -e

ACTION="$1"

LOCAL_PG_SERVICE="postgresql"
LOCAL_REDIS_SERVICE="redis-server"

COMPOSE_FILE="docker-compose.yml"

function stop_local() {
  echo "▶ Stopping local PostgreSQL & Redis"
  sudo systemctl stop $LOCAL_PG_SERVICE || true
  sudo systemctl stop $LOCAL_REDIS_SERVICE || true

  sudo systemctl disable $LOCAL_PG_SERVICE || true
  sudo systemctl disable $LOCAL_REDIS_SERVICE || true
}

function start_local() {
  echo "▶ Starting local PostgreSQL & Redis"
  sudo systemctl enable $LOCAL_PG_SERVICE
  sudo systemctl enable $LOCAL_REDIS_SERVICE

  sudo systemctl start $LOCAL_PG_SERVICE
  sudo systemctl start $LOCAL_REDIS_SERVICE
}

function start_docker() {
  echo "▶ Starting Docker PostgreSQL & Redis"
  docker compose up -d
}

function stop_docker() {
  echo "▶ Stopping Docker PostgreSQL & Redis"
  docker compose down
}

function port_check() {
  echo "▶ Port check (5432 / 6379)"
  sudo ss -lntp | egrep '5432|6379' || echo "✔ Ports are free"
}

case "$ACTION" in
  local)
    stop_docker
    start_local
    port_check
    ;;
  docker)
    stop_local
    start_docker
    port_check
    ;;
  stop-all)
    stop_docker
    stop_local
    port_check
    ;;
  *)
    echo "Usage: $0 {local|docker|stop-all}"
    exit 1
    ;;
esac
# How to run: 
# ./infra-switch.sh docker
# ./infra-switch.sh local
# ./infra-switch.sh stop-all

