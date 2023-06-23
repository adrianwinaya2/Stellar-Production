from flask import Flask, render_template, request, redirect
import json, sys
import urllib.request, requests

app = Flask(__name__)

#====================================================================================
# API ROUTE
#====================================================================================

# ! ORDERS
@app.route('/order/', methods=['GET', 'POST'])
def order():

    with urllib.request.urlopen("http://localhost:5500/order") as url:
        data = json.load(url)
        print(data)

    display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('order.html', display_attrs=display_attrs, table=data)


@app.route('/event/', methods=['GET', 'POST'])
def event():

    with urllib.request.urlopen("http://localhost:5501/event") as url:
        data = json.load(url)

    display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('event.html', display_attrs=display_attrs, table=data)

@app.route('/event/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def event2(id):
    
    with urllib.request.urlopen(f"http://localhost:5500/event/{id}") as url:
        data = json.load(url)
        data = [data]
        print(data)

    display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('order.html', display_attrs=display_attrs, table=data)


# ! CLIENTS
@app.route('/client/', methods=['GET'])
def client():

    with urllib.request.urlopen("http://localhost:5502/client") as url:
        data = json.load(url)

    display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('client.html', display_attrs=display_attrs, table=data)

@app.route('/client/<int:id>', methods=['GET', 'PUT', 'DELEETE'])
def client2(id):

    with urllib.request.urlopen(f"http://localhost:5502/client/{id}") as url:
        data = json.load(url)
        data = [data]
        print(data)

    display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('client.html', display_attrs=display_attrs, table=data)

# ! STAFFS
@app.route('/staff/', methods=['GET'])
def staff():

    with urllib.request.urlopen("http://localhost:5503/staff") as url:
        data = json.load(url)

    display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('staff.html', display_attrs=display_attrs, table=data)

@app.route('/staff/<int:id>', methods=['GET', 'PUT', 'DELEETE'])
def staff2(id):

    with urllib.request.urlopen(f"http://localhost:5503/staff/{id}") as url:
        data = json.load(url)
        data = [data]
        print(data)

    display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('staff.html', display_attrs=display_attrs, table=data)

@app.route('/staff/<string:position>', methods=['GET', 'PUT', 'DELEETE'])
def staff3(position):

    with urllib.request.urlopen(f"http://localhost:5503/staff/{position}") as url:
        data = json.load(url)
        print(data)

    display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('staff.html', display_attrs=display_attrs, table=data)


# Tidak ada method GET nya
# @app.route('/account/', methods=['GET', 'POST'])
# def account():

#     with urllib.request.urlopen("http://localhost:5504/account") as url:
#         data = json.load(url)

#     display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
#     return render_template('account.html', display_attrs=display_attrs, table=data)



#====================================================================================
# WEB UI
#====================================================================================

# ! HOMEPAGE
@app.route('/')
def index():
    display_attrs = {"activemenu":0,"bgcolor":"#fff","bgbreadcolor":"#F0F4F7"}
    return render_template('index.html', display_attrs=display_attrs)


# ! ORDER
@app.route('/order/edit/<path:id>', methods=['GET', 'POST'])
def order_edit(id):

    # -------------------------------------------------------
    # kalau ada data POST maka kirim data json melalui REST ke KantinSvc
    if (request.method == "POST"):
        postdata = request.form.lists()
        data = {}
        data["id"] = str(id)
        for i in postdata:
            if(i[0] == "name"):   data["name"] = i[1][0]
            if(i[0] == "status"): data["status"] = i[1][0]
        jsondoc = json.dumps(data)
        print(jsondoc)

        headers = {'Content-Type': 'application/json'}
        requests.put(f"http://localhost:5500/order/{id}", data=jsondoc, headers=headers)
        urllib.request.urlopen(url)

        return redirect("/order/")

    # -------------------------------------------------------
    # kalau tidak ada data POST dari perubahan data di form, 
    # tampilkan form berisi data yang siap diubah
    else:

        with urllib.request.urlopen(f"http://localhost:5500/order/{id}") as url:
            order_data = json.load(url)

            formdata = {
                "id": str(id),
                "pic": order_data["pic_name"],
                "name": order_data["name"],
                "schedule": order_data["schedule"],
                "status": order_data["status"]
            }
        
        with urllib.request.urlopen("http://localhost:5503/staff") as url:
            staff_data = json.load(url)

        display_attrs = {"showpanel":0, "activemenu":4, "activesubmenu":41, "bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
        return render_template('order_edit.html', display_attrs=display_attrs, formdata=formdata, staff_data=staff_data)

@app.route('/order/new', methods=['GET', 'POST'])
def order_input():

    # -------------------------------------------------------
    # kalau ada data POST maka kirim data json melalui REST ke KantinSvc
    if (request.method == "POST"):
        postdata = request.form.lists()
        data = {}
        data["id"] = str(id)
        for i in postdata:
            if(i[0] == "name"):   data["name"] = i[1][0]
            if(i[0] == "status"): data["status"] = i[1][0]
        jsondoc = json.dumps(data)
        print(jsondoc)

        url     = "http://localhost:5500/order/" + str(id)
        headers = {'Content-Type': 'application/json'}
        requests.put(url, data=jsondoc, headers=headers)
        urllib.request.urlopen(url)

        return redirect("/order/")

    # -------------------------------------------------------
    # kalau tidak ada data POST dari perubahan data di form, 
    # tampilkan form berisi data yang siap diubah
    else:
        data_url = "http://localhost:5500/order/" + str(id)
        with urllib.request.urlopen(data_url) as url:
            data = json.load(url)
            formdata={}
            formdata["id"] = str(id)
            formdata["name"] = data["name"]
            formdata["status"] = data["status"]

        display_attrs = {"showpanel":0, "activemenu":4, "activesubmenu":41, "bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
        return render_template('order_edit.html', display_attrs=display_attrs, formdata=formdata)

# ! EVENT
@app.route('/event/edit/<path:id>', methods=['GET', 'POST'])
def event_edit(id):

    # -------------------------------------------------------
    # kalau ada data POST maka kirim data json melalui REST ke KantinSvc
    if (request.method == "POST"):
        postdata = request.form.lists()
        data = {}
        data["id"] = str(id)
        for i in postdata:
            if(i[0] == "name"):   data["name"] = i[1][0]
            if(i[0] == "status"): data["status"] = i[1][0]
        jsondoc = json.dumps(data)
        print(jsondoc)

        headers = {'Content-Type': 'application/json'}
        requests.put(f"http://localhost:5501/event/{id}", data=jsondoc, headers=headers)
        urllib.request.urlopen(url)

        return redirect("/event/")

    # -------------------------------------------------------
    # kalau tidak ada data POST dari perubahan data di form, 
    # tampilkan form berisi data yang siap diubah
    else:
        
        with urllib.request.urlopen(f"http://localhost:5501/event/{id}") as url:
            event_data = json.load(url)

            formdata = {
                "id": str(id),
                "order_name": event_data["order_name"],
                "name": event_data["name"],
                "pic_name": event_data["pic_name"],
                "time_start": event_data["time_start"],
                "time_end": event_data["time_end"]
            }
        
        with urllib.request.urlopen("http://localhost:5503/staff") as url:
            staff_data = json.load(url)


        display_attrs = {"showpanel":0, "activemenu":4, "activesubmenu":41, "bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
        return render_template('event_edit.html', display_attrs=display_attrs, formdata=formdata, staff_data=staff_data)


if __name__ == "__main__":
    # Mac OS kadang nabrak port 5000 maka pakai port 8000
    app.run(host="0.0.0.0", port=8000)

    # Untuk Windows
    # app.run()