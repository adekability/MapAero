from fastapi import FastAPI, Request, File, UploadFile, status, Response, Form
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from db import *
from services import get_zipfile
from datetime import datetime
import uvicorn
from services import generate_color, convert_color
import os
import sys
from fastapi.staticfiles import StaticFiles
import datetime
from typing import List

os.environ['GDAL_DATA'] = os.path.join(f'{os.sep}'.join(sys.executable.split(os.sep)[:-1]), 'Library', 'share', 'gdal')
app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")
app.mount("/tiles", StaticFiles(directory="./tiles"), name="tiles")

# templates = Jinja2Templates(directory=resource_path(""))
templates = Jinja2Templates(directory="./")


@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse(
        name="main.html", context={"request": request}
    )


@app.get("/plot")
async def root(request: Request):
    records = fetch_all_records()
    dates = fetch_distinct_dates()
    context = {"request": request,
               "data": records,
               "dates": dates}
    return templates.TemplateResponse("original.html", context=context)


@app.post("/render")
async def render(request: Request,
                 tableData: str = Form(...),
                 image_files: list[UploadFile] = File(...)):
    tableData = eval(tableData)

    lat_index = tableData[0].index("Lat")
    lon_index = tableData[0].index("Lon")
    filename_index = tableData[0].index("File")
    files = {image_file.filename: await image_file.read() for image_file in image_files}
    color_str, color = generate_color()
    convert_color(color=color_str,
                  target_color=color)
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for record in range(1, len(tableData)):
        image_file = files.get(tableData[record][filename_index], None)
        if not image_file: continue
        create_record(filename=tableData[record][filename_index],
                      lat=str(float(tableData[record][lat_index])),
                      lon=str(float(tableData[record][lon_index])),
                      file=image_file,
                      color=color_str,
                      current_datetime=current_datetime)
    return RedirectResponse(request.url_for('root'),
                            status_code=status.HTTP_303_SEE_OTHER)


@app.post("/export")
async def export(request: Request):
    coordinates = await request.json()
    print(coordinates)
    records = []
    for coordinate in coordinates:
        record = get_record(lat=coordinate['lat'],
                            lon=coordinate['lon'])
        if record:
            records.append(record)

    zipfile = get_zipfile(records)
    zip_filename = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    response = Response(
        content=zipfile.read(),
        media_type="application/x-zip-compressed",
        headers={
            'Content-Disposition': f'attachment;filename=export-{zip_filename}.zip'
        }
    )
    return response


@app.get("/images/{filename}")
async def export_image(request: Request,
                       filename: str):
    image = get_image(filename=filename)
    return Response(content=image,
                    media_type="image/png")




def run_app():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
