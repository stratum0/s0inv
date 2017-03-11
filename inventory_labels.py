import urllib
import labels
from reportlab.graphics import shapes
from reportlab.graphics.barcode import qr, code128, createBarcodeDrawing

def create_pdf(db, ids):
    specs = labels.Specification(57, 32, 1, 2, 57, 16)
    sheet = labels.Sheet(specs, _draw_label, border=True)
    for i in ids:
        item = _query_by(db, Item, 'id', i)
        project = _query_by(db, Project, 'name', item.project_name)
        sheet.add_label((item, project))
    sheet.save('tmp/label.pdf')
    return 'label.pdf'

def _query_by(db, model, column, value):
    kwargs = {column:value}
    return db.session.query(model).filter_by(**kwargs).first()

def _draw_label(label, width, height, obj):
    item, project = obj
    #qrcode = qr.QrCodeWidget('s0inv.de/'+str(item.id))
    long_id = str(item.id).rjust(5, '0')
    barcode = createBarcodeDrawing('Code128', value=long_id, barHeight=30, humanReadable=True, quiet=False, width=70)
    barcode.translate(26,0)
    label.add(barcode)
    qrcode = createBarcodeDrawing('QR', value='s0inv.de/'+str(item.id), barHeight=50)
    qrcode.translate(90, -2)
    label.add(qrcode)
    if project and project.logourl:
        urllib.request.urlretrieve(project.logourl, 'tmp/logo')
        logo = shapes.Image(0,2,40,40,'tmp/logo')
        label.add(logo)

