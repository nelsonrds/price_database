import datetime
import unidecode

from bson.objectid import ObjectId
from flask import (
    Blueprint, render_template, request, make_response, json, session, g
)

from .auth import login_required, protected
from .document import Product, User

bp = Blueprint('product', __name__)


@bp.route('/')
@login_required
def index():
    product_list = []
    product_hist = []
    if session["url"] is not None:
        url = session["url"]
        list_url = []
        for _id in url:
            list_url.append(ObjectId(_id))
        find_qry = {"_id": {"$in": list_url}}
        products2 = Product.objects(__raw__=find_qry)

        # for url_id in list_url:
        products2 = dict([(obj.id, obj) for obj in products2])
        sorted_objects = [products2[id] for id in list_url]           

    # products = Product.objects()[:16]

    products = g.user["product"]

    for product in products:
        product_list.append({
            "id": product.id,
            "name": product.name,
            "image": product.url_img,
            "sub_title": product.sub_title,
            "price": product.prices[-1].price,
            "price_was": product.prices[-1].price_was
        })

    for product in reversed(sorted_objects):
        if product in products:
            exist = True
        else:
            exist = False
        product_hist.append({
            "id": product.id,
            "name":product.name,
            "image": product.url_img,
            "sub_title": product.sub_title,
            "price": product.prices[-1].price,
            "price_was": product.prices[-1].price_was,
            "exist": exist
        })

    context = {
        "product_list": product_list,
        "product_hist": product_hist
    }

    res = make_response(render_template('product/product.html', context=context))

    return res


@bp.route('/product_list')
@login_required
def product_list():
    products_list = []
    products = Product.objects()[:50]
    for product in products:
        products_list.append({
            "id": product.id,
            "name": product.name,
            "sub_title": product.sub_title,
            "sub_sub_title": product.sub_sub_title,
            "company": product.company,
            "creation_date": product.date_created,
            "is_deleted": product.is_deleted
        })

    return make_response(render_template('product/product_list.html', products_list=products_list))


@bp.route('/product/<id>', methods=["GET"])
@login_required
def product(id):
    product_out = {}
    if request.method == "GET":
        prd = Product.objects(id=id)
        user = g.user
        if user:
            if prd.first() in user["product"]:
                product_out["exist"] = True
        else:
            product_out["exist"] = False
        if prd:
            prod = prd.first()
            product_out["id"] = str(prod.id)
            product_out["name"] = prod.name
            product_out["image"] = prod.url_img
            product_out["sub_title"] = prod.sub_title
            product_out["price_list"] = []
            product_out["month"] = datetime.datetime.now().strftime("%B")
            for price in prod.prices:
                price_out = price.price.replace('€', '').replace('/un', '').replace(',', '.')
                date_out = price.date_created.strftime('%d')
                product_out["price_list"].append({"price": price_out, "date": date_out.lstrip("0")})
                product_out["price"] = price.price
                product_out["price_was"] = price.price_was

    res = make_response(render_template('product/product_info.html', product=product_out))
    
    if session["url"] is None:
        session["url"] = []

    if str(id) not in session["url"]:
        session["url"].append(str(id))
    else:
        session["url"].remove(str(id))
        session["url"].append(str(id))
    if len(session["url"]) > 8:
        session["url"].remove(session["url"][0])
    
    session.modified = True

    return res


@bp.route('/search', methods=['GET'])
@login_required
def search():
    text = ""
    number_results = 0
    prd_list = []
    if request.args:
        text = request.args.get('text')
        text_in = unidecode.unidecode(text)
        tags = text_in.lower().split(' ')
        
        list_tags = []
        for tag in tags:
            list_tags.append({
                "tags": {'$regex': tag}
            })
        qry = {'$and': list_tags}

        if request.args.get('order'):
            product_list = Product.objects(__raw__=qry).order_by(request.args.get('order'))
        else:
            product_list = Product.objects(__raw__=qry)
        
        number_results = Product.objects(__raw__=qry).count()
        for prd in product_list:
            if prd in g.user["product"]:
                exist = True
            else:
                exist = False
            prd_list.append({
                "id": prd.id,
                "name": prd.name,
                "company": prd.company,
                "image": prd.url_img,
                "sub_title": prd.sub_title,
                "price": prd.prices[-1].price,
                "price_was": prd.prices[-1].price_was,
                "exist": exist
            })

    context = {
        "search_text": text,
        "number_results": number_results,
        "product_list": prd_list,
        "product_search_link": request.full_path.split('&')[0]
    }

    res = make_response(render_template('product/product_search.html', context=context))

    return res


@bp.route('/product/<id>', methods=['POST', 'DELETE'])
@protected
def product_follow(id):
    message = ""
    error = False
    if request.method == "POST":
        prd = Product.objects(id=id)
        if prd:
            prod = prd.first()
            user = User.objects(id=g.user["id"]).first()
            if prod not in user["product"]:
                user["product"].append(prod)
                user.save()
                message = "Product added!"
                error = False
            else:
                message = "Product already on the list"
                error = True

    if request.method == "DELETE":
        prd = Product.objects(id=id)
        if prd:
            prod = prd.first()
            user = User.objects(id=g.user["id"]).first()
            if prod in user["product"]:
                user["product"].remove(prod)
                user.save()
                message = "Product removed!"
                error = False
            else:
                message = "Product not on the list"
                error = True

    return json.dumps({
        "message": message,
        "error": error
    })


@bp.route('/api/test')
@protected
def api_test():
    return json.dumps({
        "name": "nelson",
        "last_name": "rodrigues"
    })