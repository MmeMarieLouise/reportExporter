import json
import dicttoxml
from flask import render_template, g
from io import BytesIO
from pdfdocument.document import PDFDocument
from app import app

# root
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# this endpoint returns the first report in the report table, this data will be used to export into other formats
@app.route('/getdata', methods=['GET'])
def getdata():
    # the results of the query is stored in a lazy object which is returned after this line is executed
    results = g.conn.execute('select * from reports')

    # to obtain the results I must run fetchall. This will return all the rows but I just need the first one so I add [0]
    first = results.fetchall()[0]

    # to show primary key and also the data
    primary_key, data = first

    # load the data in json using json.loads to get the python dictionary so that I can work with it
    data_json = json.loads(data)

    # at this point it's a python dictionary and I add the keys in the data
    org_name = data_json['organization']
    report_at = data_json['reported_at']
    created_at = data_json['created_at']

    # I pass the variables as params and map them here
    # (first one is template variable, second one is the variable of the view (json))
    return render_template('report.html', org_name=org_name, report_at=report_at, created_at=created_at)

# endpoint to export to xml format
@app.route('/xml', methods=['GET'])
def xml():
    results = g.conn.execute('select * from reports')

    first = results.fetchall()[0]

    primary_key, data = first

    data_json = json.loads(data)

    org_name = data_json['organization']
    report_at = data_json['reported_at']
    created_at = data_json['created_at']

    # create dictionary
    out_json = {
        # add header
        'Header': 'The Report',
        'Data': {
            'Organisation': org_name,
            'Reported at':report_at,
            'Created at': created_at,
        }
    }
    # run dicttoxml function and pass dictionary as a param
    xml = dicttoxml.dicttoxml(out_json)

    # return xml object with response header, add content-disposition so it downloads an attachment
    return xml, 200, {'Content-Type': 'text/xml', 'Content-Disposition': 'attachment; filename=report.xml'}



# end point that to export to pdf format
@app.route('/pdf', methods=['GET'])
def pdf():
    results = g.conn.execute('select * from reports')

    first = results.fetchall()[0]

    primary_key, data = first

    data_json = json.loads(data)

    org_name = data_json['organization']
    report_at = data_json['reported_at']
    created_at = data_json['created_at']

    # returns a file object - that stays in the memory and isn't saved
    f = BytesIO()
    # pass file object 'f' to pdf object
    pdf = PDFDocument(f)
    #initialise
    pdf.init_report()
    # convert dictionary to string and add h1 & p tags to pdf
    pdf.h1('The Report')
    pdf.p(f'Organisation: {org_name}')
    pdf.p(f'Reported at: {report_at}')
    pdf.p(f'Created at: {created_at}')
    pdf.generate()

    return f.getvalue(), 200, {'Content-Type': 'application/pdf', 'Content-Disposition':'attachment; filename=report.pdf'}