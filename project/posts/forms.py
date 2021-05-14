from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, IntegerField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class PostForm(FlaskForm):
    title = StringField("Title ", validators=[DataRequired()])
    county = SelectField("County ", validators=[DataRequired()],
                                choices=[" ", "Bjelovarsko-bilogorska", "Brodsko-posavska", "Dubrovačko-neretvanska", "Istarska",
                                         "Karlovačka", "Koprivničko-križevačka", "Krapinsko-zagorska", "Ličko-senjska",
                                         "Međimurska", "Osječko-baranjska", "Požeško-slavonska", "Primorsko-goranska",
                                         "Sisačko-moslavačka", "Splitsko-dalmatinska", "Šibensko-kninska", "Varaždinska",
                                         "Virovitičko-podravska", "Vukovarsko-srijemska", "Zadarska", "Zagrebačka",
                                         "Grad Zagreb"])
    quadrature = IntegerField("Quadrature (m2) ")
    price = IntegerField("Price (€) ")
    property_type = SelectField("Type ", validators=[DataRequired()], choices=[" ", "House", "Apartment"])
    text = TextAreaField("Text ", validators=[DataRequired()])
    sale_rent = SelectField("Sale/Rent ", validators=[DataRequired()], choices=[" ", "For sale", "For rent"])
    property_pics = MultipleFileField("Property pictures ", validators=[FileAllowed(["png", "jpg"])])
    submit = SubmitField("Post")
