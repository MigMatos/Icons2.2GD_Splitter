import json
from PIL import Image
import plistlib

async def parse_new_icons(form,id):
    gamesheet_cache = ""
    path = 'api/new_icons/'
    try:
        file = f"{form}_{id}-hd"
        file_path = f"{path}{file}.plist"
        with open(file_path, 'rb') as f:
            tpl = plistlib.load(f)
    except:
        file = f"{form}_01-hd"
        file_path = f"{path}{file}.plist"
        id = "01"
        with open(file_path, 'rb') as f:
            tpl = plistlib.load(f)
    frames = list(tpl['frames'])
    json_data = []
    for datas in frames:
        gamesheet_cache = f'"{datas}":'+"{\n"+f'"spriteOffset":[{tpl["frames"][datas]["spriteOffset"][1:-1]}],'+f'\n"spriteSize":[{tpl["frames"][datas]["spriteSize"][1:-1]}],'
        gamesheet_cache = gamesheet_cache+f'\n"spriteSourceSize":[{tpl["frames"][datas]["spriteSourceSize"][1:-1]}],'
        gamesheet_cache_r = f'\n"textureRect":{tpl["frames"][datas]["textureRect"]},'
        gamesheet_cache_r = gamesheet_cache_r.replace("{","[")
        gamesheet_cache_r = gamesheet_cache_r.replace("}","]")
        gamesheet_cache = gamesheet_cache + gamesheet_cache_r
        gamesheet_cache = gamesheet_cache+f'\n"textureRotated":"{tpl["frames"][datas]["textureRotated"]}"'+"},\n"
        json_data.append(gamesheet_cache)
        gamesheet_cache = ""
        gamesheet_cache_r = ""
    txt_final = ""
    for i in range(len(json_data)):
        txt_final = txt_final + json_data[i]
    txt_final = "{\n" + txt_final + txt_final[:-2] + "\n}"
    data_sheet = json.loads(txt_final)
    path_cache = "api/cache_new_icons/"
    for file_sheet in list(data_sheet):
        file_path = f"{path}{file}.png"
        try:
            file_cache = open(f'{path_cache}{file_sheet}')
            file_cache.close()
            break
        except:
            img_sheet = Image.open(file_path)
            data = data_sheet[file_sheet]["textureRect"]
            rotated_bool = data_sheet[file_sheet]["textureRotated"]
            if rotated_bool == "True":area = (data[0][0],data[0][1],data[0][0]+data[1][1],data[0][1]+data[1][0])
            else:area = (data[0][0],data[0][1],data[0][0]+data[1][0],data[0][1]+data[1][1])
            img_sheet = img_sheet.crop(area)
            if rotated_bool == "True":img_sheet=img_sheet.rotate(90,expand=True)
            img_sheet = img_sheet.convert("RGBA")
            img_sheet.save(f"{path_cache}{file_sheet}","PNG")
    return data_sheet,id