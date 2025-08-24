#!/bin/zsh

# Usage: ./set-heroku-vars.sh <your-heroku-app-name>

APP_NAME=$1

if [ -z "$APP_NAME" ]; then
  echo "❌ Please provide the Heroku app name."
  echo "   Example: ./set-heroku-vars.sh my-gavel-app"
  exit 1
fi

# Prompt for core inputs
read -s "?🔑 Enter Admin Password: " ADMIN_PASSWORD
echo
read "?📧 Enter 'From' Email (e.g. Gavel Admin <you@example.com>): " EMAIL_FROM
read "?📨 Choose Email Provider (smtp/sendgrid/mailgun) [default: smtp]: " EMAIL_PROVIDER
EMAIL_PROVIDER=${EMAIL_PROVIDER:-smtp}

# Initialize defaults
EMAIL_USER="_unused_"
EMAIL_PASSWORD="_unused_"
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT="587"
SENDGRID_API_KEY="_unused_"
MAILGUN_DOMAIN="_unused_"
MAILGUN_API_KEY="_unused_"

# Branch logic based on provider
if [[ "$EMAIL_PROVIDER" == "smtp" ]]; then
  read "?👤 Enter SMTP Username: " EMAIL_USER
  read -s "?🔒 Enter SMTP Password: " EMAIL_PASSWORD
  echo
  read "?🌐 Enter SMTP Host [default: smtp.gmail.com]: " EMAIL_HOST
  EMAIL_HOST=${EMAIL_HOST:-smtp.gmail.com}
  read "?🔌 Enter SMTP Port [default: 587]: " EMAIL_PORT
  EMAIL_PORT=${EMAIL_PORT:-587}
elif [[ "$EMAIL_PROVIDER" == "sendgrid" ]]; then
  read -s "?🔑 Enter SendGrid API Key: " SENDGRID_API_KEY
  echo
elif [[ "$EMAIL_PROVIDER" == "mailgun" ]]; then
  read "?🌐 Enter Mailgun Domain: " MAILGUN_DOMAIN
  read -s "?🔑 Enter Mailgun API Key: " MAILGUN_API_KEY
  echo
else
  echo "❌ Invalid email provider. Must be one of: smtp, sendgrid, mailgun"
  exit 1
fi

echo "⚙️ Setting config vars for $APP_NAME..."

heroku config:set \
  ADMIN_PASSWORD="$ADMIN_PASSWORD" \
  SECRET_KEY="$(openssl rand -hex 32)" \
  BASE_URL="https://$APP_NAME.herokuapp.com" \
  VIRTUAL_EVENT="false" \
  DISABLE_EMAIL="false" \
  EMAIL_FROM="$EMAIL_FROM" \
  EMAIL_PROVIDER="$EMAIL_PROVIDER" \
  EMAIL_USER="$EMAIL_USER" \
  EMAIL_PASSWORD="$EMAIL_PASSWORD" \
  EMAIL_HOST="$EMAIL_HOST" \
  EMAIL_PORT="$EMAIL_PORT" \
  SENDGRID_API_KEY="$SENDGRID_API_KEY" \
  MAILGUN_DOMAIN="$MAILGUN_DOMAIN" \
  MAILGUN_API_KEY="$MAILGUN_API_KEY" \
  IGNORE_CONFIG_FILE="true" \
  --app $APP_NAME

echo "✅ Done! Config vars set for $APP_NAME"
