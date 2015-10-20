from django.shortcuts import redirect, render
from django.http import HttpResponse
from todo.models import Item

def home_page(request):
    return render(request, 'home.html')

def index2(request):
    #return render(request, 'index1.html', {
    #    'new_item_text': request.POST['item_text'],
    #})
    item = Item()
    item.text = request.POST.get('item_text', '')
    item.save()

    #return render(request, 'index1.html', {
    #    'new_item_text': request.POST.get('item_text', ''),
    #})
    return render(request, 'index1.html',{'new_item_text': item.text})
    # if request.method == 'POST':
    #    return HttpResponse(request.POST['item_text'])
    # return render(request, 'index1.html')

def index3(request):
    if request.method == 'POST':
        new_item_text = request.POST['item_text']  #1
        Item.objects.create(text=new_item_text)  #2
    else:
        new_item_text = ''  #3

    return render(request, 'index1.html', {
        'new_item_text': new_item_text,  #4
    })

def index4(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    return render(request, 'index1.html')

def index1(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'index1.html', {'items': items})