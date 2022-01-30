from flask import Flask, request, jsonify, make_response, render_template
import datetime
app = Flask(__name__)
# print(app.config)

# global variables
cnt_today = 0
step_dict = {}
ip_dict = {}
dt_now = datetime.datetime.now()
date_pre = str(dt_now.hour)+':'+str(dt_now.minute)  # for test
# date_pre = str(dt_now.year)+'/'+str(dt_now.month)+'/'+str(dt_now.day)


@app.route("/")
def hello():
    # this is test page
    return "Hello World !!"


@app.route("/getadc", methods=['GET'])
def getadc():
    print("Request = ")
    print(request.args)
    adc_value = request.args.get('ADC', type=int)
    time = request.args.get('TIME', type=int)
    global cnt_today
    global date_pre
    dt_now = datetime.datetime.now()
    date = str(dt_now.hour)+':'+str(dt_now.minute)  # for test
    # date = str(dt_now.year)+'/'+str(dt_now.month)+'/'+str(dt_now.day)
    if date != date_pre:    # if date changed
        cnt_today = 0

    if adc_value < 1500:  # 1step
        cnt_today += 1

    print("Steps = "+str(cnt_today))
    ip_dict[request.remote_addr] = cnt_today
    step_dict[date] = cnt_today

    date_pre = date

    print("Data by day: ", step_dict)
    print("IP: ", ip_dict)

    if cnt_today == 10:
        print("10 steps achieved.")

    json_data = {"adc": adc_value, "time": time}
    return jsonify(json_data)


@app.route('/status')
def status():
    return render_template("index.html", cnt=cnt_today)


@app.route('/graph1')
def graph1():
    import math
    import numpy
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    import io

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(step_dict.keys(), step_dict.values())
    ax.set_xlabel("date")
    ax.set_ylabel("steps")

    canvas = FigureCanvasAgg(fig)
    buf = io.BytesIO()
    canvas.print_png(buf)
    data = buf.getvalue()

    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)
    return response


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=50000, debug=True, threaded=True)
