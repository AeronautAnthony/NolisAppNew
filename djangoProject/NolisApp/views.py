from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count, Q
from django.contrib import messages
from .models import FlavorPreference, Ingredients as IngredientModel,Product

# Create your views here.
def Welcome(request):
    return render(request, 'NolisApp/Welcome.html', {})
 #View for the welcome page renders welcome.html
def Flavor(request):
    if request.method == 'POST':
        selected_flavor = request.POST.get('flavor').lower()
        try:
            flavor = FlavorPreference.objects.get(flavor_Name__iexact=selected_flavor)
            request.session['flavor_id'] = flavor.id
            return redirect('Ingredients')
        except FlavorPreference.DoesNotExist:
            return redirect('Flavor')

    return render(request, 'NolisApp/Flavor.html', {})
#This view handles flavor selection and processes choices from a post request

def Ingredients(request):
    flavor_id = request.session.get('flavor_id')
    if not flavor_id:
        return redirect('Flavor')
    ingredients = IngredientModel.objects.filter(flavor_id=flavor_id)
    return render(request, 'NolisApp/Ingredients.html', {'ingredients': ingredients})
# this gets the flavor ID and fetches the Ingredients that match


def process_ingredients(request):
    flavor_id = request.session.get('flavor_id')
    if request.method == 'POST':
        selected_ingredients = request.POST.getlist('selected_ingredients')

        #If no Ingredients are selected displays message
        if not selected_ingredients:
            ingredients = IngredientModel.objects.filter(flavor_id=flavor_id)
            context = {
                'ingredients': ingredients,
                'error_message': 'You must select at least one ingredient.',
            }
            return render(request, 'NolisApp/Ingredients.html', context)

        #sets limit of chosen Ingredients to 5
        if len(selected_ingredients) > 5:
            ingredients = IngredientModel.objects.filter(flavor_id=flavor_id)
            context = {
                'ingredients': ingredients,
                'error_message': 'You can select a maximum of 5 ingredients.',
            } # error message passed to html doc if no more than 5 chosen
            return render(request, 'NolisApp/Ingredients.html', context)
        else:
            request.session['selected_ingredient_ids'] = selected_ingredients
            return redirect(reverse('Recommendation'))
    else:
        return redirect(reverse('Ingredients'))


def Recommendation(request):
    flavor_id = request.session.get('flavor_id')
    selected_ingredient_ids = request.session.get('selected_ingredient_ids')

    if not flavor_id:
        return redirect('Flavor')
    if not selected_ingredient_ids:
        return redirect('Ingredients')

    try:
        selected_ingredient_ids = [int(id) for id in selected_ingredient_ids]
    except ValueError:
        messages.error(request, "Invalid ingredient IDs. Please select ingredients again.")
        return redirect('Ingredients')

    selected_flavor = FlavorPreference.objects.get(id=flavor_id)
    selected_ingredients = IngredientModel.objects.filter(id__in=selected_ingredient_ids)

    products = Product.objects.filter(ProductIngredients__in=selected_ingredients, Available=True).distinct()
    products = products.annotate(
        match_count=Count('ProductIngredients', filter=Q(ProductIngredients__in=selected_ingredients))
    ).order_by('-match_count')

    context = {
        'products': products,
        'selected_flavor': selected_flavor,
        'selected_ingredients': selected_ingredients,
    }
    return render(request, 'NolisApp/Recommendation.html', context)