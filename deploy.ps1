# Set the name for your Docker image
$IMAGE_NAME = "futuro_hacker"

# Set the path to your Dockerfile
$DOCKERFILE_PATH = "Dockerfile"

# Set the VPS SSH connection details
$VPS_USERNAME = "ubuntu"
$VPS_IP = "15.229.68.116"
$VPS_SSH_KEY = "C:\Users\giga\.ssh\fh"
$REMOTE_DIR = "~/app"
$TarFilename = "$IMAGE_NAME.tar"
$TarGzipFilename = "$IMAGE_NAME.tar.gz"

# Build the Docker container
docker build -t $IMAGE_NAME -f $DOCKERFILE_PATH .

# Save the Docker image as a tarball
docker save -o $TarFilename $IMAGE_NAME

while (-not (Test-Path $TarFilename)) {
    Write-Host "Waiting for the file to exist..."
    Start-Sleep -Seconds 1  # Wait for 1 second before checking again
}

Compress-Archive -Path $TarFilename -DestinationPath $TarGzipFilename -Force

# Upload the Docker image to your VPS using SCP
scp -i $VPS_SSH_KEY $TarGzipFilename "$($VPS_USERNAME)@$($VPS_IP):$($REMOTE_DIR)/$TarGzipFilename"

# SSH into your VPS and load the Docker image
ssh -i $VPS_SSH_KEY "$($VPS_USERNAME)@$($VPS_IP)" "cd $REMOTE_DIR && unzip $TarGzipFilename && docker load -i $TarFilename"

# Run the Docker container on your VPS
ssh -i $VPS_SSH_KEY "$($VPS_USERNAME)@$($VPS_IP)" "docker run -d -p 80:5000 $IMAGE_NAME"
