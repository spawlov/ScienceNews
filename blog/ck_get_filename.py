def get_filename(filename, request):
    return filename.lower().replace(" ", "_").replace("-", "_")
