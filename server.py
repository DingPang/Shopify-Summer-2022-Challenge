'''
Author: Ding Pang
'''
import os
import io, csv
from re import S
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, make_response, flash, session, Response, url_for
from DBHelpers import *
from datetime import date

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  I use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


# Edit
@app.route('/editonestorage', methods=["POST"])
def editonestorage():
    try:
        s = request.form["Storage"].split(" ")
        S_Id = s[0]
        name = request.form["Name"]
        Street1 = request.form["Street1"]
        Street2 = request.form["Street2"]
        City = request.form["City"]
        State = request.form["State"]
        ZIP = request.form["ZIP"]
        if not name or not Street1 or not City or not State or not ZIP:
            flash("Dont't enter something empty")
            resp = make_response(redirect("/"))
            return resp
        g.conn.execute(EDIT_STORAGE, (name, Street1, Street2, City, State, ZIP, S_Id,))
        resp = make_response(redirect("/"))
        return resp
    except:
        flash("An error has occured, Please try again")
        resp = make_response(redirect("/"))
        return resp

@app.route('/editoneitem', methods=["POST"])
def editoneitem():
    try:
        id = request.form["Item"].split(" ")[0]
        S_Id = request.cookies.get('S_Id')
        name = request.form["Name"]
        Stock = request.form["Stock"]
        g.conn.execute(EDIT_ITEM, (name, int(Stock), int(S_Id), int(id),))
        resp = make_response(redirect("/viewonestorage"))
        return resp
    except:
        flash("An error has occured or you entered something 'stupid', Please try again")
        resp = make_response(redirect("/viewonestorage"))
        return resp

# ADD
@app.route('/addonestorage', methods=["POST"])
def addonestorage():
    try:
        # get first maybe unnecessary
        # There could be duplicated address in the database because of this implementation
        # But I think this provides flexibility
        temp = g.conn.execute(GET_STORAGES_LAST_ID)
        id = 1
        x = get_first(temp)[0]
        if x:
            id = int(x) + 1
        name = request.form["Name"]
        Street1 = request.form["Street1"]
        Street2 = request.form["Street2"]
        City = request.form["City"]
        State = request.form["State"]
        ZIP = request.form["ZIP"]
        if not name or not Street1 or not City or not State or not ZIP:
            flash("Don't enter something empty")
            resp = make_response(redirect("/"))
            return resp
        g.conn.execute(INSERT_ADDRESS, (id, name, Street1, Street2, City, State, ZIP,))
        resp = make_response(redirect("/"))
        return resp
    except:
        flash("An error has occured, Please try again")
        resp = make_response(redirect("/"))
        return resp

@app.route('/addoneitem', methods=["POST"])
def addoneitem():
    try:
        S_Id = request.cookies.get('S_Id')
        temp = g.conn.execute(GET_ITEM_LAST_ID, (int(S_Id)))
        id = 1
        x =  get_first(temp)[0]
        if x:
            id = int(x) + 1
        name = request.form["Name"]
        Stock = request.form["Stock"]
        g.conn.execute(INSERT_ITEM, (int(S_Id), int(id), name, int(Stock),))
        resp = make_response(redirect("/viewonestorage"))
        return resp
    except:
        flash("An error has occured or you entered something 'stupid', Please try again")
        resp = make_response(redirect("/viewonestorage"))
        return resp


# Remove
@app.route('/removeonestorage', methods=["POST"])
def removeonestorage():
    try:
        s = request.form["Storage"].split(" ")
        S_Id = s[0]
        cursor = g.conn.execute(REMOVE_ONE_STORAGE, (int(S_Id)))
        resp = make_response(redirect("/"))
        return resp
    except:
        flash("An error has occured, Please try again")
        resp = make_response(redirect("/"))
        return resp

@app.route('/removeoneitem', methods=["POST"])
def removeoneitem():
    try:
        s = request.form["Item"].split(" ")
        Part_Id = s[0]
        S_Id = request.cookies.get('S_Id')
        cursor = g.conn.execute(REMOVE_ONE_ITEM, (int(Part_Id), int(S_Id),))
        resp = make_response(redirect("/viewonestorage"))
        return resp
    except:
        flash("An error has occured, Please try again")
        resp = make_response(redirect("/viewonestorage"))
        return resp

# View
@app.route('/viewonestorage', methods=["POST", "GET"])
def viewonestorage():
    try:
        if request.method == "POST":
            s = request.form["Storage"].split(" ")
            S_Id = s[0]
            Name = " ".join(s[1:])
            cursor = g.conn.execute(GET_ONE_STORAGE, (int(S_Id)))
            inventory = [s for s in cursor]
            context = dict(inventory = inventory, S_Id = S_Id, Name = Name)
            resp = make_response(render_template("viewonestorage.html", **context))
            resp.set_cookie("S_Id", S_Id)
            resp.set_cookie("Name", Name)
            return resp
        else:
            S_Id = request.cookies.get('S_Id')
            Name = request.cookies.get("Name")
            if not Name or not S_Id:
                flash("An error has occured, Please try again")
                resp = make_response(redirect("/"))
                return resp
            cursor = g.conn.execute(GET_ONE_STORAGE, (int(S_Id)))
            inventory = [s for s in cursor]
            context = dict(inventory = inventory, S_Id = S_Id, Name = Name)
            resp = make_response(render_template("viewonestorage.html", **context))
            return resp
    except:
        flash("An error has occured, Please try again")
        resp = make_response(redirect("/"))
        return resp

@app.route('/viewall', methods=["GET"])
def viewall():
    try:
        Storages = {}
        cursor = g.conn.execute(GET_ALL)
        cursor = [s for s in cursor]
        for c in cursor:
            sname = c[1]
            if sname not in Storages:
                Storages[sname] = {}
                Storages[sname]["address"] = ", ".join([i for i in c[2:7] if i])
                Storages[sname]["inventory"] = []
            Storages[sname]["inventory"].append(c[7:])
        context = dict(Storages = Storages)
        resp = make_response(render_template("viewall.html", **context))
        return resp
    except:
        flash("An error has occured, Please try again")
        resp = make_response(redirect("/"))
        return resp

@app.route('/', defaults={'path': ''}, methods=["GET"])
@app.route('/<path:path>')
def index(path):
    try:
        if path:
            return make_response(redirect("/"))
        cursor = g.conn.execute(GET_ALL_STORAGES)
        storages = [s for s in cursor]
        context = dict(storages = storages)
        resp = make_response(render_template("index.html", **context))
        return resp
    except:
        pass

# downloads
@app.route('/download/storagescsv')
def downloadstoragescsv():
    try:
        cursor = g.conn.execute(GET_ALL_STORAGES)
        cursor = [s for s in cursor]
        output = io.StringIO()
        writer = csv.writer(output)
        line = 'S_Id, Name, Street1, Street2, City, State, ZIP'.split(", ")
        writer.writerow(line)
        for row in cursor:
            line = [str(i) for i in row]
            writer.writerow(line)
        resp = make_response(output.getvalue())
        resp.headers["Content-Disposition"] = "attachment; filename=storages.csv"
        resp.headers["Content-type"] = "text/csv"
        return resp
    except:
        flash("An error has occured, Please try again")
        resp = make_response(redirect("/"))
        return resp

@app.route('/download/storagecsv')
def downloadstoragecsv():
    try:
        S_Id = request.cookies.get("S_Id")
        Name = request.cookies.get("Name")
        cursor = g.conn.execute(GET_ONE_STORAGE, (int(S_Id)))
        cursor = [s for s in cursor]
        output = io.StringIO()
        writer = csv.writer(output)
        line = 'Part_Id, Name, Stock'.split(", ")
        writer.writerow(line)
        for row in cursor:
            line = [str(i) for i in row]
            writer.writerow(line)
        resp = make_response(output.getvalue())
        resp.headers["Content-Disposition"] = "attachment; filename="+Name+".csv"
        resp.headers["Content-type"] = "text/csv"
        return resp
    except:
        flash("An error has occured, Please try again")
        resp = make_response(redirect("/"))
        return resp

@app.route('/download/allcsv')
def downloadallcsv():
    try:
        Storages = {}
        store = set()
        cursor = g.conn.execute(GET_ALL)
        cursor = [s for s in cursor]
        output = io.StringIO()
        writer = csv.writer(output)
        line = 'S_Id, Name, Address, Part_Id, Name, Stock'.split(", ")
        writer.writerow(line)
        for c in cursor:
            sname = c[1]
            if sname not in Storages:
                Storages[sname] = {}
                Storages[sname]["id"] = c[0]
                Storages[sname]["address"] = ", ".join([i for i in c[2:7] if i])
                Storages[sname]["inventory"] = []
            Storages[sname]["inventory"].append(c[7:])

        for sname in Storages:
            add = Storages[sname]["address"]
            for j in Storages[sname]["inventory"]:
                l = None
                if sname not in store:
                    store.add(sname)
                    l = [str(Storages[sname]["id"]), sname, add] + [str(i) for i in j]
                else:
                    l = [""]*3+[str(i) for i in j]
                writer.writerow(l)

        resp = make_response(output.getvalue())
        resp.headers["Content-Disposition"] = "attachment; filename=all.csv"
        resp.headers["Content-type"] = "text/csv"
        return resp
    except:
        flash("An error has occured, Please try again")
        resp = make_response(redirect("/"))
        return resp



if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=False)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("RUNNING!!!!!")
    print("running on " + str(HOST) + " : " + str(PORT))
    app.secret_key = 'super secret key'
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()

