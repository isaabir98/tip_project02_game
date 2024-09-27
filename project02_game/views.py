def pagehome(request):
    return render(request,'frontface.html')


@app.route('/')
def index(request):
    """Video streaming home page."""
    return render(request,'index.html')
