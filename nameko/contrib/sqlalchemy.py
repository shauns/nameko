from __future__ import absolute_import

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from nameko.dependencies import AttributeDependency


class ORMSession(AttributeDependency):
    def __init__(self, declarative_base):
        self.declarative_base = declarative_base
        self.sessions = {}

    def acquire_injection(self, worker_ctx):
        service_name = worker_ctx.srv_ctx.name
        decl_base_name = self.declarative_base.__name__
        uri_key = '{}:{}'.format(service_name, decl_base_name)

        db_uris = worker_ctx.config['orm_db_uris']
        db_uri = db_uris[uri_key].format({
            'service_name': service_name,
            'declarative_base_name': decl_base_name,
        })

        engine = create_engine(db_uri)
        Session = sessionmaker(bind=engine)
        session = Session()

        self.sessions[worker_ctx] = session
        return session

    def release_injection(self, worker_ctx):
        session = self.sessions.pop(worker_ctx)
        session.close()