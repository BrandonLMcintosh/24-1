from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from forms import PetForm
from models import connect_db, db, Pet

app = Flask(__name__)

app.debug = True

app.create_jinja_environment()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'SuperSecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.drop_all()
db.create_all()

debug = DebugToolbarExtension(app)

@app.route('/')
def pets_list():
    """Render list of pets in DB"""

    title = "Pets"
    pets = Pet.query.all()
    return render_template('pets/list.html.j2', pets=pets, title=title)


@app.route('/add', methods=["GET", "POST"])
def pets_add():
    """Render view for adding a pet"""

    title = "Add Pet"
    form = PetForm()
    if request.method == "GET":
        #Do stuff
        return render_template("pets/add.html.j2", form=form, title=title)
    elif request.method == "POST":
        if form.validate_on_submit():

            name = form.name.data
            species = form.species.data 
            photo_url = form.photo_url.data if form.photo_url.data else None
            age = form.age.data if form.age.data else None
            notes = form.notes.data if form.notes.data else None

            pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)

            db.session.add(pet)
            db.session.commit()

            flash(f'{pet.name} has been successfully added!')

            return redirect("/")

        else:

            form.flash_errors()
            
            return render_template('pets/add.html.j2', form=form, title=title)
    else:

        return redirect("/")


@app.route('/<int:pet_id>')
def pets_get(pet_id):
    """View a specific pet"""

    pet = Pet.query.get_or_404(pet_id)

    return render_template('pets/get.html.j2', pet=pet, title=pet.name)


@app.route('/<int:pet_id>/edit', methods=["GET", "POST"])
def pets_edit(pet_id):
    """
    GET: Renders edit pet view
    POST: Sends data back to DB to edit referenced pet
    """

    pet = Pet.query.get_or_404(pet_id)
    title = "Edit Pet: " + pet.name
    form = PetForm()

    form.name.data = pet.name
    form.species.data =  pet.species
    form.photo_url.data = pet.photo_url
    form.age.data = pet.age
    form.notes.data = pet.notes

    if request.method == "GET":
        
        return render_template("pets/edit.html.j2",pet=pet, form=form, title=title)

    elif request.method == "POST":

        if form.validate_on_submit():

            pet.name = form.name.data
            pet.species = form.species.data
            pet.photo_url = form.photo_url.data if form.photo_url.data else None
            pet.age = form.age.data if form.age.data else None
            pet.notes = form.notes.data if form.notes.data else None

            db.session.add(pet)
            db.session.commit()
            
            flash(f'{pet.name} successfully updated.')

            return redirect("/")

        else:

            form.flash_errors()

            return render_template('pets/edit.html.j2', form=form, title=title)

    else:

        return redirect("/")


@app.route('/<int:pet_id>/adopt')
def pets_adopt(pet_id):
    """Simple function for adopting a pet. Runs instance function that sets available to false."""

    pet = Pet.query.get_or_404(pet_id)

    pet.adopt()

    return redirect('/')


@app.route('/<int:pet_id>/delete')
def pets_delete(pet_id):
    """Deletes a pet from the DB"""

    pet = Pet.query.get_or_404(pet_id)

    db.session.delete(pet)
    db.session.commit()

    return redirect('/')