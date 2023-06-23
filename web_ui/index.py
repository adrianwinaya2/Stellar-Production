from flask import Flask, render_template, request, redirect, session
import json, sys
import urllib.request, requests

app = Flask(__name__)

@app.before_request
def require_authentication():
    # Check if the user is not logged in
    if 'account_id' not in session:
        # Check if the requested URL requires authentication
        if not request.path.startswith('/account'):
            # Redirect to the login page
            return redirect('/account/login')
        
#====================================================================================
# API ROUTE
#====================================================================================

# ! ORDERS
@app.route('/order/', methods=['GET'])
def order():

    with urllib.request.urlopen("http://localhost:5500/order") as url:
        data = json.load(url)
        print(data)

    display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('order.html', display_attrs=display_attrs, table=data)

@app.route('/order/<int:id>', methods=['GET'])
def order2(id):
    
    with urllib.request.urlopen(f"http://localhost:5500/order/{id}") as url:
        data = json.load(url)
        data = [data]
        print(data)

    display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('order.html', display_attrs=display_attrs, table=data)

# ! EVENTS
@app.route('/event/', methods=['GET'])
def event():

    with urllib.request.urlopen("http://localhost:5501/event") as url:
        data = json.load(url)

    display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('event.html', display_attrs=display_attrs, table=data)

@app.route('/event/<int:id>', methods=['GET'])
def event2(id):
    
    with urllib.request.urlopen(f"http://localhost:5501/event/{id}") as url:
        data = json.load(url)
        data = [data]
        print(data)

    display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('event.html', display_attrs=display_attrs, table=data)

@app.route('/order/<int:id>/events', methods=['GET'])
def event3(id):
    
    with urllib.request.urlopen(f"http://localhost:5501/order/{id}/events") as url:
        data = json.load(url)
        print(data)

    display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('event.html', display_attrs=display_attrs, table=data)


# ! CLIENTS
@app.route('/client/', methods=['GET'])
def client():

    with urllib.request.urlopen("http://localhost:5502/client") as url:
        data = json.load(url)

    display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('client.html', display_attrs=display_attrs, table=data)

@app.route('/client/<int:id>', methods=['GET'])
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

@app.route('/staff/<int:id>', methods=['GET'])
def staff2(id):

    with urllib.request.urlopen(f"http://localhost:5503/staff/{id}") as url:
        data = json.load(url)
        data = [data]
        print(data)

    display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('staff.html', display_attrs=display_attrs, table=data)

@app.route('/staff/<string:position>', methods=['GET'])
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

        data = {key: value[0] for key, value in postdata}
        jsondoc = json.dumps(data)
        print(jsondoc)

        headers = {'Content-Type': 'application/json'}
        requests.put(f"http://localhost:5500/order/{id}", data=jsondoc, headers=headers)
        # urllib.request.urlopen(url)

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
                "category": order_data["category"],
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

        data = {key: value[0] for key, value in postdata}
        data['account_id'] = session['account_id']
        jsondoc = json.dumps(data)
        print(jsondoc)

        headers = {'Content-Type': 'application/json'}
        requests.post("http://localhost:5500/order", data=jsondoc, headers=headers)
        # urllib.request.urlopen(url)

        return redirect("/order/")

    # -------------------------------------------------------
    # kalau tidak ada data POST dari perubahan data di form, 
    # tampilkan form berisi data yang siap diubah
    with urllib.request.urlopen("http://localhost:5503/staff") as url:
        staff_data = json.load(url)
        
    with urllib.request.urlopen("http://localhost:5502/client") as url:
        client_data = json.load(url)

    display_attrs = {"showpanel":0, "activemenu":4, "activesubmenu":41, "bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('order_new.html', display_attrs=display_attrs, staff_data=staff_data)

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

# ! ACCOUNT
@app.route('/account/login', methods=['GET', 'POST'])
def login():

    login_failed = False

    if (request.method == "POST"):
        postdata = request.form.to_dict()

        jsondoc = json.dumps(postdata)
        print(jsondoc)

        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"http://localhost:5504/authenticate", data=jsondoc, headers=headers)
        # urllib.request.urlopen(url)

        if response.status_code == 200:
            session['account_id'] = response.json()['account_id']
            return redirect("/")
        login_failed = True

    display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('login.html', display_attrs=display_attrs, login_failed=login_failed)

@app.route('/account/register', methods=['GET', 'POST'])
def register():

    register_failed = ''

    if (request.method == "POST"):
        postdata = request.form.lists()
        data = {}
        
        for i in postdata:
            if(i[0] == "username"):   data["username"] = i[1][0]
            if(i[0] == "password"):   data["password"] = i[1][0]
            if(i[0] == "role"): data["role"] = i[1][0]
            if(i[0] == "name"): data["name"] = i[1][0]
            if(i[0] == "email"): data["email"] = i[1][0]
            if(i[0] == "position"): data["position"] = i[1][0]
        jsondoc = json.dumps(data)
        print(jsondoc)

        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"http://localhost:5504/register", data=jsondoc, headers=headers)
        # urllib.request.urlopen(url)

        if response.status_code == 201:
            return redirect("/account/login")
        register_failed = response.json()['message']

    display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('register.html', display_attrs=display_attrs, login_failed=register_failed)

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/account/login")

if __name__ == "__main__":
    # Mac OS kadang nabrak port 5000 maka pakai port 8000
    app.run(host="0.0.0.0", port=8000)

    # Untuk Windows
    # app.run()