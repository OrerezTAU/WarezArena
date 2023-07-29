from django.shortcuts import render
from cracken import utils


# Create your views here.
def index(request):
    """View function for home page of site."""
    # Generate the html table from the database
    utils.create_html_table()
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')


