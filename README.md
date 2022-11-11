# LinearToSpace
A utility for importing projects and issues from Linear to Jetbrains space

### How it works
1. Configure a Python 3.10+ virtual environment and install all the dependencies in [requirements.txt](requirements.txt)
2. Create an application and application permanent token on Jetbrains Space
![App on Jetbrains Image](docs/jetbrains-app-key.jpg?raw=true "Title")
3. Provide the necessary permissions for the application
![Configure Permissions Image](docs/permissions.jpg?raw=true "Title")
4. Create a Personal Key on Linear
![Personal Key Image](docs/linear-personal-token.jpg?raw=true "Title")
5. Run the main.py file


### What's not added
Feel free to make a PR to enable this functionalities
- Importing members into a project
- Checking whether an issue exists on Jetbrains before creating it. We completely avoid this by not creating issues for a project that already exists
- Custom Fields