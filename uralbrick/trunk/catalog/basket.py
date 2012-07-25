# -*- coding: utf-8 -*-
import json
from models import Product, Pricing

class Basket:
    session = None
    
    def __init__(self, session):
        if session.get('basket') is None:
            session['basket'] = "{}"
        self.session = session
    
    def _get_key(self, product_id, size_id=0):
        """
        Creates key for basket item.
        Key for basket item is the string of "product_id:size_id"
        """
        #return str(product_id) + ':' + str(size_id)
        return str(product_id)
    
    def _get_ids(self, key):
        """
        Returns product id and size id for given key
        """
        #product_id, size_id = key.split(':')
        #return (int(product_id), int(size_id))
        return int(key)
    
    def _save(self, obj):
        """
        Serializes and saves the basket into session
        """
        result = json.dumps(obj)
        self.session['basket'] = result
        return result
    
    def _load(self):
        """
        Loads basket from session and deserializes it
        """
        string = self.session['basket']
        return json.loads(string)

    
    #
    # Adding, deleting and changing basket items
    #
            
    def _change_count(self, product_id, size_id=0, count=1):
        """
        Adds or delete the Product (optionally with its Size) to basket (-/+ 1)
        """
        
        size_id = int(size_id)
        
        # Checking if given product and size (if specified) are exist
        # It will throw an exception if no product/size exist
        product = Product.objects.get(pk=product_id)
        if size_id:
            size = product.sizes.get(pk=size_id) 
        else:
            size = None
            
        del product
        del size

        # Getting basket contents
        basket = self._load()

        # Key for basket item is the string of "product_id:size_id"
        key = self._get_key(product_id, size_id)
        
        # Checking if this combination is already exist in basket
        if count > 0:
            if key in basket:
                if type(basket[key]) is list:
                    # Items with sizes: adding an item to the list
                    basket[key].append(size_id)
                else:
                    # Items w/o sizes: adding count
                    basket[key] = int(basket[key]) + 1
            else:
                # Creating new record
                if size_id:
                    basket[key] = [size_id]
                else:
                    basket[key] = 1
        
        elif count < 0:
            if key in basket:
                if type(basket[key]) is list:
                    index = basket[key].index(size_id)
                    del basket[key][index]
                else:
                    basket[key] -= 1
                if not basket[key]:
                    del basket[key]
        else:
            pass
        
        # Saving the basket
        self._save(basket)
        
        if not basket.get(key):
            return 0
        elif type(basket[key]) is list:
            return len(basket[key])
        else:
            return basket[key]
    
    def add(self, product_id, size_id=0):
        """ Adds one position with given size """
        return self._change_count(product_id, size_id, 1)
        
    def delete(self, product_id, size_id=0):
        """ Deletes one position with given size """
        return self._change_count(product_id, size_id, -1)
            
    def change_size(self, product_id, old_size_id, new_size_id):
        """
        Changes the size for given product.
        Assumes that:
        - item with key product:OLD_size DOES exist in basket.
        - item with key product:NEW_size DOES NOT exist in basket.
        """
        
        product_id = int(product_id)
        old_size_id = int(old_size_id)
        new_size_id = int(new_size_id)
        
        # Checking for existance
        product = Product.objects.get(pk=product_id)
        old_size = product.sizes.get(pk=old_size_id)
        new_size = product.sizes.get(pk=new_size_id)
        del product
        del old_size
        del new_size
        
        # Getting basket contents
        basket = self._load()

        key = self._get_key(product_id, old_size_id)
        index = basket[key].index(old_size_id)
        
        # Changing key
        basket[key][index]  = new_size_id
        
        # Saving 
        self._save(basket)
        return basket
    
#    def delete(self, product_id, size_id=0):
#        """
#        Deletes basket item
#        """
#        # ... Checking for product / size existance is not neccessary
#        # ... because it could not be added to basket
#        basket = self._load()
#        key = self._get_key(product_id, size_id)
#        if key in basket:
#            del basket[key]
#        self._save(basket)
#        
#        return basket
    
    def clear(self):
        """
        Clears whole user basket
        """
        self._save({})
    
    
    #
    # Basket items lists, properties and summaries
    #
    
    def _get_price(self, product, size):
        """
        Calculates the price for the product by its size 
        """
        if size is None:
            return product.discounted()
        else:
            pricing = Pricing.objects.get(product=product, size=size)
            return pricing.discounted()
    
    def _get_item(self, product_id, size_id, count):
        """
        Returns extended basket item with information about price, summary, sizes, etc. 
        """
        product = Product.objects.get(pk=product_id)
        if size_id:
            size = product.sizes.get(pk=size_id)
        else:
            size = None
        price = self._get_price(product, size)

        count = int(count)
                    
        return {
            '0': product.id, # dirty hack for sorting by product ID...
            '1': size_id, # ... and then by its size
            'product': product,
            'count': count,
            'price': price,
            'summary': price * count,
            'url': product.section.path + product.slug,
            'current_size_id': size_id,
            'sizes_list': product.sizes.all(),
            'pricing_list': Pricing.objects.filter(product=product)
        }
    
    def get_list(self):
        """
        Returns list of basket items with extended information
        """
        
        basket = self._load()
        result = []
        
        for key, val in basket.iteritems():
            if type(val) is list:
                for size_id in val:
                    item = self._get_item(key, size_id, 1)
                    result.append(item)
            else:
                item = self._get_item(key, 0, val)
                result.append(item)
        
        result.sort()
        return result 
    
    def get_count(self, product_id):
        """
        Returns count of basket item with given product_id (any sizes)
        """
        basket = self._load()
        key = self._get_key(product_id)

        if not basket.get(key):
            return 0
        if type(basket[key]) is list:
            return len(basket[key])
        else:
            return int(basket[key])
    
    def get_summary_info(self):
        """
        Returns summary price and count of all items in basket
        """
        basket = self._load()
        summary_count = 0
        summary_price = 0
        
        for key, val in basket.iteritems():
            if type(val) is list:
                product = Product.objects.get(pk=key)
                for size_id in val:
                    size = product.sizes.get(pk=size_id)
                    price = self._get_price(product, size)
                    summary_price += price 
                summary_count += len(val)
            else:
                count = val
                product = Product.objects.get(pk=key)
                price = self._get_price(product, None)
                summary_price += int(count) * price 
                summary_count += int(count)
                
        return { 
            'summary_count': summary_count, 
            'summary_price': summary_price 
        } 
