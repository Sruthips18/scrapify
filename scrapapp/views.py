from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Sum 
from django.http import HttpResponseRedirect
from django.urls import reverse
from scrapapp.forms import RegistrationForm,LoginForm,UserProfileForm,ScrapForm,CategoryForm,BidsForm
from django.views.generic import View,FormView,CreateView,TemplateView,UpdateView,DetailView,ListView
from django.contrib.auth import authenticate,login,logout
from scrapapp.models import UserProfile,Scrap,Category,Wishlist,Bids
from django.contrib import messages
from django.utils.decorators import method_decorator

def signin_requires(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('sign-in')
        else:
            return fn(request,*args,**kwargs)
    return wrapper

class RegistrationView(CreateView):
    template_name='register.html'
    form_class=RegistrationForm

    def get_success_url(self):
        return reverse('sign-in')

class SignInView(FormView):
    template_name='login.html'
    form_class=LoginForm
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password')
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                messages.success(request,'Login successfully done')
                return redirect('home')
        messages.error(request,'failed to login')
        return render(request,'login.html',{'form':form})

@method_decorator(signin_requires,name='dispatch')
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('sign-in')

@method_decorator(signin_requires,name='dispatch')
class HomeView(ListView):
    template_name='home.html'
    form_class=ScrapForm
    model=Scrap
    context_object_name='data'

    def get_success_url(self):
        return reverse('home')
    
    def get_queryset(self):
        # Exclude scraps added by the current logged-in user
        return Scrap.objects.exclude(user=self.request.user)

@method_decorator(signin_requires,name='dispatch')
class ProfileUpdateView(UpdateView):
    template_name='update_profile.html'
    form_class=UserProfileForm
    model=UserProfile
    
    def get_success_url(self):
        return reverse('home')
   
@method_decorator(signin_requires,name='dispatch')
class ProfileDetailsView(DetailView):
    template_name='profile_details.html'
    model=UserProfile
    context_object_name='data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_items = Scrap.objects.filter(user=self.request.user)
        context['user_items'] = user_items
        return context
    
class ScrapAddView(CreateView):
    template_name='add_scrap.html'
    form_class=ScrapForm
    model=Scrap
    context_object_name='data'
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('home')
        
@method_decorator(signin_requires,name='dispatch')
class ScrapUpdateView(UpdateView):
    template_name='update_scrap.html'
    form_class=ScrapForm
    model=Scrap
    print('updated')
    def get_success_url(self):
        return reverse('home')

@method_decorator(signin_requires,name='dispatch')
class ScrapDetailView(DetailView):
    template_name='Scrap_details.html'
    model=Scrap
    context_object_name='detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scrap = self.get_object()
        bid_item = scrap.scrap_bids.all()  # Check the related_name, e.g., 'bids_set'
        context['bid_item'] = bid_item
        context['wishlist_toggle_url'] = reverse('wishlist_toggle', args=[self.object.id])
        context['bids_url'] = reverse('bids', args=[self.object.id])
        return context

@method_decorator(signin_requires,name='dispatch')
class ScrapDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk') 
        Scrap.objects.get(id=id).delete()
        messages.success(request,"Scrap deleted successfully")
        return redirect('home')
    
@method_decorator(signin_requires,name='dispatch')
class WishlistView(View):
    def get(self, request, scrap_id):
        scrap = get_object_or_404(Scrap, pk=scrap_id)
        if request.user.is_authenticated:
            user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
            wishlist_items = user_profile.wishlists.all()
            total_price = wishlist_items.aggregate(total_price=Sum('price'))['total_price'] or 0          

        return render(request, 'cart.html', { 'scrap': scrap,
                                              'wishlist_items': wishlist_items,  # Pass wishlist items to context
                                              'total_price':total_price
        } )
    
    def post(self, request, scrap_id):
        scrap = get_object_or_404(Scrap, pk=scrap_id)
        if request.user.is_authenticated:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            if scrap not in user_profile.wishlists.all():
                user_profile.wishlists.add(scrap)
        return HttpResponseRedirect(reverse('wishlist_toggle', kwargs={'scrap_id': scrap_id}))

@method_decorator(signin_requires,name='dispatch')
class WishlistProductsView(View):
    def get(self, request):
        wishlist_items = []
        if request.user.is_authenticated:
            user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
            wishlist_items = user_profile.wishlists.all()
        return render(request, 'cart_products.html',{'wishlist_items': wishlist_items} )
    
@method_decorator(signin_requires,name='dispatch')
class WishlistDeleteView(View):
    def get(self,request,pk):
        scrap=get_object_or_404(Scrap,pk=pk)
        if request.user.is_authenticated:
            user_profile=request.user.profile
            user_profile.wishlists.remove(scrap)
            messages.error(request,'Cart item Deleted')
            return redirect('home')

@method_decorator(signin_requires,name='dispatch')
class BidsAddView(CreateView):
    form_class=BidsForm
    template_name='Scrap_details.html'

    def form_valid(self, form):
       scrap_id = self.kwargs.get('scrap_id')
       scrap = Scrap.objects.get(pk=scrap_id)
       user = self.request.user
       form.instance.scrap = scrap
       form.instance.user = user
       return super().form_valid(form)
    
    def get_success_url(self):
        # scrap_id = self.kwargs.get('scrap_id')
        # return reverse('home', kwargs={'pk': self.kwargs['scrap_id']})
        return reverse('home')

@method_decorator(signin_requires,name='dispatch')  
class BidsListView(ListView):
    template_name='bids_list.html'
    form_class=BidsForm
    model=Bids
    context_object_name='data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bids_items=Bids.objects.filter(user=self.request.user)
        context['bids_items'] = bids_items 
        if not bids_items.exists():
            context['no_bids'] = True
        return context

@method_decorator(signin_requires,name='dispatch')
class BidsDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk') 
        Bids.objects.get(id=id).delete()
        messages.success(request,"Bids deleted successfully")
        return redirect('home')

@method_decorator(signin_requires,name='dispatch')
class BidRequestView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        scrap = Scrap.objects.get(id=id)
        bids = scrap.scrap_bids.all()
        return render(request,'bidrequest.html',{'scrap': scrap,
                                                  'bids': bids,})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        action=request.POST.get("action")
        if action=="accept":
            Bids.objects.filter(id=id).update(status="Accept")
            messages.success(request, 'Bid request accepted!')
        elif action=="reject":
            Bids.objects.filter(id=id).update(status="Reject")
            Bids.objects.filter(id=id).delete()
            messages.success(request, 'Bid request rejected')
        return redirect("home")

