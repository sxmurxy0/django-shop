from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Product


def catalog(request):
    products = Product.objects.filter(is_active=True).select_related('category')
    
    category_id = request.GET.get('category')
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)
    
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'price':
        products = products.order_by('price')
    elif sort_by == '-price':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')
    
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'current_category_id': category_id,
        'sort_by': sort_by,
        'search_query': search_query if search_query else ''
    }
    return render(request, 'catalog.html', context)

def product_detail(request, id):
    product = get_object_or_404(Product, id=id, is_active=True)
    
    similar_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'similar_products': similar_products,
        'page_title': product.name,
    }
    return render(request, 'product_detail.html', context)