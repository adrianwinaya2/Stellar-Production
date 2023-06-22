from flask import Flask, render_template, request, redirect
import json, sys
import urllib.request, requests

app = Flask(__name__)



#====================================================================================
# SHOW HOMEPAGE
#====================================================================================
@app.route('/')
def index():
    display_attrs = {"activemenu":0,"bgcolor":"#fff","bgbreadcolor":"#F0F4F7"}
    return render_template('index.html', display_attrs=display_attrs)



#====================================================================================
# SHOW ALL RESTOs AND MENUs
#====================================================================================
@app.route('/order/', methods=['GET', 'POST'])
def resto():

    with urllib.request.urlopen("http://localhost:5500/order") as url:
        data = json.load(url)

    display_attrs = {"activemenu":4,"bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
    return render_template('order.html', display_attrs=display_attrs, table=data)



#====================================================================================
# EDIT RESTO
#====================================================================================
@app.route('/resto_edit/<path:id>', methods=['GET', 'POST'])
def resto_edit(id):

    # -------------------------------------------------------
    # kalau ada data POST maka kirim data json melalui REST ke KantinSvc
    if (request.method == "POST"):
        postdata = request.form.lists()
        data = {}
        data["id"] = str(id)
        for i in postdata:
            if(i[0] == "nama"):   data["nama"] = i[1][0]
            if(i[0] == "gedung"): data["gedung"] = i[1][0]
        jsondoc = json.dumps(data)
        print(jsondoc)

        url     = "http://localhost:5500/kantin/" + str(id)
        headers = {'Content-Type': 'application/json'}
        requests.put(url, data=jsondoc, headers=headers)
        urllib.request.urlopen(url)

        return redirect("/resto/")

    # -------------------------------------------------------
    # kalau tidak ada data POST dari perubahan data di form, 
    # tampilkan form berisi data yang siap diubah
    else:
        data_url = "http://localhost:5500/kantin/" + str(id)
        with urllib.request.urlopen(data_url) as url:
            data = json.load(url)
            formdata={}
            formdata["id"] = str(id)
            formdata["nama"] = data["nama"]
            formdata["gedung"] = data["gedung"]

        display_attrs = {"showpanel":0, "activemenu":4, "activesubmenu":41, "bgcolor":"#E9ECEF","bgbreadcolor":"#dee2e6"}
        return render_template('resto_edit.html', display_attrs=display_attrs, formdata=formdata)


if __name__ == "__main__":
    # Mac OS kadang nabrak port 5000 maka pakai port 8000
    app.run(host="0.0.0.0", port=8000)

    # Untuk Windows
    # app.run()
