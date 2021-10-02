#!/bin/sh

# Declare variables to be available to Docker.
export SPOTIFY_USER_ID="${SPOTIFY_USER_ID}"
export SPOTIFY_CLIENT_ID="${SPOTIFY_CLIENT_ID}"
export SPOTIFY_CLIENT_SECRET="${SPOTIFY_CLIENT_SECRET}"
export SPOTIFY_REDIRECT_URI="${SPOTIFY_REDIRECT_URI}"

# Generate .env file just in case the above fails for some reason.
cat << EOF > .env

SPOTIFY_USER_ID=${SPOTIFY_USER_ID}
SPOTIFY_CLIENT_ID=${SPOTIFY_CLIENT_ID}
SPOTIFY_CLIENT_SECRET=${SPOTIFY_CLIENT_SECRET}
SPOTIFY_REDIRECT_URI=${SPOTIFY_REDIRECT_URI}

EOF

# Expose app files to the host.
if [ ! -d "/app" ]; then
  ln -s /opt/app/* /app
elif [ -z "$(ls -A /app)" ]; then
  cp -a /opt/app/. /app
fi

exec "$@"
