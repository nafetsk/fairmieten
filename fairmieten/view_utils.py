def layout(request):
    return "partial.html" if request.htmx else "base.html"
