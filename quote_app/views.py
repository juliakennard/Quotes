from django.shortcuts import render, redirect
from .models import User, UserManager, Quote, QuoteManager
from django.contrib import messages
import bcrypt

## RENDER

def log_reg(request):
    return render(request, "log_reg.html")

def quotes_wall(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        "all_users": User.objects.all(),
        "all_quotes": Quote.objects.all().order_by('-created_at'),
    }
    
    return render(request, "quotes.html", context)

def profile(request, user_id):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id = user_id),
        "all_quotes": Quote.objects.all()
    }
    return render(request, "user.html", context)

def edit_profile(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        "first_name": User.objects.get(id = request.session['id']).first_name,
        "last_name": User.objects.get(id = request.session['id']).last_name,
        "email": User.objects.get(id = request.session['id']).email,
    }
    return render(request, "edit.html", context)


## LOGIN

def login(request):
    if request.method == 'POST':

        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')

        logged_user = User.objects.filter(email = request.POST['email'])
        if logged_user:
            logged_user = logged_user[0]
            request.session['id'] = logged_user.id
            request.session['first_name'] = logged_user.first_name
            request.session['last_name'] = logged_user.last_name
        
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.pw.encode()):
                return redirect('/quotes')

        return redirect('/')
    return redirect('/')

## LOGOUT

def logout(request):
    request.session.clear()
    return redirect('/')

## CREATE

def create_user(request):
    if request.method == 'POST':

        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')

        user_pw = request.POST['pw']
        hash_pw = bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            pw = hash_pw
        )
        request.session['id'] = new_user.id
        request.session['first_name'] = new_user.first_name
        request.session['last_name'] = new_user.last_name
        return redirect('/quotes')
    
    return redirect('/')

## POST

def create_quote(request):
    if request.method == 'POST':

        errors = Quote.objects.quote_validator(request.POST)
        if len(errors) > 0:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/quotes')

        Quote.objects.create(
                quote = request.POST['quote'],
                author = request.POST['author'],
                user = User.objects.get(id = request.session['id'])
            )
        return redirect('/quotes')
    return redirect('/quotes')

## DELETE 

def delete_quote(request, quote_id):
    Quote.objects.get(id = quote_id).delete()
    return redirect('/quotes')

## EDIT

def edit_user(request):
    if request.method == 'POST':

        errors = User.objects.update_validator(request.POST)
        if len(errors) > 0:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/edit/{{request.session.id}}')

        user_to_update = User.objects.get(id = request.session['id'])

        user_to_update.first_name = request.POST["first_name"]
        user_to_update.save()

        user_to_update.last_name = request.POST["last_name"]
        user_to_update.save()

        user_to_update.email = request.POST["email"]
        user_to_update.save()

        request.session["first_name"] = user_to_update.first_name
        request.session["last_name"] = user_to_update.last_name
        request.session["email"] = user_to_update.email
        request.session["id"] = user_to_update.id

        return redirect('/quotes')

def like(request, quote_id):
    user = User.objects.get(id = request.session['id'])
    quote = Quote.objects.get(id = quote_id)
    user.liked_quotes.add(quote)
    return redirect('/quotes')