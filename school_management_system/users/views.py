from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, DetailView, ListView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.db.models import Count
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"
