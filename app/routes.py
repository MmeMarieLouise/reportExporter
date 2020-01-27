import json
import dicttoxml
from flask import render_template, g
from io import BytesIO
from pdfdocument.document import PDFDocument
from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/getdata', methods=['GET'])
def getdata():
    # this is the lazy object for the results of the query that was run from reports
    # - the results is stored in a lazy object
    results = g.conn.execute('select * from reports')

    # fetchall return all the rows but I just need the first one so I add [0]
    first = results.fetchall()[0]

    # to retrieve or show primary key and also the data
    primary_key, data = first

    # load the data in json using json.loads to get the python dictionary so that I can work with it
    data_json = json.loads(data)

    # at this point it's a python dictionary and I add the keys in the data
    org_name = data_json['organization']
    report_at = data_json['reported_at']
    created_at = data_json['created_at']

    # pass the variables I must map it here (first one is template variable, second one is the variable
    # of the view (json)
    return render_template('report.html', org_name=org_name, report_at=report_at, created_at=created_at)


@app.route('/xml', methods=['GET'])
def xml():
    results = g.conn.execute('select * from reports')

    first = results.fetchall()[0]

    primary_key, data = first

    data_json = json.loads(data)

    org_name = data_json['organization']
    report_at = data_json['reported_at']
    created_at = data_json['created_at']

    out_json = {
        'Header': 'The Report',
        'Data': {
            'Organisation': org_name,
            'Reported at':report_at,
            'Created at': created_at,
        }
    }

    xml = dicttoxml.dicttoxml(out_json)

    return xml, 200, {'Content-Type': 'text/xml', 'Content-Disposition': 'attachment; filename=report.xml'}


# to do get template file to show

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
    # passing file object to pdf object
    pdf = PDFDocument(f)
    pdf.init_report()

    pdf.h1('The Report')

    pdf.p(f'Organisation: {org_name}')
    pdf.p(f'Reported at: {report_at}')
    pdf.p(f'Created at: {created_at}')
    # convert python dictionary to string and adds a p tag to pdf
    #pdf.p(f'org')
    pdf.generate()

    return f.getvalue(), 200, {'Content-Type': 'application/pdf', 'Content-Disposition':'attachment; filename=report.pdf'}

