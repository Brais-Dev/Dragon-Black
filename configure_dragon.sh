# Créate .dragon directory
mkdir -p ~/.dragon
mv ~/Dragon-Black ~/.dragon
# Grant execution permissions
chmod +x bin/dragon
chmod +x utils/dragon_path.sh
chmod +x utils/shell-zsh.sh

echo "set Dragon Black"
apt update && apt upgrade -y
apt install git -y
apt install python3 -y

bash utils/dragon_path.sh
pip install -r "requirements.txt"
bash "utils/shell-zsh.sh"



