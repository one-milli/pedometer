from flask import Flask, request, jsonify, make_response, render_template
import datetime
app = Flask(__name__)
# print(app.config)

# global variables
cnt_today = 0
# step_dict = {}
ip_dict = {}
dt_now = datetime.datetime.now()
# date_pre = str(dt_now.hour)+':'+str(dt_now.minute)  # for test
# date_pre = str(dt_now.year)+'/'+str(dt_now.month)+'/'+str(dt_now.day)


class ip_step_data(object):
    def __init__(self, ip):
        self.ip = ip
        self.step_dict = {}

    # 日付とADCを入力して、1500以下であれば、その日付にカウントする
    def count_step(self, date, adc):
        if (date not in self.step_dict) and (adc < 1500):
            self.step_dict[date] = 1
        elif (date in self.step_dict) and (adc < 1500):
            self.step_dict[date] = self.step_dict[date]+1


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
    # global cnt_today
    # global date_pre
    ip_temp = request.remote_addr  # record ip addr of the request

    dt_now = datetime.datetime.now()
    date = str(dt_now.hour)+':'+str(dt_now.minute)  # for test
    # date = str(dt_now.year)+'/'+str(dt_now.month)+'/'+str(dt_now.day)
    # if date != date_pre:    # if date changed
    #     cnt_today = 0

    # if adc_value < 1500:  # 1step
    #     cnt_today += 1

    ip_dict[ip_temp] = ip_step_data(ip_temp)
    ip_dict[ip_temp].input_step(date, adc_value)
    print("Steps = "+str(ip_dict[ip_temp].step_dict[date]))

    # step_dict[date] = cnt_today

    # date_pre = date

    print("Data by day: ", ip_dict[ip_temp].step_dict)
    print("IP: ", ip_temp)

    if cnt_today == 10:
        print("10 steps achieved.")
#################################################
# 修正する必要あるかもしれません
    json_data = {"adc": adc_value, "time": time}
    return jsonify(json_data)


@app.route('/status')
def status():
    return render_template("index.html", cnt=cnt_today)
#######################################################


@app.route('/graph1')
def graph1():
    import math
    import numpy
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    import io

    global time_list
    global adc_list

    fig = plt.figure()
    i = 1
    for item in ip_dict:
        locals()['ax%s' % i] = fig.add_subplot(111)
        locals()['ax%s' % i].bar(
            item.step_dict.keys(), item.step_dict.values())
        locals()['ax%s' % i].set_xlabel("date")
        locals()['ax%s' % i].set_ylabel("steps")
        locals()['ax%s' % i].set_title(str(item.ip))
        i = i+1

    canvas = FigureCanvasAgg(fig)
    buf = io.BytesIO()
    canvas.print_png(buf)
    data = buf.getvalue()

    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)
    return response


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=50000, debug=True, threaded=True)
