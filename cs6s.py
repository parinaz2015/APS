from bokeh.plotting import figure,output_file,show,save, ColumnDataSource
from bokeh.models import SingleIntervalTicker, LinearAxis, Grid, Slider,CustomJS
from bokeh.layouts import row, column
from bokeh.models.grids import Grid
from bokeh.models.tools import HoverTool
# to add color pallet based on a factor
from bokeh.transform import factor_cmap  
from bokeh.palettes import Blues8
from bokeh.embed import components
from bokeh.models import Range1d
import pandas

#Read in CSV
df = pandas.read_csv('Cs.csv')
#Dataframe
# wavelength = df['wavelength']
# polarizability = df['polarizability']
#Create ColumnDataSource from Data Frame - ColumnDataSource gives more features like hover,tooltips
source= ColumnDataSource(df)


# df2=pandas.read_csv('Cs.csv')
# source= ColumnDataSource(df2)
#creates html file
output_file('graphcs6s.html')

polarizability_list = source.data['polarizability'].tolist()


TOOLTIPS = [
    ("wavelength:", "@wavelength{1.1}"),
    ("polarizability:", "@polarizability{1.111}"),
]
# # display a tooltip whenever the cursor is vertically in line with a glyph
# mode='vline'

# """
# <div>
# <h3> Cs 6s </h3>
# <div><strong>wavelength:</strong> @wavelength</div>
# <div><strong>polarizability:</strong> @polarizability</div>
# </div>
# """

#Add plot
p= figure(
    # y_range = polarizability ,
    # x_range = wavelength,
    # x = wavelength,
    # y = polarizability ,
    plot_width= 600,
    plot_height= 450,
    title= 'CS 6s',
    # fill_color = factor_cmap(
    #     'Car',
    #     palette = Blues8,
    #     factors = polarizability_list
    # ),
    tooltips=TOOLTIPS,
    x_axis_label='wavelength(nm)',
    y_axis_label= 'polarizability',
    x_axis_type = None,
    y_axis_type = None,
    tools = "pan,wheel_zoom,box_zoom,zoom_in,zoom_out,box_select,reset,save,hover,crosshair"    
)
# p.background_fill_color="#f5f5f5"
# p.grid.grid_line_color="white"
p.axis.axis_line_color = None

# change just some things about the x-grid
# p.xgrid.grid_line_color = "Blue"

# # change just some things about the y-grid
# p.ygrid.grid_line_alpha = 0.9
# # p.ygrid.grid_line_dash = [6, 4]
# p.ygrid.grid_line_color = 'navy'
# # p.ygrid.minor_grid_line_alpha = 0.1


# figure.left[0].formatter.use_scientific = False
# figure.left.formatter.use_scientific=False
# p.background_fill_color = "#eeeeee"
# defining range of xaxis and yaxis
p.x_range=Range1d(500, 1600)
p.y_range=Range1d(-5000, 5000)

# p.xgrid.visible = True
# p.xgrid.grid_line_color = "blue"
# p.xgrid.grid_line_alpha = 0.5

# p.ygrid.visible = True

#setting tickers for X axis and Y axis
ticker = SingleIntervalTicker(interval=100, num_minor_ticks=500)
xaxis = LinearAxis(ticker=ticker)
# p.xaxis.visible = True
xaxis.axis_label = "wavelength (nm)"
xaxis.axis_line_width = 1
xaxis.axis_label_text_font_style = "italic"
p.add_layout(xaxis, 'below')

tickery = SingleIntervalTicker(interval=1000, num_minor_ticks=-5000)
yaxis = LinearAxis(ticker=tickery)
# Disable scientific notation on yaxis
yaxis.formatter.use_scientific = False
yaxis.axis_label = "polarizability (a.u.)"
yaxis.axis_line_width = 1
yaxis.axis_label_text_font_style = "italic"
p.add_layout(yaxis, 'left')




#render glyph
# p.line( source = source, x= 'wavelength', y= 'polarizability' , legend='Cs 6s',line_width=3)
p.scatter(source = source, x= 'wavelength', y= 'polarizability' , marker="circle", legend='Cs 6s',size=4,alpha=0.9)
# p.circle( source = source, x= 'wavelength', y= 'polarizability' , legend='Cs 6s',color='blue')

# Add Legend
p.legend.orientation= 'vertical'
p.legend.location= 'top_right'
p.legend.label_text_font_size= '10px'


x_slider = Slider(start=500, end=1600, value=500, step=.1, title="Wavelength(nm)" )
y_slider = Slider(start=-5000, end=5000, value=-5000, step=.1, title="Polarizability(a.u.)" )

# callback should set the value for new ranges
callback = CustomJS(args=dict(source=source, x=x_slider, y=y_slider),
                    code="""
    var data = source.data;
    var xRange==x.value
    var yRange=y.value
    # p.x_range=Range1d(xRange, 1600)
    # p.y_range=Range1d(yRange, 5000)
    emit();
""")

# in case of any change in the slide bar send the value to callback
x_slider.js_on_change('value', callback)
y_slider.js_on_change('value', callback)

layout = row(
    p,
    column(x_slider, y_slider),
)

show(layout)

# Ad tooltips
# hover = HoverTool()
# hover.tooltips="""
# <div>
# <h3> Cs 6s </h3>
# <div><strong>wavelength:</strong> @wavelength</div>
# <div><strong>polarizability:</strong> @polarizability</div>
# </div>
# """
# p.add_tools(hover)


#show results
# show(p)

# save file
save(p)
#  printout components div and script
script, div = components(p)
# print(div)
# print(script)


# https://www.youtube.com/watch?v=2TR_6VaVSOs&t=419s