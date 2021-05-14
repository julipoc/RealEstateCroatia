from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, IntegerField
from wtforms.validators import DataRequired


class FilterForm(FlaskForm):
    search = StringField("Search")
    county_filter = SelectField("", validators=[DataRequired(message="Choose county")],
                                choices=["Bjelovarsko-bilogorska", "Brodsko-posavska", "Dubrovačko-neretvanska", "Istarska",
                                         "Karlovačka", "Koprivničko-križevačka", "Krapinsko-zagorska", "Ličko-senjska",
                                         "Međimurska", "Osječko-baranjska", "Požeško-slavonska", "Primorsko-goranska",
                                         "Sisačko-moslavačka", "Splitsko-dalmatinska", "Šibensko-kninska", "Varaždinska",
                                         "Virovitičko-podravska", "Vukovarsko-srijemska", "Zadarska", "Zagrebačka",
                                         "Grad Zagreb"])
    quadrature_filter = IntegerField("", validators=[DataRequired(message="Add minimum required quadrature")])
    price_filter = IntegerField("", validators=[DataRequired(message="Add maximum required price")])
    property_type_filter = SelectField("", validators=[DataRequired(message="Choose property type")],
                                       choices=["House", "Apartment"])
    sale_rent = SelectField("", validators=[DataRequired()], choices=["For sale", "For rent"])
    submit = SubmitField("Search")