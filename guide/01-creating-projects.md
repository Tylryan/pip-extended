# Create app from scratch

# Setup the project structure and the project environment
asu app new <app-name> --class-snippet --with-virtual-environment
asu app new <app-name> -c -e

# List all of your virtual environments 
asu env list

# Create a setup.py file
This creates an executable 
asu app setup

# Run your main file from anywhere in the file tree
asu run

# Run your command to see if it works in your environment
<executable-name>

# Build your project
asu app build

# Install your project independent of it's environment

asu app install <whatever-name-you-want>


