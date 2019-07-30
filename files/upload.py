from files.models import Document
import hashlib
import magic


def handle_uploaded_file(files):
    for f in files:
        # Do something with each file.
        with open('media/' + f.name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        md5_hash = hashlib.md5()
        with open('media/' + f.name, "rb") as infile:
            for byte_block in iter(lambda: infile.read(4096), b""):
                md5_hash.update(byte_block)
            md5sum = md5_hash.hexdigest()

        mime = magic.Magic(mime=True).from_file(('media/' + f.name))

        doc = Document(filename=f.name, md5sum=md5sum, filesize=str(len(f)), uploader='Niels', type=mime)
        doc.save()