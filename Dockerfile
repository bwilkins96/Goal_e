FROM python:3.11

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY goal_e_project goal_e_project
WORKDIR /goal_e_project

EXPOSE 8000

ENTRYPOINT [ "gunicorn" ]
CMD ["--bind", "0.0.0.0:8000", "goal_e_project.wsgi"]
