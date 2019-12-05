import json
import os
import numpy as np
from datetime import datetime
from flask import (render_template, flash, redirect, url_for, 
    request, jsonify, current_app)

from app.core import bp


def load_pets():
    pets_url = os.path.join(current_app.root_path, "static/json", "pets.json")
    return json.load(open(pets_url))

def load_hard_pets():
    pets_url = os.path.join(current_app.root_path, "static/json", "hard_sh_pets.json")
    return json.load(open(pets_url))

def load_pet_priority():
    pet_priority_url = os.path.join(current_app.root_path, "static/json", "pet_priority.json")
    return json.load(open(pet_priority_url))

def load_hard_pet_priority():
    pet_priority_url = os.path.join(current_app.root_path, "static/json", "hard_sh_pet_priority.json")
    return json.load(open(pet_priority_url))

def load_units():
    units_url = os.path.join(current_app.root_path, "static/json", "units.json")
    return json.load(open(units_url))


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@bp.route('/pets/', methods=['GET', 'POST'])
def pets():
    pet_priority = load_pet_priority()
    pets = load_pets()

    for key, item in pet_priority.items():
        pets[item]["priority"] = key
        pets[item]["KL"] = (np.ceil(np.array(pets[item]["from"])/5)*2).astype(int).tolist()

    pets_ordered = json.loads(json.dumps(dict([(pet, pets[pet]) for pet in sorted(pets, key=lambda d: int(pets[d]["priority"]))])))

    return render_template('pets.html', title='Pets', pets=pets_ordered, ceil=np.ceil)

@bp.route('/pets_hard/', methods=['GET', 'POST'])
def pets_hard():
    pet_priority = load_hard_pet_priority()
    pets = load_hard_pets()

    for key, item in pet_priority.items():
        pets[item]["priority"] = key
        pets[item]["KL"] = (50 + (np.array(pets[item]["from"])-1)*4).astype(int).tolist()

    pets_ordered = json.loads(json.dumps(dict([(pet, pets[pet]) for pet in sorted(pets, key=lambda d: int(pets[d]["priority"]))])))
    return render_template('pets_hard.html', title='Pets', pets=pets_ordered, ceil=np.ceil)

@bp.route('/units/', methods=['GET', 'POST'])
def units():
    max_rotation = 17
    max_buffs_list = [4 for i in range(1,max_rotation+1)]
    units = load_units()
    pets = load_pets()
    max_buffs = [max([len(unit["buffs"]) for key, unit in units.items() if(unit["rotation"] == i)]) for i in range(1, max_rotation+1)]
    max_buffs.reverse()
    max_buffs = np.repeat(np.array(max_buffs), max_buffs_list, axis=0)
    max_add_buffs = [max([len(pets[unit["pet"]]["additional_buffs"]) for key, unit in units.items() if(unit["rotation"] == i)]) for i in range(1, max_rotation+1)]
    max_add_buffs.reverse()
    max_add_buffs = np.repeat(np.array(max_add_buffs), max_buffs_list, axis=0)
    return render_template('units.html', title='Units', units=units, pets=pets, max_buffs=max_buffs, max_add_buffs=max_add_buffs)

@bp.route('/tickets/', methods=['GET', 'POST'])
def tickets():
    units = load_units()
    tickets_url = os.path.join(current_app.root_path, "static/json", "ticket_order.json")
    tickets = json.load(open(tickets_url))
    return render_template('tickets.html', title='Tickets', units=units, tickets=tickets)

@bp.route('/static/json/pets/<petid>.json', methods=['GET', 'POST'])
def get_pet(petid):
    pets = load_pets()
    return jsonify({"petid":petid, "pet": pets[petid.replace("_", " ")]})

@bp.route('/static/json/units/<unitid>.json', methods=['GET', 'POST'])
def get_unit(unitid):
    units = load_units()
    return jsonify(unit=units[unitid.replace("_", " ")])

@bp.route('/static/json/pet_priority.json', methods=['GET', 'POST'])
def get_priority():
    pet_priority = load_pet_priority()
    return jsonify(priority=pet_priority)

@bp.route('/static/json/hard_sh_pet_priority.json', methods=['GET', 'POST'])
def get_hard_sh_priority():
    pet_priority = load_hard_pet_priority()
    return jsonify(priority=pet_priority)

@bp.route('/meta_progression/', methods=['GET', 'POST'])
def meta_progression():   
    return render_template('meta_progression.html')
