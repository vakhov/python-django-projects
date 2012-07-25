# -*- coding: utf-8 -*-
from models import Position

class Basket:

    session = None

    def __init__(self, session):
        if session.get('basket') is None:
            session['basket'] = {}
        self.session = session

    def _get_position(self, position_id):
        # Position must have "price" attribute!        
        return Position.objects.get(pk=position_id)

    def add(self, position_id, count):
        if self.session['basket'].get(position_id) is None:
            self._get_position(position_id) # Check if position exist
            self.session['basket'][position_id] = 1
        else:
            self.session['basket'][position_id] += 1
        return self.session['basket'][position_id]
    
    def delete(self, position_id, count):
        if self.session['basket'].get(position_id) is None:
            return 0
        elif self.session['basket'][position_id] == 0:
            return 0
        else:
            self.session['basket'][position_id] -= 1
        return self.session['basket'][position_id]

    def clear(self):
        self.session['basket'] = {}
    
    def order(self, request):
        # Проверяем заполнение формы
        fields = ('r_autor', 'r_cont', 'r_mes')
        empty_fields = []
        for field in fields:
            if not request.POST.get(field):
                empty_fields.append(field)
        # Если есть ошибки, возвращаем ошибки
        if empty_fields:
            return empty_fields
        # Если все ок, то:
        else:
            # Сохраняем заказ в БД
            self._save_order(request)
            # Отправляем письмо
            self._send_mail(request)
            return False

    def position_count(self, position_id):
        if self.session['basket'].get(position_id) is None:
            return 0
        else:
            return self.session['basket'][position_id]
    
    def position_info(self, position_id):
        if self.session['basket'].get(position_id):
            return { 
                'count': self.session['basket'][position_id],
                'sum': self._get_position(position_id).price_rozn * self.session['basket'][position_id]
            }
        else:
            return { 'count': 0, 'sum': 0 }

    def list(self):
        result = {}
        for position_id in self.session['basket'].keys():
            info = self.position_info(position_id)
            info['position'] = self._get_position(position_id)
            result[position_id] = info
        return result

    def get_summary_info(self):
        result = { 
            'summary_count': 0, 
            'summary_price': 0 
        }
        for position_id in self.session['basket'].keys():
            info = self.position_info(position_id)
            result['summary_count'] += info['count']
            result['summary_price'] += info['price']
        return result