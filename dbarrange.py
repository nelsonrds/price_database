from mongoengine.connection import connect, disconnect
from document import Product
import json, unidecode
connect(host="mongodb+srv://nelsonrds:connect98@cluster0-lq52p.mongodb.net/mongo-dev-db?retryWrites=true&w=majority")

prd = Product.objects(tags__exists=True).count()
print(prd)
#for p in prd:
    #product = json.loads(p.get_json())
    #name = product["name"]
    #criar tags com o nome
    #text = unidecode.unidecode(name)
    #tags = text.lower().split(' ')
    #for tag in tags:
        #if len(tag) < 2:
            #tags.remove(tag)
    #print(tags)
    #p.tags = tags
    #p.save()
    
    


