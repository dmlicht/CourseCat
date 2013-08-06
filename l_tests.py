# (1) testing the models/databases

from coursecat.models import *
import fill_test_db

english_category = Topic.query.all()[0]
english_101 = Course.query.all()[0]

print english_101.topics
print english_category.courses

english_101.topics.append(english_category) #works!
db.session.commit()

english_category.courses 
english_cat_fromquery = Topic.query.filter_by(name="english").first()
english_cat_fromquery.courses  ## PERFECT!



