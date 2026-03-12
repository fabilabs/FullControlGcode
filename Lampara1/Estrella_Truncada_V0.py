#if 'google.colab' in str(get_ipython()):
#  !pip install git+https://github.com/FullControlXYZ/fullcontrol --quiet
import fullcontrol as fc
#from google.colab import files
from math import tau

# printer/gcode parameters

design_name = 'Estrella_Truncada'
nozzle_temp = 230
bed_temp = 40
print_speed = 1000
fan_percent = 100
printer_name='prusa_i3' # generic / ultimaker2plus / prusa_i3 / ender_3 / cr_10 / bambulab_x1 / toolchanger_T0


# design parameters

radius = 50
# Nominal Radius (mm) - This radius is achieved when fractional radius is set to 1
# default value: 20

altura = 100
# altura en milimetros del objeto

angle_fractions = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
# Angle Fraction List (0-1) - List of fractional 'polar angles' for all points (angle increases anti-clockwise around a circle... 0 = positive x direction from centre, 0.25 = positive y direction, 1 is equivalent to 0) - google '2D polar angle' if unsure'
# default value: [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

numero_lados = 101 # numero de lados del poligono


fraccion = 1/(numero_lados -1)
angle_fractions2 = []
for n in range(int(numero_lados)):
  angle_fractions2.append(n*fraccion)


radial_fractions = [2, 0.5, 2, 0.5, 2, 0.5, 2, 0.5, 2, 0.5, 2]
# Radii Fraction List (0-1) - List of fractional radii for all points (0 = centre of circle, 1 = nominal radius)
# default value: [1,0.5,1,0.5,1,0.5,1,0.5,1,0.5,1]

# Try a double-star (change all 0.5 radii to -0.5) or a coarse spiral (radii = [0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1])

radial_fractions2=[]

for i in range(numero_lados):
  if i%2==0:
    radial_fractions2.append(1)
  else:
    radial_fractions2.append(0.8)


centre_x, centre_y = 150, 150
# XY centre - Centre of part in X and Y
# default value: 50

EW = 0.6
# Extrusion Width (mm) - Width of printed lines - recommended value: 1.5x nozzle diameter
# default value: 0.6

EH = 0.2
# Extrusion Height (mm) - Height of printed lines (i.e. layer thickness) - recommended value: 0.5x nozzle diameter
# default value: 0.2

layers = int(altura / EH)
# Layers - Number of layers to print - each layer is offset in Z by the extrusion height. Make sure layers finish at the same point they start
# default value: 1



#travel_moves = [0]*len(angle_fractions)
travel_moves = [0]*len(angle_fractions2)
# Travel Instructions - A list of 0s and 1s (one for each point in the radii/angle lists) indicate whether to print to each point or travel to it. E.g. [0,0,0,0,0,0,0,0,0,0,1] prints all lines except the last one for the default model'
# default value: [0]*len(angle_fractions)

use_retraction = False
# Use Retraction? - Set as True to use retraction commands (G10 and G11) before and after non-printing travel movements
# default value: False

initial_z = 0.8*EH # squash

# generate the design (make sure you've run the above cells before running this cell)

#if len(angle_fractions) != len(radial_fractions) or len(angle_fractions) != len(travel_moves):
if len(angle_fractions2) != len(radial_fractions2) or len(angle_fractions2) != len(travel_moves):
    #raise Exception(f'the number of angles ({len(angle_fractions)}) / radii ({len(radial_fractions)}) / travel_moves-IDs ({len(travel_moves)}) in angle_fractions / radial_fractions / travel_moves must be the same')
    raise Exception(f'the number of angles ({len(angle_fractions2)}) / radii ({len(radial_fractions2)}) / travel_moves-IDs ({len(travel_moves)}) in angle_fractions / radial_fractions / travel_moves must be the same')

def travel_retract(existing_travel_state: int, new_travel_state: int, use_retraction: bool) -> list:
    if new_travel_state == existing_travel_state:
        return []
    elif new_travel_state == 0:
        return [fc.Extruder(on=True),  fc.PrinterCommand(id='unretract')] if use_retraction else [fc.Extruder(on=True)]
    elif new_travel_state == 1:
        return [fc.Extruder(on=False),  fc.PrinterCommand(id='retract')] if use_retraction else [fc.Extruder(on=False)]
    else:
        raise Exception(f'list of "travel_moves" must only include values of 0 or 1. current value: {new_travel_state}')

centre = fc.Point(x=centre_x, y=centre_y, z=initial_z)

steps = []
existing_travel_state = 0
for layer in range(int(layers)):
    #for i in range(len(angle_fractions)):
    for i in range(len(angle_fractions2)):
      if (i)%4 != 0:
        steps.extend(travel_retract(existing_travel_state, travel_moves[i], use_retraction))
        #steps.append(fc.polar_to_point(centre, radius*radial_fractions[i], tau*angle_fractions[i]))
        #steps.append(fc.polar_to_point(centre, radius*radial_fractions2[i], tau*angle_fractions2[i]))
        steps.append(fc.polar_to_point(centre, radius*(radial_fractions2[i]+layer/800), tau*(angle_fractions2[i]+layer*fraccion/100)))
        existing_travel_state = travel_moves[i]
    centre.z += EH

if fc.distance(steps[0], steps[-1]) > 0.001:
    steps.insert(1, fc.PlotAnnotation(label='start'))
    steps.append(fc.PlotAnnotation(label='end'))
else:
    steps.append(fc.PlotAnnotation(label='start/end'))

#for i in range( 0,n):
# respuesta = 0
# if (i+1)%4 == 0: respuesta = 1
# print( 'Modulo 4 de ' + str(i) + 'es cero ? = ' + str(respuesta))


    # preview the design\n

    # fc.transform(steps, 'plot', fc.PlotControls(style='line'))
    # hover the cursor over the lines in the plot to check xyz positions of the points in the design
    # uncomment the next line to create a plot with real heights/widths for extruded lines to preview the real 3D printed geometry
    fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='tube', initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))
   # uncomment the next line to create a neat preview (click the top-left button in the plot for a .png file) - post and tag @FullControlXYZ :)\n",
   # fc.transform(steps, 'plot', fc.PlotControls(neat_for_publishing=True, zoom=0.9,  initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))\n"


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
#files.download(f'{design_name}.gcode')