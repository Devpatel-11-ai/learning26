from django.shortcuts import render

def home(request):
    return render(request, 'SerNest/home.html')

# def home(request):
#     categories = [
#         {'name': 'Electrical', 'icon': '⚡', 'desc': 'Wiring, repairs & installations', 'count': '120+'},
#         {'name': 'Plumbing', 'icon': '🔧', 'desc': 'Pipes, leaks & drain cleaning', 'count': '95+'},
#         {'name': 'Cleaning', 'icon': '🧹', 'desc': 'Deep clean, daily & move-out', 'count': '200+'},
#         {'name': 'Carpentry', 'icon': '🪚', 'desc': 'Furniture, doors & woodwork', 'count': '60+'},
#         {'name': 'Painting', 'icon': '🖌️', 'desc': 'Interior, exterior & texture', 'count': '80+'},
#         {'name': 'AC Repair', 'icon': '❄️', 'desc': 'Servicing, gas & installation', 'count': '75+'},
#     ]
#     return render(request, 'home.html', {'categories': categories})

def categories(request):
    all_categories = [
        {'name': 'Electrical', 'icon': '⚡', 'desc': 'Wiring, repairs & installations', 'count': '120+'},
        {'name': 'Plumbing', 'icon': '🔧', 'desc': 'Pipes, leaks & drain cleaning', 'count': '95+'},
        {'name': 'Cleaning', 'icon': '🧹', 'desc': 'Deep clean, daily & move-out', 'count': '200+'},
        {'name': 'Carpentry', 'icon': '🪚', 'desc': 'Furniture, doors & woodwork', 'count': '60+'},
        {'name': 'Painting', 'icon': '🖌️', 'desc': 'Interior, exterior & texture', 'count': '80+'},
        {'name': 'AC Repair', 'icon': '❄️', 'desc': 'Servicing, gas & installation', 'count': '75+'},
        {'name': 'Pest Control', 'icon': '🐛', 'desc': 'Termite, rodents & insects', 'count': '45+'},
        {'name': 'Gardening', 'icon': '🌿', 'desc': 'Landscaping & plant care', 'count': '55+'},
        {'name': 'Security', 'icon': '🔒', 'desc': 'CCTV, locks & alarms', 'count': '40+'},
    ]
    return render(request, 'SerNest/categories.html', {'categories': all_categories})

def about(request):
    return render(request, 'SerNest/about.html')

def contact(request):
    return render(request, 'SerNest/contact.html')

def login_view(request):
    return render(request, 'SerNest/login.html')

def register_view(request):
    return render(request, 'SerNest/register.html')

def provider_register(request):
    return render(request, 'SerNest/provider_register.html')
