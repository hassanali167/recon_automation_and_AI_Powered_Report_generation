#!/bin/bash

echo "🔧 Updating system and installing recon tools..."

# Update and install APT-based tools
sudo apt update && sudo apt upgrade -y

echo "📦 Installing system packages..."

sudo apt install -y \
  nmap \
  whois \
  dnsenum \
  dnsrecon \
  theharvester \
  recon-ng \
  whatweb \
  wafw00f \
  amass \
  dnsutils \
  netdiscover \
  fierce \
  nikto \
  httpie \
  curl \
  git \
  python3-pip \
  ruby \
  libcurl4-openssl-dev \
  libxml2 \
  libxml2-dev \
  libxslt1-dev \
  ruby-dev \
  zlib1g-dev \
  build-essential

echo "✅ APT packages installed."

# Install Python libraries using pip
echo "🐍 Installing Python packages..."

pip3 install --user shodan --break-system-packages
pip3 install --user requests  --break-system-packages
pip install python-dotenv   --break-system-packages
 pip install reportlab    --break-system-packages
pip install sublister --break-system-packages

echo "✅ Python packages installed."

# Install Sublist3r (if not present)
if ! command -v sublist3r &> /dev/null; then
  echo "📁 Installing Sublist3r..."
  git clone https://github.com/aboul3la/Sublist3r.git ~/Sublist3r
  cd ~/Sublist3r
  pip3 install -r requirements.txt
  sudo ln -s $(pwd)/sublist3r.py /usr/local/bin/sublist3r
  chmod +x /usr/local/bin/sublist3r
  cd -
else
  echo "✅ Sublist3r already installed."
fi

# Install WPScan (Ruby tool)
if ! command -v wpscan &> /dev/null; then
  echo "🛠 Installing WPScan..."
  sudo gem install wpscan
else
  echo "✅ WPScan already installed."
fi



echo "🎉 All tools installed successfully!"
