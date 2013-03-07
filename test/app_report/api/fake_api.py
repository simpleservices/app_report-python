from app_report.api import Base


class FakeAPI(Base):

    def params_to_sign(self):
        return ['app_name', 'access_key', 'document', 'id', 'inexistent_param']
