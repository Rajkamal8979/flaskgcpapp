

from bookshelf import storage
from flask import Blueprint, current_app, redirect, render_template, request, \
    url_for


crud = Blueprint('crud', __name__)


# [START upload_image_file]
def upload_image_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url
# [END upload_image_file]


@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    return render_template("list.html")


@crud.route('/view')
def view():
    storage_client = storage._get_storage_client()
    bucket = storage_client.get_bucket("processbucketflask")
    blobs = bucket.list_blobs()
    return render_template("view.html",blob=blobs)
#
@crud.route('/add', methods=['GET', 'POST'])
def add():
    #return "Came here"
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        file_url = upload_image_file(request.files.get('image'))
        return redirect(url_for('.list'))
    return render_template('form.html')


# @crud.route('/<id>/edit', methods=['GET', 'POST'])
# def edit(id):
#     book = get_model().read(id)
#
#     if request.method == 'POST':
#         data = request.form.to_dict(flat=True)
#
#         image_url = upload_image_file(request.files.get('image'))
#
#         if image_url:
#             data['imageUrl'] = image_url
#
#         book = get_model().update(data, id)
#
#         return redirect(url_for('.view', id=book['id']))
#
#     return render_template("form.html", action="Edit", book=book)
#
#
# @crud.route('/<id>/delete')
# def delete(id):
#     get_model().delete(id)
#     return redirect(url_for('.list'))
