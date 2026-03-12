# Instala en los servidores de Colab el paquete de github de Fullcontrol
# python3 -m venv venv

#if 'google.colab' in str(get_ipython()):
#  !pip install git+https://github.com/FullControlXYZ/fullcontrol --quiet
import fullcontrol as fc
#from google.colab import files
from math import tau

# printer/gcode parameters

design_name = 'Test_caperusa_delta_Python_GColab'
nozzle_temp = 210
bed_temp = 0
print_speed = 1000
fan_percent = 100
printer_name='prusa_i3' # generic / ultimaker2plus / prusa_i3 / ender_3 / cr_10 / bambulab_x1 / toolchanger_T0

# design parameters

EW = 0.8 # extrusion width
EH = 0.3 # extrusion height (and layer height)
initial_z = EH*0.6 # initial nozzle position is set to 0.6x the extrusion height to get a bit of 'squish' for good bed adhesion
layers = 50

# generate the design (make sure you've run the above cells before running this cell)

steps = []
for layer in range(layers):
  steps.append(fc.Point(x=50, y=50, z=initial_z+layer*EH))
  steps.append(fc.Point(x=100, y=50, z=initial_z+layer*EH))
  steps.append(fc.Point(x=100, y=100, z=initial_z+layer*EH))
  steps.append(fc.Point(x=50, y=100, z=initial_z+layer*EH))
  steps.append(fc.Point(x=50, y=50, z=initial_z+layer*EH))

# instead of the above for-loop code, you can create the exact same design using built-in FullControl functions (uncomment the next two lines):
# rectangle_steps = fc.rectangleXY(fc.Point(x=50, y=50, z=initial_z), 50, 50)
# steps = fc.move(rectangle_steps, fc.Vector(z=EH), copy=True, copy_quantity=layers)


# preview the design

fc.transform(steps, 'plot', fc.PlotControls(style='line', zoom=0.7))
# hover the cursor over the lines in the plot to check xyz positions of the points in the design

# uncomment the next line to create a plot with real heights/widths for extruded lines to preview the real 3D printed geometry
# fc.transform(steps, 'plot', fc.PlotControls(style='tube', zoom=0.7, initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))

# uncomment the next line to create a neat preview (click the top-left button in the plot for a .png file) - post and tag @FullControlXYZ :)
# fc.transform(steps, 'plot', fc.PlotControls(neat_for_publishing=True, zoom=0.5, initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))

# generate and save gcode

gcode_controls = fc.GcodeControls(
    printer_name=printer_name,

    initialization_data={
        'primer': 'front_lines_then_y',
        'print_speed': print_speed,
        'nozzle_temp': nozzle_temp,
        'bed_temp': bed_temp,
        'fan_percent': fan_percent,
        'extrusion_width': EW,
        'extrusion_height': EH})
gcode = fc.transform(steps, 'gcode', gcode_controls)
open(f'{design_name}.gcode', 'w').write(gcode)
files.download(f'{design_name}.gcode')

