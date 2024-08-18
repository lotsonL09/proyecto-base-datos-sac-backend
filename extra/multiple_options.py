from enum import Enum

class Status(Enum):
    available='Disponible'
    not_available='No disponible'
    borrowed='Prestado'

class Location(Enum):
    location_a='Oficina A'
    location_b='Oficina B'
    location_c='Oficina C'
    location_d='Oficina D'
    location_e='Oficina E'
    location_f='Oficina F'