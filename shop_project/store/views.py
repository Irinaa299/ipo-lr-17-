from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def about_author(request):
    return HttpResponse("<h1>Об авторе: Груша Ирина, студентка 2 курса </h1>")

def about_lab(request):
    return HttpResponse("<h1>Тема лабораторной: Магазин спортивных аксессуаров для подростков (рюкзаки, бутылки, браслеты)</h1>")

def main_page(request):
    return HttpResponse('''
        <h1>Главная страница</h1>
        <ul>
            <li><a href="/about-author/">Об авторе</a></li>
            <li><a href="/about-lab/">О лабораторной теме</a></li>
        </ul>
    ''')