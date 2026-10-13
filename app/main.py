from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import coupons, sources, admin, health
from app.db import models
from app.db.session import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='CouponHunter MVP')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.include_router(health.router, prefix='/api/health', tags=['health'])
app.include_router(coupons.router, prefix='/api/coupons', tags=['coupons'])
app.include_router(sources.router, prefix='/api/sources', tags=['sources'])
app.include_router(admin.router, prefix='/api/admin', tags=['admin'])

templates = Jinja2Templates(directory='app/templates')

from fastapi import Request

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse('index.html', { 'request': request })

@app.get('/admin')
def admin_ui(request: Request):
    return templates.TemplateResponse('admin.html', { 'request': request })
