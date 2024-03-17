
from aplication.api.middlewares import middleware
from flask import request, jsonify, render_template,make_response
from infrastructure.exceptions import ApiError
import re,json
class TraslateRoutes:
    def __init__(self, app):
        self.app = app
        
        @self.app.route('/subtitles', methods=['POST'])
        @middleware
        def send_subtitles():
            data = json.dumps(request.form)
            data = json.loads(data)
            print(str(data),str(type(data)))
            name = data['content']
            print(str(name),str(type(name)))
            with open(f'./static/video/{name}.txt') as file:
                content = file.read()
            dict_result = {}
            def to_ms(tiempo):
                hours = int(tiempo[0]) * 3600000
                minutes = int(tiempo[1]) * 60000
                seconds = int(tiempo[2]) * 1000
                miliseconds = seconds + minutes + hours
                miliseconds += int(tiempo[2]) % 1000
                miliseconds += int(tiempo[3])
                return miliseconds
            def process_match(obj_match):
                
                obj = obj_match.groups()[0]
                print("OBJf-- ",str(obj))
                obj = obj.split(sep="\n")
                print("OBJf-- ",str(obj))
                time = obj[1].split(sep=" --> ")
                time = time[1].replace(",",":")
                time = time.split(":")
                new_list = []
                for i in time:
                    new_list.append(str(int(i)))
                time = ":".join(new_list)
                time = to_ms(new_list)
                dict_obj ={"end":time,"data":obj[2]}
                dict_result[obj[0]] = dict_obj
                print("-----")
                return str(obj)
            #print("DICT:: ",dict_result)
            patron = r'([0-9]{1,2}\n[0-9][0-9]:[0-9][0-9]:[0-9][0-9],[0-9][0-9][0-9]\s-->\s[0-9][0-9]:[0-9][0-9]:[0-9][0-9],[0-9][0-9][0-9]\n[\w\s]*?[^\n]*)'
            result = re.subn(patron, process_match,content)
            #print("RES:: ",result)
            if "return" in data.keys():
                ret = data['return']
                context = {"video":str(name)}
                return render_template(f'{ret}.html',video={"title":name,"subtitles":dict_result})
                #return jsonify(context)
            return jsonify({"res":dict_result})