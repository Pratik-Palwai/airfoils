We use these scripts in DBF to create airfoils, import them into Solidworks to design the plane, and create G-code for our four-axis CNC foam cutter.
Airfoils are stored as .afl files, which are essentially dat files but they also contain chord and camber line points (for plotting).
The sldcrv converter still works with regular dat files from airfoiltools.com
Make sure you have numpy installed
