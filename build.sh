rm -rf build
mkdir build
cp -r public src static build/
cp *.json *.js Dockerfile build/
docker build -t homepage build
