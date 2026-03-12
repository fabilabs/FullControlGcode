#Elaborado por Fabian Fagua 

import fullcontrol as fc
from math import tau, sin, cos

# Parametros del diseño

design_name = 'Delta_Cyl_Test'
layers = 30 #  numero de capas del diseño
radio = 50 # radio del cilindro de prueba

EH = 0.3 # altura de cada capa "extrusion_height"
EW = 0.4 #0.8 # ancho de cada capa "extrusion_width"
initial_z = 0.8*EH # altura de la capa inicial es el 80% de la altura de capa


# create the initialize procedure (i.e. start_gcode)
initial_settings = {
    "extrusion_width": EW,
    "extrusion_height": EH,
    "e_units": "mm3",
    "dia_feed": 1.75,
    #"primer": "no_primer",
    "primer": "travel",
    "print_speed": 2000,
    "travel_speed": 4000
}
gcode_controls = fc.GcodeControls(printer_name='custom', initialization_data=initial_settings)
starting_procedure_steps = []
starting_procedure_steps.append(fc.ManualGcode(text='\n; #####\n; ##### beginning of start procedure\n; #####'))
starting_procedure_steps.append(fc.ManualGcode(text='G28 ; home'))
starting_procedure_steps.append(fc.GcodeComment(text='heat bed 10 degrees too hot'))
starting_procedure_steps.append(fc.Buildplate(temp=60, wait=True))
starting_procedure_steps.append(fc.GcodeComment(text='allow bed to cool to the correct temp and heat up nozzle'))
starting_procedure_steps.append(fc.Hotend(temp=220, wait=False))
starting_procedure_steps.append(fc.Buildplate(temp=50, wait=True))
starting_procedure_steps.append(fc.Hotend(temp=220, wait=True))
starting_procedure_steps.append(fc.Fan(speed_percent=100))
starting_procedure_steps.append(fc.Extruder(relative_gcode=True))
starting_procedure_steps.append(fc.Point(x=0, y=0, z=5))
starting_procedure_steps.append(fc.ManualGcode(text='; #####\n; ##### end of start procedure\n; #####\n'))


# create the final procedure (i.e. end_gcode)


ending_procedure_steps = []
ending_procedure_steps.append(fc.ManualGcode(text='\n; #####\n; ##### beginning of ending procedure\n; #####'))
ending_procedure_steps.append(fc.Extruder(on=False))
ending_procedure_steps.append(fc.GcodeComment(text='heat bed 10 degrees too hot'))
ending_procedure_steps.append(fc.Buildplate(temp=0, wait=False))
ending_procedure_steps.append(fc.GcodeComment(text='allow bed to cool to the correct temp and heat up nozzle'))
ending_procedure_steps.append(fc.Hotend(temp=0, wait=False))
ending_procedure_steps.append(fc.Fan(speed_percent=0))
ending_procedure_steps.append(fc.ManualGcode(text='G28 ; home'))
ending_procedure_steps.append(fc.ManualGcode(text='; #####\n; ##### end of start procedure\n; #####\n'))

# generate the design (make sure you've run the above cells before running this cell)
# CUBO

steps = []
steps.append(fc.Extruder(on=True))
for layer in range(layers):
  steps.append(fc.Point(x=-50, y=-50, z=initial_z+layer*EH))
  steps.append(fc.Point(x=50, y=-50, z=initial_z+layer*EH))
  steps.append(fc.Point(x=50, y=50, z=initial_z+layer*EH))
  steps.append(fc.Point(x=-50, y=50, z=initial_z+layer*EH))
  steps.append(fc.Point(x=-50, y=-50, z=initial_z+layer*EH))

# instead of the above for-loop code, you can create the exact same design using built-in FullControl functions (uncomment the next two lines):
# rectangle_steps = fc.rectangleXY(fc.Point(x=50, y=50, z=initial_z), 50, 50)
# steps = fc.move(rectangle_steps, fc.Vector(z=EH), copy=True, copy_quantity=layers)
# generate the design
# Cilindro
from math import cos, tau
layers = 50
segments_per_layer = 64
centre = fc.Point(x=0, y=0, z=initial_z)
layer_height = EH
steps_cyl = []
for i in range(layers*segments_per_layer+1):
    # find useful measures of completion
    layer_fraction = (i%segments_per_layer)/segments_per_layer
    total_fraction = (int(i/segments_per_layer)+layer_fraction)/layers
    # calculate polar details
    angle = layer_fraction*tau
    #radius = radio*EW+1*cos(tau*(total_fraction))
    radius = radio
    centre.z = layer_height*layers*total_fraction
    # add point
    steps_cyl.append(fc.polar_to_point(centre, radius, angle))


# Diseño del primer en spiral del centro al exterior

#start_radius = 2
#end_radius = 8
start_angle = 0
n_turns = int(radio/(2*EW))
segments = 32*n_turns
#z_change = 0
#clockwise = True
# steps = fc.spiralXY(centre_point, start_radius, end_radius, start_angle, n_turns, segments, clockwise)
#primer_steps = fc.spiralXY(fc.Point(x=0, y=0, z=initial_z), start_radius, end_radius, start_angle, n_turns, segments)
primer_steps = fc.spiralXY(fc.Point(x=0, y=0, z=initial_z), EW, radio, start_angle, n_turns, segments)

# combine start procedure and design to create the overall procedure
#steps = starting_procedure_steps + design_steps  # Sin Esperial de primer  usar  // usar "primer": "no_primer", en  initial_settings = {
#steps = starting_procedure_steps + primer_steps + steps # con espiral de primer // usar "primer": "travel", en  initial_settings = {
steps = starting_procedure_steps + primer_steps + steps_cyl + ending_procedure_steps  # con espiral de primer // usar "primer": "travel", en  initial_settings = {

# preview the design

#fc.transform(steps, 'plot', fc.PlotControls(style='line', zoom=0.7))
# hover the cursor over the lines in the plot to check xyz positions of the points in the design

# uncomment the next line to create a plot with real heights/widths for extruded lines to preview the real 3D printed geometry
fc.transform(steps, 'plot', fc.PlotControls(style='tube', zoom=0.7, initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))

# uncomment the next line to create a neat preview (click the top-left button in the plot for a .png file) - post and tag @FullControlXYZ :)
# fc.transform(steps, 'plot', fc.PlotControls(neat_for_publishing=True, zoom=0.5, initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))


# Visualizar el GCODE

print(fc.transform(steps, 'gcode', gcode_controls))


gcode = fc.transform(steps, 'gcode', gcode_controls)
open(f'{design_name}.gcode', 'w').write(gcode)
# files.download(f'{design_name}.gcode')