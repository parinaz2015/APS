from bokeh.plotting import figure,output_file,show,save, ColumnDataSource
from bokeh.models import SingleIntervalTicker, LinearAxis, Grid, Slider, CustomJS, Button, Label, LabelSet
from bokeh.layouts import row, column
from bokeh.models.grids import Grid
from bokeh.models.tools import HoverTool
# to add color pallet based on a factor
from bokeh.transform import factor_cmap  
from bokeh.palettes import Set2
from bokeh.embed import components
from bokeh.models import Range1d
from bokeh.models.widgets import RangeSlider
import pandas
from bokeh.models.tools import Action
# Spans (line-type annotations) have a single dimension (width or height) and extend to the edge of the plot area.
from bokeh.models import Span 
import numpy as np
import copy
# from bokeh.io import show
# from bokeh.events import ButtonClick
# from bokeh.models.widgets import Button


#Read in CSV
df = pandas.read_csv('Cs.csv')
#Create ColumnDataSource from Data Frame - ColumnDataSource gives more features like hover,tooltips
source= ColumnDataSource(df)

df2=pandas.read_csv('7p1.csv')
source2= ColumnDataSource(df2)
# dividing data to get line graph from separate parts

#  there is dissociation where y==0
def data_function(df2):
    data =[]
    data2 = []
    y = df2['polarizability']
    x = df2['wavelength']
    negative= True
    if(y[0]>0):negative=False
    y_data=[]
    x_data=[]
    for i in range(y.shape[0]):
        if(negative and y[i]>=0):
            negative=False
            y_data.append(data)
            x_data.append(data2)
            data = []
            data2 =[]

        elif(negative==False and y[i]<=0):
            negative=True
            y_data.append(data)
            x_data.append(data2)
            data = []
            data2 =[]

        data.append(y[i])
        data2.append(x[i])
    y_data.append(data)
    x_data.append(data2)
    y_data = np.asarray(y_data)
    x_data = np.asarray(x_data)
    return x_data, y_data; 

#mark where y is almost 0
def magiczero_function(df2):
    y = df2['polarizability']
    x = df2['wavelength']
    y_data=[]
    x_data=[]
    i=0
    while i < len(y):
        if (int(y[i]) == 0 ):
            y_data.append(y[i])
            x_data.append(x[i])
        i += 1
    
    y_data = np.asarray(y_data)
    x_data = np.asarray(x_data)
    print(x_data)
    print(y_data)
    return x_data, y_data; 

#mark where df and df2 crosses
# def cross_function(df,df2):
#     y1 = df['polarizability']
#     x1 = df['wavelength']
#     y2 = df2['polarizability']
#     x2 = df2['wavelength']
#     y_data=[]
#     x_data=[]
#     i=0
#     while i < abs(len(y1)):
#         j=0
#         while j < abs(len(y2)):
#             # print(x1[i], y1[i],x2[j], y2[j] )
#             if ((int(y1[i]) == int(y2[j])) and (int(x1[i]) == int(x2[j]))):
#                 print(x1[i], y1[i])
#                 y_data.append(y1[i])
#                 x_data.append(x1[i])
#             j+= 1
#         i += 1
#     y_data = np.asarray(y_data)
#     x_data = np.asarray(x_data)
#     print(y_data)
#     print(x_data)
#     return x_data, y_data; 

# creates html file
output_file('mix2files.html')
TOOLTIPS = [
    ("wavelength:", "$x{1.1}" ),
    ("polarizability:", "$y{1.111}"),
]

p= figure(  
    plot_width= 600,
    plot_height= 450,
    title= '7p1 and Cs6s',
    tooltips= TOOLTIPS,
    x_axis_label='wavelength(nm)',
    y_axis_label= 'polarizability',
    # x_axis_type='linear',
    # y_axis_type='linear',
    x_axis_type = None,
    y_axis_type = None,
    tools = "pan,wheel_zoom,box_zoom,zoom_in,zoom_out,save,hover,crosshair"    
)

p.x_range=Range1d(500, 1800)
p.y_range=Range1d(-5000, 5000)

ticker = SingleIntervalTicker(interval=100, num_minor_ticks=1100)
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

x_slider = RangeSlider(start=500, end=1800, value=(500,1800), step=.1, title="Wavelength(nm)",width=250 )
y_slider = RangeSlider(start=-5000, end=5000, value=(-5000,5000), step=.1, title="polarizability (a.u.)",width=250 )

callback = CustomJS(args=dict(p=p, x_slide=x_slider, y_slide=y_slider),
                    code="""
    p.x_range.start = x_slide.value[0];
    p.x_range.end = x_slide.value[1];
    p.y_range.start = y_slide.value[0];
    p.y_range.end = y_slide.value[1];
""")

x_slider.js_on_change('value', callback)
y_slider.js_on_change('value', callback)

# p.scatter(source = source, x= 'wavelength', y= 'polarizability' , marker="circle", legend='Cs6s',size=2,alpha=0.9,color="green" )
# p.scatter(source = source2, x= 'wavelength', y= 'polarizability' , marker="circle", legend='7p1',size=2,alpha=0.9,color= "navy", line_join='bevel', line_cap='round' )
x_data,y_data = data_function(df)
for x,y in zip(x_data,y_data):
    p.line(x= x, y=y ,color="#ff005b", legend_label='CS6s')

x_data,y_data = data_function(df2)
for x,y in zip(x_data,y_data):
    p.line( x =x, y=y ,color="navy", legend_label='7p1' )

source = ColumnDataSource(data=dict(x=[1194.3, 1758.7],
                                    y=[0.115,  0.67],
                                    names=['x=1194.3, y=0.115','x=1758.7, y=0.67']))
x_data,y_data = magiczero_function(df2)
for x,y in zip(x_data,y_data):
    p.scatter( x =x, y=y ,color="orange", legend_label='y~0',marker="square" )

labels = LabelSet(x='x', y='y', text='names', level='glyph',
         x_offset=5, y_offset=5, source=source, border_line_color='black', border_line_alpha=1.0,
      background_fill_color='white', background_fill_alpha=1.0)

p.add_layout(labels)

x_data,y_data = magiczero_function(df)
for x,y in zip(x_data,y_data):
    p.scatter( x =x, y=y ,color="pink", legend_label='y~0',marker="square" )

# x_data,y_data = cross_function(df,df2)
# for x,y in zip(x_data,y_data):
#     p.scatter( x =x, y=y ,color="pink", legend_label='cross',marker="circlex" )

# hide glyphs by clicking on an entry in a Legend.
p.title.text = 'Click on legend entries to hide the corresponding lines'
p.legend.click_policy="hide"
# "mute" "hide"

# Vertical line
vline = Span(location=0, dimension='height', line_color='black', line_width=0.5)
# Horizontal line
hline = Span(location=0, dimension='width', line_color='black', line_width=0.5)

p.renderers.extend([vline, hline])

button = Button(label='reset',width=100, align="center")
callback2 = CustomJS(args=dict(p=p, x_slide=x_slider, y_slide=y_slider),
                    code="""
    p.reset.emit();
    x_slide.value = [500,1800]; 
    y_slide.value = [-5000,5000];
""")
button.js_on_click(callback2)

# button3 = Button(label='Download 6s',width=100, align="center")
# def export():
#     # print('I was clicked')
#     df = pandas.read_csv('Cs.csv')
#     df = pandas.DataFrame(df, columns= ['wavelength','polarizability'])
#     df.to_csv(r'C:\Users\13022\Desktop\website\Bokeh\versionFinal\export_cs.csv', index = False, header=True)
#     return send_file('export_cs',
#                      mimetype='text/csv',
#                      attachment_filename='export_cs.csv',
#                      as_attachment=True, conditional=False)
# button3.on_click(export)

# button3 = Button(label='Download 6s',width=100, align="center")
# callback3 = CustomJS(args=dict(),
#                     code = """<html>
#     <h1>hello there</h1>
#     <form method="get" action="C:\Users\13022\Desktop\website\Bokeh\versionFinal\Cs.csv">
#     <button type="submit">Download CS File</button>
#     </form>
#     </html>
# """)

# button3.js_on_click(callback3)


# df = pandas.DataFrame(df, columns= ['wavelength','polarizability'])
# df.to_csv(r'C:\Users\13022\Desktop\website\Bokeh\versionFinal\export_cs.csv', index = False, header=True)
# return send_file('export_cs.csv',
#                      mimetype='text/csv',
#                      attachment_filename='downloadFile.csv',
#                      as_attachment=True)
df = pandas.DataFrame(df, columns= ['wavelength','polarizability'])
df.to_csv(r'C:\Users\13022\Desktop\website\Bokeh\versionFinal\export_cs.csv', index = False, header=True)

df = pandas.DataFrame(df2, columns= ['wavelength','polarizability'])
df.to_csv (r'C:\Users\13022\Desktop\website\Bokeh\versionFinal\export_7p1.csv', index = False, header=True)

# print (df2)
layout = row(
    p,
    column(x_slider,y_slider,button),
)

show(layout)

