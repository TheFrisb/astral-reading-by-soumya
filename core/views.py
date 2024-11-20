from django.shortcuts import render


# Create your views here.
def generate_page_tags(page_title: str = None) -> dict:
    return {"title": page_title}


def home(request):
    context = {"page_tags": generate_page_tags("Home")}
    return render(request, context=context, template_name="core/pages/horoscopes.html")
