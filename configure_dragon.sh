# Créate .dragon directory
mkdir -p ~/.dragon
mv ~/Dragon-Black ~/.dragon
# Grant execution permissions
chmod +x bin/dragon
chmod +x utils/dragon_path.sh
bash utils/dragon_path.sh

echo "set Dragon Black"
file="utils/packet_installer.sh"
bash $file



