from flask import Flask, render_template
#importing flask from flask
#render template accesses html in python app and displays it

app = Flask(__name__)
#flask object is instantiated

@app.route('/')
def home():
    return render_template('home.html')
#the output is mapped to the url found in app.route
#home.html must be a file found in a folder called templates

@app.route('/plot')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure,show,output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start = datetime.datetime(2015,11,1)
    end = datetime.datetime(2016,3,10)
    df = data.DataReader(name = 'GOOG',data_source = 'yahoo',start=start,end=end )
    #here can change the start and ends times, name can be changed to the relevent indicator

    def inc_dec(c,o):
        if c>o:
            value = "Increase"
        elif c<o:
            value = "Decrease"
        else:
            value= "equal"
        return value

    df["Status"] = [inc_dec(c,o) for c,o in zip(df.Close,df.Open)]
    df["Middle"] = (df.Open + df.Close)/2
    df["Height"] = abs(df.Open - df.Close)
    #creating intermediate results for read-ability
    p = figure(x_axis_type = 'datetime', width =1000,height = 300,sizing_mode='scale_width')
    p.title.text='Candlestick Chart'
    p.title.align = "center"
    p.title.text_font_size= "35px"
    p.grid.grid_line_alpha = 0.4


    hours_12=12*60*60*1000 #to get the milliseconds, as bokeh accepts milliseconds

    p.segment(df.index,df.High,df.index,df.Low,color="black") #high and low lines on the candle chart

    p.rect(df.index[df.Status == "Increase"],df.Middle[df.Status == "Increase"],hours_12,df.Height[df.Status == "Increase"],
        fill_color = "#7FFF00",line_color = 'black') #as subtraction, abs will provide whole num
    p.rect(df.index[df.Status == "Decrease"],df.Middle[df.Status == "Decrease"],hours_12,df.Height[df.Status == "Decrease"],
        fill_color = "#FF3333",line_color = 'black') #abs is for the height of the candle stick


    script1 , div1 = components(p) #component is a tuple with two items containing the info to embed the chart
    #script1 is the javascript only, div1 is the html
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files
    #cdn to get the correct updated version for the website


    #output_file('CS.html')
    #show(p)
    return render_template('plot.html',
    script1 = script1,
    div1 = div1,
    cdn_css = cdn_css,
    cdn_js = cdn_js)
    #adding the varibles allows the varible to be embedded into the script 1 placeholder and div1 too


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
#__name__ is equal to __main__ only when executed through the terminal
#if executed by copy and pasting the script, the __name__ would be 'test' name of the file
#app.run is only running when __name__ is equal to __main__


#.\virtual\Scripts\pip freeze > requirements.txt used to create a list of required libraries
