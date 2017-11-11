#Access to packages on a new computer (Windows)

Here is the procedure to follow to get the lab packages available on a new Windows 7 computer:

1. Right-click on "Computer" and select "Properties".
2. Go to the "Advanced settings" tab and click on the "Environment variables" button at the bottom.
3. You will see two lists of environment variables. In the top one, you should see in the first column names of variables like "PATH". Check if there is a variable named "PYTHONPATH". 
4. If there is a PYTHONPATH, edit it by clicking "Edit" and skip to step 6. If not, create a PYTHONPATH variable by clicking "New".
5. Name you new variable "PYTHONPATH".
6. Now input the path to the folder where the GIT repositories were cloned (typically "C:\Users\QPL\Desktop\LabSharedPrograms\"). If you are editing a preexisting path, add it at the end separated by a semi-colon (or check other variables to see which separation character you should use).

You can then check if you can import packages from the GIT repositories in Python, but remember to restart the terminal in which you are doing the test — just restarting the kernel might not be enough. 