#!/bin/bash

echo "📦 Installing mailutils..."
sudo apt-get update
sudo apt-get install -y mailutils

echo "📤 Sending notification emails..."

# Check if the EMAILS environment variable is set
if [ -z "$EMAILS" ]; then
  echo "❌ No email addresses provided. Please set the EMAILS environment variable."
  exit 1
fi

# Loop through the email list and send the message
for email in $(echo "$EMAILS" | tr ',' '\n'); do
  echo "✅ Pipeline executed successfully!" | mailx -s "Elo Drinks Pipeline Notification" "$email"
done

echo "✅ All notification emails have been sent."
