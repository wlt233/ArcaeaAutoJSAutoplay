# ArcaeaAutoJSAutoplay
A Python script that transcript Arcaea chart file (.aff file) into AutoJS touchscreen script which automatically plays the Arcaea chart.

# Notes and Disclamers
1. **THIS PROGRAM IS NOT INTENDED FOR CHEATING OR ANY OTHER ILLEGAL USES.**
2. There are many things you can do with this program, such as learning how to interact with Android Input Event, or simply using it to record fanmade Arcaea charts.
3. This program has been identified as having an architectural flaw and thus needs to be completely refactored. There is no real benefit to continuing to improve the program.
4. No reverse engineering work is done during the development of this program.
5. This program is not affiliated with Lowiro or any other commercial organizations, and the Arcaea trademark is owned by Lowiro.

# Prerequisites
- AutoJS Pro v8 (This is a paid application!)
- Rooted Android device
- the .AFF file for the Arcaea chart

# How to use

1. Edit the Argument List based on the situations of your Android device.
2. Put an .aff file into the same folder as the python script, and rename the file to 0.aff.
3. Run the python script.
4. Open the corresponding Arcaea chart in the game. After the game loads into the gamplay scene, press the pause button.
5. Run the generated generated .js script remotely from your computer on your Android Device. About how to perform remote debugging, please refer to the AutoJS document.
6. The Program will automatically control the device to restart and play the chart. You might need to go back to step 1 and edit the Input Offset to make the program play more precisely.
