#from typing import runtime_checkable
import PySimpleGUI as sg
import recommend as expert
from math import sqrt

window = sg.Window('Welcome', layout=[
                                [sg.Text(" Hello there! \n\n This is a laptop-recommendation service designed to personally help you find\n the right laptop that fits your needs.\n",
                                        font=("Helvetica", 20), pad = (10,10,10,10))],
                                [sg.Text(" Before we dive into the details, what's your name?", font = ("Helvetica", 20), pad = (10, 0, 10, 10))],
                                [sg.InputText(key='name', font = ("Helvetica", 20), pad = (10, 0))],
                                [sg.Button('Next', size = (10,3))]
                            ],
                    size=(1000,500))
_, values = window.read()

layout = [
    [sg.Text(' Welcome, ' + str(values['name']) + ", we hope we can help you find the kind of laptop you want.", 
        font = ("Helvetica", 20), pad = (10,10,10,10))],
    [sg.Text(' Your usage:', font = ("Helvetica", 20), pad = (10,10,10,10))],
    [
        sg.Radio("Gaming","RADIO1", default= True, key="-gaming-", font = ("Helvetica", 16)),
        sg.Radio("Advanced Projects",  "RADIO1", default= False, key="-advanced-", font = ("Helvetica", 16)),
        sg.Radio("Office/School work", "RADIO1", default= False, key="-work-", font = ("Helvetica", 16)),
        sg.Radio("Light Usage/General Documentation", "RADIO1", default= False, key="-light-", font = ("Helvetica", 16)),
        sg.Radio("Other/Unspecified", "RADIO1", default= False, key="-other-", font = ("Helvetica", 16))
    ],
    [
        sg.Text(' Your preferred brand:', font = ("Helvetica", 20), pad = (10,10,10,10)),
        sg.Checkbox("Apple", default=True, key="-apple-", font = ("Helvetica", 16)),
        sg.Checkbox("Acer", default=True, key="-acer-", font = ("Helvetica", 16)),
        sg.Checkbox("Asus", default=True, key="-asus-", font = ("Helvetica", 16)),
        sg.Checkbox("Alienware", default=True, key="-alienware-", font = ("Helvetica", 16)),
        sg.Checkbox("Dell", default=True, key="-dell-", font = ("Helvetica", 16)),
        sg.Checkbox("HP", default=True, key="-hp-", font = ("Helvetica", 16)),
        sg.Checkbox("Lenovo", default=True, key="-lenovo-", font = ("Helvetica", 16)),
        sg.Checkbox("Microsoft", default=True, key="-microsoft-", font = ("Helvetica", 16))
    ],
    [
        sg.Text(' Your preferred screen size:', font = ("Helvetica", 20), pad = (10,10,10,10)),
        sg.Checkbox("10.1~13.0", default=True, key="-small-", font = ("Helvetica", 16)),
        sg.Checkbox("13.0~15.0", default=True, key="-median-", font = ("Helvetica", 16)),
        sg.Checkbox("15.0~17.6", default=True, key="-large-", font = ("Helvetica", 16))
    ],
    [
        sg.Text(' Your preferred weight:', font = ("Helvetica", 20), pad = (10,10,10,10)),
        sg.Checkbox("<= 1.5kg", default=True, key="-light-", font = ("Helvetica", 16)),
        sg.Checkbox("1.5~2.0kg", default=True, key="-average-", font = ("Helvetica", 16)),
        sg.Checkbox(">=2kg", default=True, key="-heavy-", font = ("Helvetica", 16))
    ],
    [
        sg.T(" Your budget(range from 2000 ~ 20000, generally around 5000):", key="lbl_a", font="Helvetica 20"),
        sg.I("0", key="edit_a", font="Helvetica 20", pad=(10, 10)),
    ],
    [sg.B("Find", key="find", border_width=5, pad=(10, 10), size=(200, 2))],
    [
        sg.Multiline(
            "", size=(1300, 25), font="Helvetica 14", disabled=True, key="-multiline-"
        )
    ],
]

window = sg.Window("Laptop recommender", layout, size=(1200, 600))

while True:
    event, values = window.read()
    rules = expert.import_rules()
    facts = expert.import_facts()

    purpose = ""
    brand = []
    screen_size = []
    weight = [999,0]

    if (values["-gaming-"] == True):
        purpose = "Gaming"
    if (values["-advanced-"] == True):
        purpose = "Advanced Projects"
    if (values["-work-"] == True):
        purpose = "Office/School work"
    if (values["-light-"] == True):
        purpose = "Light Usage/General Documentation"
    if (values["-other-"] == True):
        purpose = "Other/Unspecified"
    
    if (values["-apple-"] == True):
        brand.append("Apple")
    if (values["-acer-"] == True):
        brand.append("Acer")
    if (values["-asus-"] == True):
        brand.append("Asus")
    if (values["-alienware-"] == True):
        brand.append("Alienware")
    if (values["-dell-"] == True):
        brand.append("Dell")
    if (values["-hp-"] == True):
        brand.append("HP")
    if (values["-lenovo-"] == True):
        brand.append("Lenovo")
    if (values["-microsoft-"] == True):
        brand.append("Microsoft")
    
    if (values["-small-"] == True):
        screen_size.append(10.1)
        screen_size.append(11.0)
        screen_size.append(11.6)
        screen_size.append(12.0)
        screen_size.append(12.3)
    if(values["-median-"] == True):
        screen_size.append(13.3)
        screen_size.append(13.5)
        screen_size.append(14.0)
    if(values["-large-"] == True):
        screen_size.append(15.0)
        screen_size.append(15.5)
        screen_size.append(15.6)
        screen_size.append(17.3)
        screen_size.append(17.6)

    if(values["-light-"] == True):
        weight[0] = min(weight[0], 0)
        weight[1] = max(weight[1], 1.5)
    if(values["-average-"] == True):
        weight[0] = min(1.5, weight[0])
        weight[1] = max(2.0, weight[1])
    if(values["-heavy-"] == True):
        weight[0] = min(weight[0], 2.0)
        weight[1] = max(weight[1], 999)
    
    budget = int(values['edit_a'])

    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    if event == "find":
        try:
            result = ""
            index_result = expert.recommend(rules, facts, purpose, budget, brand, screen_size, weight)
            for idx in index_result:
                result = result + "brand:" + facts[idx]["brand"] + "\tmodel:" + facts[idx]["model"] + "\t\t\tprice:" + str(facts[idx]["price"]) + "\n"
            text_elem = window["-multiline-"]
            text_elem.update(result)

        except:
            sg.popup_error("Some error happened!")
            break

window.close()
