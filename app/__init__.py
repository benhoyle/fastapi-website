"""Runs the webserver."""

from fastapi import FastAPI

app = FastAPI()

from app import views



